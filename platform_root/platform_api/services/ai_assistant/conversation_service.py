#   Copyright 2026 NEC Corporation
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

チャット会話管理サービス

メッセージのやり取りは個別テーブル(T_CHAT_MESSAGE)を使わず、
T_CHAT_HISTORYにJSON配列（1会話分のターン一覧）としてスナップショット保存する。
配列内の各ターンの構造はフロントエンド(ai_assistant_client.js / amazon_bedrock.js)が
扱う履歴配列と同じ形式（role, content[], _timestamp, _thinkingMs, _model）に揃えている。
"""

import os
import time
from datetime import datetime, timezone
from typing import Optional, List, Dict
from contextlib import closing
import ulid

from common_library.common.db import DBconnector
from common_library.common import common
from libs import queries_ai_assistant
from services.users.ai_credential_service import (
    get_ai_credential_service,
    CredentialNotFound,
)
from services.ai_assistant.aws_session_manager import (
    create_bedrock_session_from_credential_data,
)
from services.ai_assistant.history_service import get_history_service
from ai_providers.base import (
    AIProviderTimeoutError,
    AIProviderValidationError,
)

import globals


class ConversationNotFound(Exception):
    """会話が見つからない"""
    pass


def _now_iso() -> str:
    """UTCの現在時刻をISO8601(Z終端)で返す（フロントエンドの_timestampと同じ形式）"""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _extract_text(turn: Dict) -> str:
    """ターン(role/content[]形式)からtextブロックのみを連結して取り出す"""
    return "".join(
        block.get("text", "")
        for block in turn.get("content", []) or []
        if isinstance(block, dict) and block.get("type") == "text"
    )


class ConversationService:
    """
    Conversation Service

    チャット会話の作成・一覧・メッセージ送受信を管理
    """

    def create_conversation(
        self,
        organization_id: str,
        workspace_id: str,
        user_id: str,
        title: str,
        service_id: str = "LLMEditor",
    ) -> str:
        """
        会話を作成

        Args:
            organization_id: Organization ID (DB接続用、テーブルには保存しない)
            workspace_id: Workspace ID (DB接続用、テーブルには保存しない)
            user_id: User ID
            title: 会話タイトル
            service_id: サービスID（AgenticAI/LLMEditor - システムプロンプト切り替え用）

        Returns:
            str: Conversation ID

        Raises:
            CredentialNotFound: ユーザーがCredentialを登録していない
        """
        # T_USER_CREDENTIALから最新のactiveなCredentialを取得してAI_SERVICE_IDを決定
        with closing(DBconnector().connect_orgdb(organization_id)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    queries_ai_assistant.SQL_SELECT_USER_ACTIVE_CREDENTIAL,
                    {"user_id": user_id},
                )
                row = cursor.fetchone()

                if not row:
                    raise CredentialNotFound(
                        f"No active credential found for user: {user_id}. "
                        "Please register a credential first."
                    )

                ai_service_id = row["CREDENTIAL_TYPE"]

        conversation_id = ulid.new().str

        with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    queries_ai_assistant.SQL_INSERT_CONVERSATION,
                    {
                        "conversation_id": conversation_id,
                        "service_id": service_id,
                        "workspace_id": workspace_id,
                        "user_id": user_id,
                        "ai_service_id": ai_service_id,
                        "title": title,
                    },
                )
                conn.commit()

        globals.logger.debug(
            f"Conversation created: id={conversation_id}, "
            f"org={organization_id}, workspace={workspace_id}, user={user_id}, "
            f"service={service_id}, ai_service={ai_service_id}, title={title}"
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
            organization_id: Organization ID (DB接続用、テーブルには保存しない)
            workspace_id: Workspace ID (DB接続用、テーブルには保存しない)
            user_id: User ID
            status: ステータスフィルター (オプション)
            limit: 取得件数
            offset: オフセット

        Returns:
            List[Dict]: 会話一覧
        """
        with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    queries_ai_assistant.SQL_LIST_CONVERSATIONS,
                    {
                        "user_id": user_id,
                        "status": status,
                        "limit": limit,
                        "offset": offset,
                    },
                )
                conversations = cursor.fetchall()

        globals.logger.debug(
            f"Listed {len(conversations)} conversations: "
            f"org={organization_id}, user={user_id}"
        )

        return conversations

    def create_completion(
        self,
        organization_id: str,
        workspace_id: str,
        user_id: str,
        conversation_id: str,
        message_text: str,
        ai_service_id: str = None,
        model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0",
        user_language: str = None,
        menu_id: str = None,
    ) -> Dict:
        """
        メッセージを送信してAI応答を取得

        会話全体(直前までの全ターン)はT_CHAT_HISTORYの最新スナップショットから取得し、
        ユーザーターン・アシスタントターンを追記した配列を新しいスナップショットとして
        T_CHAT_HISTORYに保存する（T_CHAT_MESSAGEは使用しない）。

        Args:
            organization_id: Organization ID (DB接続用、テーブルには保存しない)
            workspace_id: Workspace ID (DB接続用、テーブルには保存しない)
            user_id: User ID
            conversation_id: Conversation ID
            message_text: ユーザーメッセージ
            ai_service_id: AIサービスID (メッセージ固有、Noneの場合は会話のデフォルトを使用)
            model_id: AIモデルID
            user_language: ユーザー言語 (jp, en, None)
            menu_id: メニューID (ITA画面ID、任意)

        Returns:
            Dict: 送信結果

        Raises:
            ConversationNotFound: 会話が見つからない
        """
        with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn:
            with closing(conn.cursor()) as cursor:
                # 会話の存在確認とAI_SERVICE_ID、SERVICE_IDの取得
                cursor.execute(
                    queries_ai_assistant.SQL_SELECT_CONVERSATION,
                    {"conversation_id": conversation_id, "user_id": user_id},
                )
                conversation = cursor.fetchone()

                if not conversation:
                    raise ConversationNotFound(
                        f"Conversation not found: id={conversation_id}, user={user_id}"
                    )

                # AIサービスIDの決定：メッセージで指定されていればそれを使用、なければ会話のデフォルト
                conversation_default_ai_service_id = conversation["AI_SERVICE_ID"]
                effective_ai_service_id = ai_service_id if ai_service_id else conversation_default_ai_service_id
                service_id = conversation["SERVICE_ID"]

        # 直前までの会話ターン一覧を取得（無ければ新規会話として空配列から開始）
        history = get_history_service().get_latest_history(
            organization_id=organization_id,
            workspace_id=workspace_id,
            conversation_id=conversation_id,
        ) or []

        # ユーザーターンを追記
        user_turn = {
            "role": "user",
            "content": [{"type": "text", "text": message_text}],
            "_timestamp": _now_iso(),
        }
        # 会話のデフォルトと異なるAIサービスが指定された場合のみ記録する（オーバーライドの記録）
        if ai_service_id and ai_service_id != conversation_default_ai_service_id:
            user_turn["_service"] = ai_service_id
        history.append(user_turn)

        # Bedrockを呼び出し
        try:
            # effective_ai_service_idで認証方式を判定
            credential_service = None
            credential = None
            aws_session = None

            if effective_ai_service_id == "bedrock-cache":
                # AWS Login Cache方式（DBから取得、自動トークン更新）
                globals.logger.debug("Using AWS login cache credential for Bedrock authentication")

                credential_service = get_ai_credential_service()
                credential = credential_service.get_credential(
                    organization_id=organization_id,
                    user_id=user_id,
                    credential_type=effective_ai_service_id,
                )

                credential_data = credential.credential_data
                region = credential_data.get("region", "ap-northeast-1")
                aws_session = create_bedrock_session_from_credential_data(
                    credential_data=credential_data,
                    region=region,
                )
                bedrock_client = aws_session.get_bedrock_client()

            elif effective_ai_service_id == "bedrock":
                # 手動Credential方式（固定トークン）
                globals.logger.debug("Using manual credential for Bedrock authentication")

                credential_service = get_ai_credential_service()
                credential = credential_service.get_credential(
                    organization_id=organization_id,
                    user_id=user_id,
                    credential_type=effective_ai_service_id,
                )

                import boto3
                from botocore.config import Config

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
                raise ValueError(f"Unsupported ai_service_id for Bedrock: {effective_ai_service_id}")

            # システムプロンプトを読み込み
            from services.ai_assistant.system_prompt_loader import (
                load_system_prompt,
                load_menu_prompt,
            )

            try:
                system_prompt = load_system_prompt(service_id, user_language)
                globals.logger.debug(
                    f"Loaded system prompt for service_id={service_id}, "
                    f"user_language={user_language}: {len(system_prompt)} chars"
                )
            except FileNotFoundError as e:
                globals.logger.warning(f"System prompt not found: {e}. Using empty prompt.")
                system_prompt = None

            # menu_idが指定されている場合は追加プロンプトを読み込み
            if menu_id:
                try:
                    menu_prompt = load_menu_prompt(menu_id, user_language)
                    if menu_prompt:
                        if system_prompt:
                            system_prompt = f"{system_prompt}\n\n{menu_prompt}"
                        else:
                            system_prompt = menu_prompt
                        globals.logger.debug(
                            f"Loaded and appended menu prompt for menu_id={menu_id}: "
                            f"{len(menu_prompt)} chars, total={len(system_prompt)} chars"
                        )
                except Exception as e:
                    globals.logger.warning(
                        f"Failed to load menu prompt for menu_id={menu_id}: {e}"
                    )

            # 会話履歴（ユーザーターン追記済み）からBedrock用messagesを構築
            # ai_assistant_client.js / amazon_bedrock.jsと同じく、textタイプのcontentのみを渡す
            # （サーバー側のこのエンドポイントはツール呼び出しを行わないシンプルなテキスト対話のため）
            messages = []
            for turn in history:
                text = _extract_text(turn)
                if not text:
                    continue
                messages.append({
                    "role": turn["role"],
                    "content": [{"text": text}],
                })

            converse_params = {
                "modelId": model_id,
                "messages": messages,
                "inferenceConfig": {
                    "maxTokens": 4096,
                },
            }

            if system_prompt:
                converse_params["system"] = [{"text": system_prompt}]

            request_start = time.monotonic()
            response = bedrock_client.converse(**converse_params)
            thinking_ms = round((time.monotonic() - request_start) * 1000)

            assistant_content = response["output"]["message"]["content"][0]["text"]
            input_tokens = response["usage"]["inputTokens"]
            output_tokens = response["usage"]["outputTokens"]

            # アシスタントターンを追記
            assistant_turn = {
                "role": "assistant",
                "content": [{"type": "text", "text": assistant_content}],
                "_timestamp": _now_iso(),
                "_thinkingMs": thinking_ms,
                "_model": model_id,
            }
            history.append(assistant_turn)

            # 新しいスナップショットとしてT_CHAT_HISTORYへ保存し、会話のトークン数を更新
            saved = get_history_service().create_history(
                organization_id=organization_id,
                workspace_id=workspace_id,
                user_id=user_id,
                conversation_id=conversation_id,
                contents=history,
            )

            with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn:
                with closing(conn.cursor()) as cursor:
                    cursor.execute(
                        queries_ai_assistant.SQL_UPDATE_CONVERSATION_TOKEN_COUNT,
                        {
                            "token_count": input_tokens + output_tokens,
                            "user_id": user_id,
                            "conversation_id": conversation_id,
                        },
                    )
                    conn.commit()

            total_turns = len(history)
            user_message_seq = total_turns - 1
            assistant_message_seq = total_turns

            globals.logger.debug(
                f"Message sent and response received: "
                f"conv={conversation_id}, history_id={saved['history_id']}, "
                f"user_seq={user_message_seq}, assistant_seq={assistant_message_seq}, "
                f"tokens={input_tokens}+{output_tokens}"
            )

            # 最終使用日時とトークン更新（Bedrock呼び出し後）
            if credential_service and credential:
                if effective_ai_service_id == "bedrock-cache" and aws_session:
                    latest_token = aws_session.get_current_token()
                    if latest_token:
                        credential_service.update_last_used(
                            organization_id=organization_id,
                            credential_id=credential.credential_id,
                            credential_data=latest_token
                        )
                    else:
                        credential_service.update_last_used(
                            organization_id=organization_id,
                            credential_id=credential.credential_id
                        )
                else:
                    credential_service.update_last_used(
                        organization_id=organization_id,
                        credential_id=credential.credential_id
                    )

            return {
                "conversation_id": conversation_id,
                "history_id": saved["history_id"],
                "user_message_seq": user_message_seq,
                "assistant_message_seq": assistant_message_seq,
                "content": assistant_content,
                "usage": {
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens,
                },
            }

        except AIProviderTimeoutError as e:
            # タイムアウト → InternalError
            globals.logger.error(f"Bedrock request timeout: {e}")
            message_id = "500-94105"
            message = f"AI サービスへのリクエストがタイムアウトしました: {str(e)}"
            raise common.InternalErrorException(
                message_id=message_id, message=message
            ) from e

        except AIProviderValidationError as e:
            # maxTokens 超過などのバリデーションエラー → 413
            error_message = str(e)
            if "maxTokens" in error_message or "token" in error_message.lower():
                globals.logger.error(f"Bedrock payload too large: {e}")
                message_id = "400-94106"
                message = f"リクエストのペイロードが大きすぎます: {str(e)}"
                raise common.BadRequestException(
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
