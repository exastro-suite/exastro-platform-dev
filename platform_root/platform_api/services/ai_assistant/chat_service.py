#   Copyright 2022 NEC Corporation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
Chat Service

チャットメッセージ処理とAI統合
"""

from typing import List, Optional, Dict, Any
from contextlib import closing
import ulid

from common_library.common.db import DBconnector
from ai_providers.base import AIMessage, AIRequest
from ai_providers.bedrock.provider import create_bedrock_provider
from services.ai_assistant.credential_factory import get_credential_service
from services.ai_assistant.ai_router import get_ai_router

import globals


class ConversationNotFound(Exception):
    """会話が見つからない"""
    pass


class ChatService:
    """
    Chat Service

    チャット会話とメッセージの管理、AI呼び出し統合
    """

    def __init__(self):
        self.credential_service = get_credential_service()
        self.ai_router = get_ai_router()

    def send_message(
        self,
        organization_id: str,
        user_id: str,
        conversation_id: Optional[str],
        message_content: str,
        model_id: str,
        ai_service_id: str = "bedrock",
        capability: str = "chat",
        workspace_id: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        メッセージ送信とAI応答取得

        Args:
            organization_id: Organization ID
            user_id: User ID
            conversation_id: 会話ID (新規の場合はNone)
            message_content: ユーザーメッセージ
            model_id: モデルID
            ai_service_id: AIサービスID
            capability: 用途
            workspace_id: Workspace ID
            max_tokens: 最大トークン数
            temperature: Temperature

        Returns:
            Dict: 応答結果
        """
        request_id = str(ulid.ULID())

        with closing(DBconnector().connect_platformdb()) as conn:
            with closing(conn.cursor()) as cursor:
                try:
                    # 1. モデル利用許可チェック
                    self.ai_router.validate_model_permission(
                        organization_id=organization_id,
                        user_id=user_id,
                        ai_service_id=ai_service_id,
                        model_id=model_id,
                        capability=capability,
                    )

                    # 2. 会話の取得 or 作成
                    if conversation_id:
                        conversation = self._get_conversation(cursor, conversation_id)
                        if not conversation:
                            raise ConversationNotFound(
                                f"Conversation not found: {conversation_id}"
                            )
                    else:
                        conversation_id = self._create_conversation(
                            cursor=cursor,
                            organization_id=organization_id,
                            user_id=user_id,
                            workspace_id=workspace_id,
                            ai_service_id=ai_service_id,
                            model_id=model_id,
                        )
                        conn.commit()

                    # 3. ユーザーメッセージ保存
                    user_message_id = self._save_message(
                        cursor=cursor,
                        conversation_id=conversation_id,
                        role="user",
                        content=message_content,
                        user_id=user_id,
                        request_id=request_id,
                    )
                    conn.commit()

                    # 4. 会話履歴取得
                    messages = self._get_conversation_messages(cursor, conversation_id)

                    # 5. AI呼び出し
                    ai_request = AIRequest(
                        messages=[
                            AIMessage(role=msg["ROLE"], content=msg["CONTENT"])
                            for msg in messages
                        ],
                        model_id=model_id,
                        max_tokens=max_tokens,
                        temperature=temperature,
                    )

                    # AWS Credential取得
                    credential = self.credential_service.get_bedrock_credential(
                        organization_id=organization_id,
                        user_id=user_id,
                    )

                    # Bedrockリージョン取得
                    with closing(DBconnector().connect_platformdb()) as conn2:
                        with closing(conn2.cursor()) as cursor2:
                            cursor2.execute(
                                """
                                SELECT BEDROCK_REGION, CONNECTION_ID
                                FROM T_AWS_SSO_CONNECTION
                                WHERE ORGANIZATION_ID = %s AND USER_ID = %s
                                """,
                                (organization_id, user_id)
                            )
                            connection_info = cursor2.fetchone()
                            bedrock_region = connection_info["BEDROCK_REGION"] or "ap-northeast-1"
                            connection_id = connection_info["CONNECTION_ID"]

                    # Bedrock Provider作成
                    provider = create_bedrock_provider(
                        credential=credential,
                        region_name=bedrock_region,
                    )

                    # AI呼び出し
                    ai_response = provider.converse(ai_request)

                    # 6. AI応答保存
                    assistant_message_id = self._save_message(
                        cursor=cursor,
                        conversation_id=conversation_id,
                        role="assistant",
                        content=ai_response.content,
                        user_id=user_id,
                        request_id=request_id,
                        model_id=model_id,
                        token_count=ai_response.usage.output_tokens,
                    )

                    # 7. 会話の最終メッセージ日時更新
                    cursor.execute(
                        """
                        UPDATE T_CHAT_CONVERSATION
                        SET LAST_MESSAGE_AT = NOW(),
                            LAST_UPDATE_TIMESTAMP = NOW()
                        WHERE CONVERSATION_ID = %s
                        """,
                        (conversation_id,)
                    )

                    # 8. 監査ログ記録
                    self._log_ai_usage(
                        cursor=cursor,
                        organization_id=organization_id,
                        workspace_id=workspace_id,
                        user_id=user_id,
                        event_type="bedrock_invoked",
                        ai_service_id=ai_service_id,
                        model_id=model_id,
                        request_id=request_id,
                        conversation_id=conversation_id,
                        message_id=assistant_message_id,
                        connection_id=connection_id,
                        status="success",
                        input_token_count=ai_response.usage.input_tokens,
                        output_token_count=ai_response.usage.output_tokens,
                        latency_ms=ai_response.metadata.get("latency_ms"),
                    )

                    conn.commit()

                    globals.logger.debug(
                        f"Chat message processed successfully: "
                        f"conversation={conversation_id}, "
                        f"request={request_id}, "
                        f"tokens={ai_response.usage.total_tokens}"
                    )

                    return {
                        "conversation_id": conversation_id,
                        "user_message_id": user_message_id,
                        "assistant_message_id": assistant_message_id,
                        "content": ai_response.content,
                        "usage": {
                            "input_tokens": ai_response.usage.input_tokens,
                            "output_tokens": ai_response.usage.output_tokens,
                            "total_tokens": ai_response.usage.total_tokens,
                        },
                        "request_id": request_id,
                    }

                except Exception as e:
                    conn.rollback()
                    globals.logger.error(
                        f"Failed to process chat message: {e}",
                        exc_info=True
                    )

                    # エラー監査ログ
                    self._log_ai_usage(
                        cursor=cursor,
                        organization_id=organization_id,
                        workspace_id=workspace_id,
                        user_id=user_id,
                        event_type="bedrock_invoke_failed",
                        ai_service_id=ai_service_id,
                        model_id=model_id,
                        request_id=request_id,
                        conversation_id=conversation_id,
                        connection_id=None,
                        status="failed",
                        error_code=type(e).__name__,
                        error_message=str(e),
                    )
                    conn.commit()

                    raise

    def _get_conversation(self, cursor, conversation_id: str) -> Optional[Dict]:
        """会話を取得"""
        cursor.execute(
            """
            SELECT * FROM T_CHAT_CONVERSATION
            WHERE CONVERSATION_ID = %s AND STATUS = 'active'
            """,
            (conversation_id,)
        )
        return cursor.fetchone()

    def _create_conversation(
        self,
        cursor,
        organization_id: str,
        user_id: str,
        workspace_id: Optional[str],
        ai_service_id: str,
        model_id: str,
    ) -> str:
        """新規会話作成"""
        conversation_id = str(ulid.ULID())

        cursor.execute(
            """
            INSERT INTO T_CHAT_CONVERSATION
            (
                CONVERSATION_ID, ORGANIZATION_ID, WORKSPACE_ID, USER_ID,
                AI_SERVICE_ID, MODEL_ID, STATUS,
                CREATE_TIMESTAMP, CREATE_USER,
                LAST_UPDATE_TIMESTAMP, LAST_UPDATE_USER
            )
            VALUES
            (%s, %s, %s, %s, %s, %s, 'active', NOW(), %s, NOW(), %s)
            """,
            (
                conversation_id, organization_id, workspace_id, user_id,
                ai_service_id, model_id, user_id, user_id
            )
        )

        globals.logger.debug(
            f"Created new conversation: id={conversation_id}, "
            f"org={organization_id}, user={user_id}"
        )
        return conversation_id

    def _save_message(
        self,
        cursor,
        conversation_id: str,
        role: str,
        content: str,
        user_id: str,
        request_id: str,
        model_id: Optional[str] = None,
        token_count: Optional[int] = None,
    ) -> str:
        """メッセージ保存"""
        message_id = str(ulid.ULID())

        # シーケンス番号取得
        cursor.execute(
            """
            SELECT COALESCE(MAX(SEQUENCE_NUMBER), 0) + 1 AS next_seq
            FROM T_CHAT_MESSAGE
            WHERE CONVERSATION_ID = %s
            """,
            (conversation_id,)
        )
        sequence_number = cursor.fetchone()["next_seq"]

        cursor.execute(
            """
            INSERT INTO T_CHAT_MESSAGE
            (
                MESSAGE_ID, CONVERSATION_ID, ROLE, CONTENT,
                SEQUENCE_NUMBER, MODEL_ID, TOKEN_COUNT, REQUEST_ID,
                CREATE_TIMESTAMP, CREATE_USER,
                LAST_UPDATE_TIMESTAMP, LAST_UPDATE_USER
            )
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, NOW(), %s)
            """,
            (
                message_id, conversation_id, role, content,
                sequence_number, model_id, token_count, request_id,
                user_id, user_id
            )
        )

        return message_id

    def _get_conversation_messages(self, cursor, conversation_id: str) -> List[Dict]:
        """会話履歴取得"""
        cursor.execute(
            """
            SELECT ROLE, CONTENT
            FROM T_CHAT_MESSAGE
            WHERE CONVERSATION_ID = %s
            ORDER BY SEQUENCE_NUMBER ASC
            """,
            (conversation_id,)
        )
        return cursor.fetchall()

    def _log_ai_usage(
        self,
        cursor,
        organization_id: str,
        user_id: str,
        event_type: str,
        status: str,
        workspace_id: Optional[str] = None,
        ai_service_id: Optional[str] = None,
        model_id: Optional[str] = None,
        request_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        message_id: Optional[str] = None,
        connection_id: Optional[str] = None,
        input_token_count: Optional[int] = None,
        output_token_count: Optional[int] = None,
        latency_ms: Optional[int] = None,
        error_code: Optional[str] = None,
        error_message: Optional[str] = None,
    ):
        """監査ログ記録"""
        audit_log_id = str(ulid.ULID())

        cursor.execute(
            """
            INSERT INTO T_AI_USAGE_AUDIT_LOG
            (
                AUDIT_LOG_ID, ORGANIZATION_ID, WORKSPACE_ID, USER_ID,
                EVENT_TYPE, AI_SERVICE_ID, MODEL_ID, REQUEST_ID,
                CONVERSATION_ID, MESSAGE_ID, CONNECTION_ID, STATUS,
                INPUT_TOKEN_COUNT, OUTPUT_TOKEN_COUNT, LATENCY_MS,
                ERROR_CODE, ERROR_MESSAGE,
                CREATE_TIMESTAMP, CREATE_USER
            )
            VALUES
            (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                NOW(), %s
            )
            """,
            (
                audit_log_id, organization_id, workspace_id, user_id,
                event_type, ai_service_id, model_id, request_id,
                conversation_id, message_id, connection_id, status,
                input_token_count, output_token_count, latency_ms,
                error_code, error_message,
                user_id
            )
        )
