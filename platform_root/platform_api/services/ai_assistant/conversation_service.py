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

会話のやり取りは1ターンずつの個別レコードではなく、T_CHAT_MESSAGEに
JSON配列（1会話分のターン一覧）としてスナップショット保存する。
配列内の各ターンの構造はフロントエンド(ai_assistant_client.js / amazon_bedrock.js)が
扱う履歴配列と同じ形式（role, content[], _timestamp, _thinkingMs, _model）に揃えている。
"""

import os
import time
from datetime import datetime, timezone
from typing import Optional, List, Dict
from contextlib import closing
import ulid
from botocore.exceptions import (
    ClientError,
    BotoCoreError,
    ConnectTimeoutError,
    ReadTimeoutError,
)

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
from services.ai_assistant.message_service import get_message_service

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
        message_text: str = None,
        ai_service_id: str = None,
        model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0",
        user_language: str = None,
        menu_id: str = None,
    ) -> Dict:
        """
        メッセージを送信してAI応答を取得

        会話全体(直前までの全ターン)はT_CHAT_MESSAGEの最新スナップショットから取得し、
        ユーザーターン・アシスタントターンを追記した配列を新しいスナップショットとして
        T_CHAT_MESSAGEに保存する。

        message_textを省略した場合は、T_CHAT_MESSAGEの既存内容のみでAIに問い合わせる
        （新規ユーザーターンは追加しない）。この場合、応答結果はT_CHAT_MESSAGEに保存せず、
        会話のトークン数も更新しない（問い合わせ結果を確認するだけの用途）。

        Args:
            organization_id: Organization ID (DB接続用、テーブルには保存しない)
            workspace_id: Workspace ID (DB接続用、テーブルには保存しない)
            user_id: User ID
            conversation_id: Conversation ID
            message_text: ユーザーメッセージ (省略可。省略時は既存履歴のみで問い合わせ、結果を保存しない)
            ai_service_id: AIサービスID (メッセージ固有、Noneの場合は会話のデフォルトを使用)
            model_id: AIモデルID
            user_language: ユーザー言語 (jp, en, None)
            menu_id: メニューID (ITA画面ID、任意)

        Returns:
            Dict: 送信結果

        Raises:
            ConversationNotFound: 会話が見つからない
        """
        # message_textの有無で「新規発言して保存する」か「既存履歴のみで問い合わせて保存しない」かの動作が分岐する
        # Whether message_text is provided branches behavior: "post a new message and save" vs. "query using only existing history without saving"
        has_new_message = bool(message_text)
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
        messages = get_message_service().get_latest_message(
            organization_id=organization_id,
            workspace_id=workspace_id,
            conversation_id=conversation_id,
        ) or []

        # LLMに渡すターン一覧（保存対象のmessagesとは別に持つ）
        # ・message指定時: messagesにユーザーターンを追記したものをそのまま使う
        # ・message省略時: 履歴の最後がassistantターンで終わっている場合、Bedrock Converse APIは
        #   assistantターンで終わる会話を受け付けない（"assistant message prefill"未対応で、
        #   必ずuserターンで終える必要がある）ため、直前のassistant応答を一時的に取り除いて
        #   （＝再生成）その手前のuserターンまでで問い合わせる。取り除いた結果は保存しない。
        llm_input_messages = messages

        if has_new_message:
            # ユーザーターンを追記
            # Append the new user turn
            user_turn = {
                "role": "user",
                "content": [{"type": "text", "text": message_text}],
                "_timestamp": _now_iso(),
            }
            # 会話のデフォルトと異なるAIサービスが指定された場合のみ記録する（オーバーライドの記録）
            # Record the override only when the specified AI service differs from the conversation's default
            if ai_service_id and ai_service_id != conversation_default_ai_service_id:
                user_turn["_service"] = ai_service_id
            messages.append(user_turn)
            llm_input_messages = messages
        elif not messages:
            # 新規メッセージも既存履歴も無い場合は問い合わせ不可
            # Cannot query when there is neither a new message nor any existing history
            raise common.BadRequestException(
                message_id="400-94107",
                message="messageが未指定で、会話に既存の履歴もありません",
            )
        elif messages[-1].get("role") == "assistant":
            # 直前のassistant応答を一時的に取り除き、再生成（結果は保存しない）
            # Temporarily drop the trailing assistant turn and regenerate the response (the result is not saved)
            llm_input_messages = messages[:-1]
            if not llm_input_messages:
                # assistantターンを除いた結果userターンも残らない＝問い合わせ可能な発言が無いため400エラー
                # No user turn remains after removing the assistant turn, i.e. nothing to query, so raise a 400 error
                raise common.BadRequestException(
                    message_id="400-94108",
                    message="messageが未指定で、会話に問い合わせ可能なユーザーメッセージがありません",
                )

        # Bedrockを呼び出し
        try:
            # effective_ai_service_idで認証方式を判定
            credential_service = None
            credential = None
            aws_session = None

            if effective_ai_service_id == "bedrock-cache":
                # AWS Login Cache方式（DBから取得、自動トークン更新）
                # AWS login cache method (retrieved from the DB, with automatic token refresh)
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
                # Manual credential method (fixed/static token)
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
                # bedrock-cache/bedrock以外のai_service_idは現時点で未対応（将来、他AIプロバイダー対応時に分岐を追加）
                # Any ai_service_id other than bedrock-cache/bedrock is currently unsupported (add a branch here when other AI providers are supported)
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
            # Load the additional prompt only when menu_id is specified
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

            # 会話メッセージ（ユーザーターン追記済み、または再生成用に末尾assistantを除いたもの）
            # からBedrock用messagesを構築する。
            # ai_assistant_client.js / amazon_bedrock.jsと同じく、textタイプのcontentのみを渡す
            # （サーバー側のこのエンドポイントはツール呼び出しを行わないシンプルなテキスト対話のため）
            bedrock_messages = []
            for turn in llm_input_messages:
                text = _extract_text(turn)
                if not text:
                    continue
                bedrock_messages.append({
                    "role": turn["role"],
                    "content": [{"text": text}],
                })

            converse_params = {
                "modelId": model_id,
                "messages": bedrock_messages,
                "inferenceConfig": {
                    "maxTokens": 4096,
                },
            }

            if system_prompt:
                converse_params["system"] = [{"text": system_prompt}]

            request_start = time.monotonic()
            response = bedrock_client.converse(**converse_params)
            thinking_ms = round((time.monotonic() - request_start) * 1000)

            # AIサービスが返したHTTPステータスコードをそのまま呼び出し元に返す
            # （ai_assistant_client.js / amazon_bedrock.jsのfetchWithRetryと同様、
            # 呼び出し側でステータスコードに基づくリトライ判断ができるようにするため。
            # 将来的にBedrock以外のAIサービスに対応した場合も同じキーで返せるよう汎用名にしている）
            ai_status_code = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

            # 拡張思考対応モデルはcontent[0]がreasoningContentブロックになる場合があり、必ずしもtextブロックとは限らないため、textキーを持つブロックのみ連結して取り出す
            # Extended-thinking-capable models may put a reasoningContent block at content[0], so it isn't always the text block — concatenate only the blocks that have a text key
            assistant_content = "".join(
                block.get("text", "")
                for block in response["output"]["message"]["content"]
                if "text" in block
            )
            input_tokens = response["usage"]["inputTokens"]
            output_tokens = response["usage"]["outputTokens"]

            if has_new_message:
                # 新規発言がある場合のみ、応答をT_CHAT_MESSAGEに保存しトークン数を更新する
                # Only when there is a new user message do we save the response to T_CHAT_MESSAGE and update the token count
                # アシスタントターンを追記
                assistant_turn = {
                    "role": "assistant",
                    "content": [{"type": "text", "text": assistant_content}],
                    "_timestamp": _now_iso(),
                    "_thinkingMs": thinking_ms,
                    "_model": model_id,
                }
                messages.append(assistant_turn)

                # 新しいスナップショットとしてT_CHAT_MESSAGEへ保存し、会話のトークン数を更新
                saved = get_message_service().create_message(
                    organization_id=organization_id,
                    workspace_id=workspace_id,
                    user_id=user_id,
                    conversation_id=conversation_id,
                    contents=messages,
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

                total_turns = len(messages)
                saved_message_id = saved["message_id"]
                user_message_seq = total_turns - 1
                assistant_message_seq = total_turns

                globals.logger.debug(
                    f"Message sent and response received: "
                    f"conv={conversation_id}, message_id={saved_message_id}, "
                    f"user_seq={user_message_seq}, assistant_seq={assistant_message_seq}, "
                    f"tokens={input_tokens}+{output_tokens}"
                )
            else:
                # messageを指定しない問い合わせ：既存履歴のみで応答を取得し、保存は行わない
                # Query without a message: get the response using only existing history, and do not persist it
                saved_message_id = None
                user_message_seq = None
                assistant_message_seq = None

                globals.logger.debug(
                    f"Completion generated without persisting (no message provided): "
                    f"conv={conversation_id}, tokens={input_tokens}+{output_tokens}"
                )

            # 最終使用日時とトークン更新（Bedrock呼び出し後）
            if credential_service and credential:
                # bedrock-cache方式のみ呼び出し中に自動更新されたトークンをDBへ書き戻す（bedrock方式は固定トークンのため対象外）
                # Only the bedrock-cache method writes the auto-refreshed token back to the DB (not applicable to the fixed-token bedrock method)
                if effective_ai_service_id == "bedrock-cache" and aws_session:
                    latest_token = aws_session.get_current_token()
                    if latest_token:
                        credential_service.update_last_used(
                            organization_id=organization_id,
                            credential_id=credential.credential_id,
                            credential_data=latest_token
                        )
                    else:
                        # トークンが更新されていない（取得できない）場合は最終使用日時のみ更新
                        # If no refreshed token is available, update only the last-used timestamp
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
                "message_id": saved_message_id,
                "user_message_seq": user_message_seq,
                "assistant_message_seq": assistant_message_seq,
                "content": assistant_content,
                "saved": has_new_message,
                "ai_status_code": ai_status_code,
                "usage": {
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens,
                },
            }

        except ClientError as e:
            # BedrockがHTTPエラーとして返したステータスコードを400/500等にまとめず、そのまま呼び出し元に伝播する（JS版のリトライ判断に合わせる）
            # Propagate the HTTP status code Bedrock returned as-is to the caller instead of collapsing it into 400/500 (matches the JS client's retry logic)
            response_metadata = e.response.get("ResponseMetadata", {})
            status_code = response_metadata.get("HTTPStatusCode", 500)
            error_info = e.response.get("Error", {})
            error_code = error_info.get("Code", "Unknown")
            error_message = error_info.get("Message", str(e))
            globals.logger.error(
                f"Bedrock ClientError: status={status_code}, code={error_code}, message={error_message}"
            )
            raise common.OtherException(
                status_code=status_code,
                message_id=f"{status_code}-94109",
                message=f"AIサービスAPIエラー ({error_code}): {error_message}",
            ) from e

        except (ReadTimeoutError, ConnectTimeoutError) as e:
            # HTTPステータスが存在しないネットワークタイムアウトのため、JS版のtimeoutStatuses([408, 504])に合わせて408として返す
            # No HTTP status exists for a network-level timeout, so return 408 to match the JS client's timeoutStatuses ([408, 504])
            globals.logger.error(f"Bedrock request timeout: {e}")
            raise common.OtherException(
                status_code=408,
                message_id="408-94110",
                message=f"AIサービスへのリクエストがタイムアウトしました: {str(e)}",
            ) from e

        except BotoCoreError as e:
            # Bedrock自体からのHTTPステータスコードが得られないその他の接続エラー（DNS失敗等）は503として返す
            # Other connection-level errors with no HTTP status code from Bedrock itself (e.g. DNS failure) are returned as 503
            globals.logger.error(f"Bedrock request failed (connection error): {e}")
            raise common.OtherException(
                status_code=503,
                message_id="503-94111",
                message=f"AIサービスへの接続に失敗しました: {str(e)}",
            ) from e

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
