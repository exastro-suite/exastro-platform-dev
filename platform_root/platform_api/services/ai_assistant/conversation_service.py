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
Conversation Service

チャット会話・メッセージ管理サービス
"""

import os
from typing import Optional, List, Dict
from contextlib import closing
import ulid

from common_library.common.db import DBconnector
from common_library.common import common
from services.ai_assistant.ai_credential_service import (
    get_ai_credential_service,
    CredentialNotFound,
)
from services.ai_assistant.aws_session_manager import (
    create_bedrock_session_from_credential_data,
)
from ai_providers.base import (
    AIProviderTimeoutError,
    AIProviderValidationError,
)

import globals


class ConversationNotFound(Exception):
    """会話が見つからない"""
    pass


class ConversationService:
    """
    Conversation Service

    チャット会話・メッセージ管理
    """

    def create_conversation(
        self,
        organization_id: str,
        workspace_id: str,
        user_id: str,
        title: str,
    ) -> str:
        """
        会話を作成

        Args:
            organization_id: Organization ID
            workspace_id: Workspace ID
            user_id: User ID
            title: 会話タイトル

        Returns:
            str: Conversation ID
        """
        conversation_id = ulid.new().str

        with closing(DBconnector().connect_platformdb()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    """
                    INSERT INTO T_CHAT_CONVERSATION
                    (
                        CONVERSATION_ID, ORGANIZATION_ID, WORKSPACE_ID, USER_ID, TITLE,
                        STATUS,
                        CREATE_TIMESTAMP, CREATE_USER,
                        LAST_UPDATE_TIMESTAMP, LAST_UPDATE_USER
                    )
                    VALUES
                    (
                        %s, %s, %s, %s, %s, 'active',
                        NOW(), %s, NOW(), %s
                    )
                    """,
                    (
                        conversation_id,
                        organization_id,
                        workspace_id,
                        user_id,
                        title,
                        user_id,
                        user_id,
                    ),
                )
                conn.commit()

        globals.logger.debug(
            f"Conversation created: id={conversation_id}, "
            f"org={organization_id}, workspace={workspace_id}, user={user_id}, title={title}"
        )

        return conversation_id

    def list_conversations(
        self,
        organization_id: str,
        workspace_id: str,
        user_id: str,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict]:
        """
        会話一覧を取得

        Args:
            organization_id: Organization ID
            workspace_id: Workspace ID
            user_id: User ID
            status: ステータスフィルター (オプション)
            limit: 取得件数
            offset: オフセット

        Returns:
            List[Dict]: 会話一覧
        """
        with closing(DBconnector().connect_platformdb()) as conn:
            with closing(conn.cursor()) as cursor:
                # メッセージ数をサブクエリで取得
                if status:
                    cursor.execute(
                        """
                        SELECT
                            c.CONVERSATION_ID, c.TITLE, c.STATUS,
                            c.CURRENT_TOKEN_COUNT, c.CREATE_TIMESTAMP, c.LAST_UPDATE_TIMESTAMP,
                            (SELECT COUNT(*) FROM T_CHAT_MESSAGE m
                             WHERE m.CONVERSATION_ID = c.CONVERSATION_ID) AS MESSAGE_COUNT
                        FROM T_CHAT_CONVERSATION c
                        WHERE c.ORGANIZATION_ID = %s AND c.WORKSPACE_ID = %s AND c.USER_ID = %s AND c.STATUS = %s
                        ORDER BY c.LAST_UPDATE_TIMESTAMP DESC
                        LIMIT %s OFFSET %s
                        """,
                        (organization_id, workspace_id, user_id, status, limit, offset),
                    )
                else:
                    cursor.execute(
                        """
                        SELECT
                            c.CONVERSATION_ID, c.TITLE, c.STATUS,
                            c.CURRENT_TOKEN_COUNT, c.CREATE_TIMESTAMP, c.LAST_UPDATE_TIMESTAMP,
                            (SELECT COUNT(*) FROM T_CHAT_MESSAGE m
                             WHERE m.CONVERSATION_ID = c.CONVERSATION_ID) AS MESSAGE_COUNT
                        FROM T_CHAT_CONVERSATION c
                        WHERE c.ORGANIZATION_ID = %s AND c.WORKSPACE_ID = %s AND c.USER_ID = %s
                        ORDER BY c.LAST_UPDATE_TIMESTAMP DESC
                        LIMIT %s OFFSET %s
                        """,
                        (organization_id, workspace_id, user_id, limit, offset),
                    )

                conversations = cursor.fetchall()

                globals.logger.debug(
                    f"Listed {len(conversations)} conversations: "
                    f"org={organization_id}, user={user_id}"
                )

                return conversations

    def list_messages(
        self,
        organization_id: str,
        workspace_id: str,
        user_id: str,
        conversation_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict]:
        """
        メッセージ一覧を取得

        Args:
            organization_id: Organization ID
            workspace_id: Workspace ID
            user_id: User ID
            conversation_id: Conversation ID
            limit: 取得件数
            offset: オフセット（message_seq基準）

        Returns:
            List[Dict]: メッセージ一覧

        Raises:
            ConversationNotFound: 会話が見つからない
        """
        with closing(DBconnector().connect_platformdb()) as conn:
            with closing(conn.cursor()) as cursor:
                # 会話の存在確認
                cursor.execute(
                    """
                    SELECT CONVERSATION_ID
                    FROM T_CHAT_CONVERSATION
                    WHERE CONVERSATION_ID = %s AND ORGANIZATION_ID = %s AND USER_ID = %s
                    """,
                    (conversation_id, organization_id, user_id),
                )
                conversation = cursor.fetchone()

                if not conversation:
                    raise ConversationNotFound(
                        f"Conversation not found: id={conversation_id}, "
                        f"org={organization_id}, user={user_id}"
                    )

                # メッセージ一覧取得
                cursor.execute(
                    """
                    SELECT
                        MESSAGE_ID, CONVERSATION_ID, MESSAGE_SEQ, ROLE,
                        MESSAGE_TEXT, AI_SERVICE_ID, AI_MODEL_ID,
                        TOKEN_COUNT, CREATE_TIMESTAMP
                    FROM T_CHAT_MESSAGE
                    WHERE CONVERSATION_ID = %s
                    ORDER BY MESSAGE_SEQ ASC
                    LIMIT %s OFFSET %s
                    """,
                    (conversation_id, limit, offset),
                )

                messages = cursor.fetchall()

                globals.logger.debug(
                    f"Listed {len(messages)} messages: "
                    f"conv={conversation_id}"
                )

                return messages

    def send_message(
        self,
        organization_id: str,
        workspace_id: str,
        user_id: str,
        conversation_id: str,
        message_text: str,
        model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0",
        ai_service_id: str = "bedrock",
    ) -> Dict:
        """
        メッセージを送信してAI応答を取得

        Args:
            organization_id: Organization ID
            workspace_id: Workspace ID
            user_id: User ID
            conversation_id: Conversation ID
            message_text: ユーザーメッセージ
            model_id: AIモデルID
            ai_service_id: AIサービスID

        Returns:
            Dict: 送信結果

        Raises:
            ConversationNotFound: 会話が見つからない
        """
        with closing(DBconnector().connect_platformdb()) as conn:
            with closing(conn.cursor()) as cursor:
                # 会話の存在確認
                cursor.execute(
                    """
                    SELECT CONVERSATION_ID
                    FROM T_CHAT_CONVERSATION
                    WHERE CONVERSATION_ID = %s AND ORGANIZATION_ID = %s AND USER_ID = %s
                    """,
                    (conversation_id, organization_id, user_id),
                )
                conversation = cursor.fetchone()

                if not conversation:
                    raise ConversationNotFound(
                        f"Conversation not found: id={conversation_id}, "
                        f"org={organization_id}, user={user_id}"
                    )

                # 次のメッセージSEQを取得
                cursor.execute(
                    """
                    SELECT COALESCE(MAX(MESSAGE_SEQ), 0) + 1 AS next_seq
                    FROM T_CHAT_MESSAGE
                    WHERE CONVERSATION_ID = %s
                    """,
                    (conversation_id,),
                )
                result = cursor.fetchone()
                next_seq = result["next_seq"]

                # ユーザーメッセージを保存
                user_message_id = ulid.new().str
                cursor.execute(
                    """
                    INSERT INTO T_CHAT_MESSAGE
                    (
                        MESSAGE_ID, CONVERSATION_ID, MESSAGE_SEQ, ROLE,
                        MESSAGE_TEXT, TOKEN_COUNT,
                        CREATE_TIMESTAMP, CREATE_USER
                    )
                    VALUES
                    (
                        %s, %s, %s, 'user',
                        %s, 0,
                        NOW(), %s
                    )
                    """,
                    (
                        user_message_id,
                        conversation_id,
                        next_seq,
                        message_text,
                        user_id,
                    ),
                )

                # 会話履歴を取得
                cursor.execute(
                    """
                    SELECT ROLE, MESSAGE_TEXT
                    FROM T_CHAT_MESSAGE
                    WHERE CONVERSATION_ID = %s
                    ORDER BY MESSAGE_SEQ ASC
                    """,
                    (conversation_id,),
                )
                history = cursor.fetchall()

                conn.commit()

        # Bedrockを呼び出し
        try:
            # ai_service_idで認証方式を判定
            # 変数を外側で定義
            credential_service = None
            credential = None
            aws_session = None

            if ai_service_id == "aws-cache":
                # AWS Login Cache方式（DBから取得、自動トークン更新）
                globals.logger.debug("Using AWS login cache credential for Bedrock authentication")

                # Credentialを取得
                credential_service = get_ai_credential_service()
                credential = credential_service.get_credential(
                    organization_id=organization_id,
                    user_id=user_id,
                    ai_service_id=ai_service_id,
                )

                # DBから取得したCredentialデータでセッションを作成
                credential_data = credential.credential_data
                region = credential_data.get("region", "ap-northeast-1")
                aws_session = create_bedrock_session_from_credential_data(
                    credential_data=credential_data,
                    region=region,
                )
                bedrock_client = aws_session.get_bedrock_client()

            elif ai_service_id == "bedrock":
                # 手動Credential方式（固定トークン）
                globals.logger.debug("Using manual credential for Bedrock authentication")

                # Credentialを取得
                credential_service = get_ai_credential_service()
                credential = credential_service.get_credential(
                    organization_id=organization_id,
                    user_id=user_id,
                    ai_service_id=ai_service_id,
                )

                # boto3 session作成
                import boto3
                from botocore.config import Config

                # 環境変数からタイムアウト・リトライ設定を読み取り
                read_timeout = int(os.getenv("AI_ASSISTANT_READ_TIMEOUT", "120"))
                connect_timeout = int(os.getenv("AI_ASSISTANT_CONNECT_TIMEOUT", "30"))
                max_attempts = int(os.getenv("AI_ASSISTANT_MAX_ATTEMPTS", "1"))

                credential_data = credential.credential_data
                session = boto3.Session(
                    aws_access_key_id=credential_data.get("access_key_id"),
                    aws_secret_access_key=credential_data.get("secret_access_key"),
                    aws_session_token=credential_data.get("session_token"),
                    region_name=credential_data.get("region", "ap-northeast-1"),
                )

                bedrock_client = session.client(
                    "bedrock-runtime",
                    config=Config(
                        read_timeout=read_timeout,
                        connect_timeout=connect_timeout,
                        retries={"max_attempts": max_attempts, "mode": "standard"},
                    ),
                )

            else:
                raise ValueError(f"Unsupported ai_service_id for Bedrock: {ai_service_id}")

            # 会話履歴を構築
            messages = []
            for msg in history:
                messages.append({
                    "role": msg["ROLE"],
                    "content": [{"text": msg["MESSAGE_TEXT"]}]
                })

            # Bedrockを呼び出し
            response = bedrock_client.converse(
                modelId=model_id,
                messages=messages,
                inferenceConfig={
                    "maxTokens": 4096,
                    "temperature": 0.7,
                },
            )

            # アシスタントメッセージを保存
            assistant_message_id = ulid.new().str
            assistant_content = response["output"]["message"]["content"][0]["text"]
            input_tokens = response["usage"]["inputTokens"]
            output_tokens = response["usage"]["outputTokens"]

            with closing(DBconnector().connect_platformdb()) as conn:
                with closing(conn.cursor()) as cursor:
                    cursor.execute(
                        """
                        INSERT INTO T_CHAT_MESSAGE
                        (
                            MESSAGE_ID, CONVERSATION_ID, MESSAGE_SEQ, ROLE,
                            MESSAGE_TEXT, AI_SERVICE_ID, AI_MODEL_ID,
                            TOKEN_COUNT,
                            CREATE_TIMESTAMP, CREATE_USER
                        )
                        VALUES
                        (
                            %s, %s, %s, 'assistant',
                            %s, %s, %s,
                            %s,
                            NOW(), %s
                        )
                        """,
                        (
                            assistant_message_id,
                            conversation_id,
                            next_seq + 1,
                            assistant_content,
                            ai_service_id,
                            model_id,
                            output_tokens,
                            user_id,
                        ),
                    )

                    # 会話のトークン数を更新
                    cursor.execute(
                        """
                        UPDATE T_CHAT_CONVERSATION
                        SET CURRENT_TOKEN_COUNT = CURRENT_TOKEN_COUNT + %s,
                            ACTIVE_TOKEN_COUNT = ACTIVE_TOKEN_COUNT + %s,
                            LAST_UPDATE_TIMESTAMP = NOW(),
                            LAST_UPDATE_USER = %s
                        WHERE CONVERSATION_ID = %s
                        """,
                        (
                            input_tokens + output_tokens,
                            input_tokens + output_tokens,
                            user_id,
                            conversation_id,
                        ),
                    )

                    conn.commit()

            globals.logger.debug(
                f"Message sent and response received: "
                f"conv={conversation_id}, "
                f"user_msg={user_message_id}, "
                f"assistant_msg={assistant_message_id}, "
                f"tokens={input_tokens}+{output_tokens}"
            )

            # 最終使用日時とトークン更新（Bedrock呼び出し後）
            if credential_service and credential:
                if ai_service_id == "aws-cache" and aws_session:
                    # aws-cacheの場合、トークンが自動更新されている可能性がある
                    latest_token = aws_session.get_current_token()
                    if latest_token:
                        # トークンが更新された場合、Credentialデータも一緒に保存
                        credential_service.update_last_used(
                            credential.credential_id,
                            credential_data=latest_token
                        )
                    else:
                        # トークンは更新されていないが、LAST_USED_ATは更新
                        credential_service.update_last_used(credential.credential_id)
                else:
                    # bedrock（固定トークン）の場合、LAST_USED_ATのみ更新
                    credential_service.update_last_used(credential.credential_id)

            return {
                "conversation_id": conversation_id,
                "user_message_id": user_message_id,
                "assistant_message_id": assistant_message_id,
                "content": assistant_content,
                "usage": {
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens,
                },
            }

        except AIProviderTimeoutError as e:
            # タイムアウト → 408
            globals.logger.error(f"Bedrock request timeout: {e}")
            message_id = "408-94105"
            message = f"AI サービスへのリクエストがタイムアウトしました: {str(e)}"
            raise common.RequestTimeoutException(
                message_id=message_id, message=message
            ) from e

        except AIProviderValidationError as e:
            # maxTokens 超過などのバリデーションエラー → 413
            error_message = str(e)
            if "maxTokens" in error_message or "token" in error_message.lower():
                globals.logger.error(f"Bedrock payload too large: {e}")
                message_id = "413-94106"
                message = f"リクエストのペイロードが大きすぎます: {str(e)}"
                raise common.PayloadTooLargeException(
                    message_id=message_id, message=message
                ) from e
            else:
                # その他のバリデーションエラーは 400
                globals.logger.error(f"Bedrock validation error: {e}")
                raise

        except CredentialNotFound as e:
            globals.logger.error(f"Credential not found: {e}")
            raise Exception("AWS Credentialが登録されていません。先にCredentialを登録してください。")

        except Exception as e:
            globals.logger.error(f"Failed to call Bedrock: {e}", exc_info=True)
            raise


# グローバルインスタンス
_global_conversation_service = ConversationService()


def get_conversation_service() -> ConversationService:
    """
    グローバルConversationServiceを取得

    Returns:
        ConversationService: インスタンス
    """
    return _global_conversation_service
