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
AI Assistant Service Controller

AIアシスタントに関する操作
"""

import connexion
import copy
import inspect
import json
from contextlib import closing

from common_library.common import common, multi_lang, organization_options, validation
from common_library.common.db import DBconnector
from services.ai_assistant.conversation_service import (
    get_conversation_service,
    ConversationNotFound,
)
from services.ai_assistant.message_service import get_message_service
from services.users.ai_credential_service import CredentialNotFound

import globals

# AIアシスタント機能(ai_assistant driver)が有効な組織のみAIAssistantServiceのAPIを許可するデコレータ
# Decorator that only allows AIAssistantService APIs for organizations with the ai_assistant driver enabled
require_ai_assistant_driver = organization_options.require_ita_driver(
    "ai_assistant",
    "403-44001",
    "AIアシスタント機能が有効になっていません",
)

# 現時点でシステムとして利用可能なAIサービス一覧（固定値。他プロバイダー対応時にここへ追加する）
# List of AI services currently supported by the system (fixed; add to this when other providers are supported)
AVAILABLE_AI_SERVICES = [
    {
        "ai_service_id": "bedrock-cache",
        "ai_service_name": "Amazon Bedrock (Login Cache)",
        "description": "AWS Login Cacheを使用し、トークンを自動更新する認証方式",
        # credential_data入力フォームの定義。ここで定義したキー名でそのままcredential_dataに保存される
        # (例: apiKeyの値はcredential_data.apiKeyに入る)
        # Definition of the credential_data input form. Saved into credential_data verbatim under these key names
        # (e.g. the value of apiKey ends up in credential_data.apiKey)
        "settings": {
            "apiKey": {
                "title": "認証情報（Login Cache）",
                "type": "password",
                "required": True,
            },
        },
    },
    {
        "ai_service_id": "bedrock",
        "ai_service_name": "Amazon Bedrock",
        "description": "手動登録したアクセスキー等の固定Credentialを使用する認証方式",
        "settings": {
            "accessKeyId": {
                "title": "AWS Access Key ID",
                "type": "text",
                "required": True,
            },
            "secretAccessKey": {
                "title": "AWS Secret Access Key",
                "type": "password",
                "required": True,
            },
            "sessionToken": {
                "title": "AWS Session Token (optional for SSO)",
                "type": "password",
                "required": False,
            },
            "region": {
                "title": "AWS Region",
                "type": "text",
                "required": False,
            },
        },
    },
]

# AVAILABLE_AI_SERVICESのdescription/settings[].titleをmulti_lang.get_textで多言語化するための対応表。
# (service_id, "description") または (service_id, "settings", setting_key, "title") -> message_id
# multi_lang.get_textはリクエストコンテキスト(Languageヘッダー)が必要なため、モジュール読み込み時ではなく
# リクエスト処理時に_localized_ai_services()で差し替える
# Mapping used to localize AVAILABLE_AI_SERVICES' description/settings[].title via multi_lang.get_text.
# multi_lang.get_text requires an active request context (Language header), so the substitution happens
# at request time in _localized_ai_services(), not at module load time
_AI_SERVICE_TEXT_MESSAGE_IDS = {
    ("bedrock-cache", "description"): "000-44001",
    ("bedrock-cache", "settings", "apiKey", "title"): "000-44002",
    ("bedrock", "description"): "000-44003",
    ("bedrock", "settings", "accessKeyId", "title"): "000-44004",
    ("bedrock", "settings", "secretAccessKey", "title"): "000-44005",
    ("bedrock", "settings", "sessionToken", "title"): "000-44006",
    ("bedrock", "settings", "region", "title"): "000-44007",
}


def _localized_ai_services():
    """AVAILABLE_AI_SERVICESのdescription/settings[].titleをmulti_lang.get_textで多言語化したコピーを返す
    Return a copy of AVAILABLE_AI_SERVICES with description/settings[].title localized via multi_lang.get_text

    Returns:
        list[dict]
    """
    services = copy.deepcopy(AVAILABLE_AI_SERVICES)

    for service in services:
        service_id = service.get("ai_service_id")

        description_message_id = _AI_SERVICE_TEXT_MESSAGE_IDS.get((service_id, "description"))
        if description_message_id:
            service["description"] = multi_lang.get_text(description_message_id, service["description"])

        for setting_key, setting in service.get("settings", {}).items():
            title_message_id = _AI_SERVICE_TEXT_MESSAGE_IDS.get(
                (service_id, "settings", setting_key, "title")
            )
            if title_message_id:
                setting["title"] = multi_lang.get_text(title_message_id, setting["title"])

    return services


@common.platform_exception_handler
@require_ai_assistant_driver
def get_ai_services(organization_id):
    """
    システムとして利用可能なAIサービス一覧を取得

    :param organization_id:
    :type organization_id: str

    :rtype: dict
    """
    globals.logger.info(f"### func:{inspect.currentframe().f_code.co_name}")

    services = _localized_ai_services()

    return common.response_200_ok(
        {
            "ai_services": services,
            "count": len(services),
        }
    )


@common.platform_exception_handler
@require_ai_assistant_driver
def create_conversation(body, organization_id, workspace_id):
    """
    会話を作成

    :param body:
    :type body: dict
    :param organization_id:
    :type organization_id: str
    :param workspace_id:
    :type workspace_id: str

    :rtype: dict
    """
    globals.logger.info(f"### func:{inspect.currentframe().f_code.co_name}")

    r = connexion.request
    user_id = r.headers.get("User-id")

    body = r.get_json()
    title = body.get("title")
    model_id = body.get("model_id")
    ai_service_id = body.get("ai_service_id")
    prompt_profile = body.get("prompt_profile", "LLMEditor")
    tools = body.get("tools")  # ツール定義（Anthropic tools形式の配列、任意）

    # バリデーション（共通のvalidationモジュールを使用）
    validate = validation.validate_conversation_title(title)
    if not validate.ok:
        return common.response_validation_error(validate)

    # completionsでmodel_idを省略した際のデフォルトとして使うため、会話作成時に必須とする
    # Required at conversation creation time, since it becomes the default used when model_id is omitted in completions
    validate = validation.validate_conversation_model_id(model_id)
    if not validate.ok:
        return common.response_validation_error(validate)

    # どのAIサービスを使うかを明確化するため必須とする（自動推定はしない）
    # Required to make explicit which AI service is used (no auto-detection)
    validate = validation.validate_conversation_ai_service_id(ai_service_id)
    if not validate.ok:
        return common.response_validation_error(validate)

    validate = validation.validate_conversation_tools(tools)
    if not validate.ok:
        return common.response_validation_error(validate)

    try:
        service = get_conversation_service()

        conversation_id = service.create_conversation(
            organization_id=organization_id,
            workspace_id=workspace_id,
            user_id=user_id,
            title=title,
            model_id=model_id,
            ai_service_id=ai_service_id,
            prompt_profile=prompt_profile,
            tools=tools,
        )

        # 作成された会話を取得してAI_SERVICE_ID/MODEL_ID/TOOLSを含む完全な情報を返す
        with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    """
                    SELECT CONVERSATION_ID, PROMPT_PROFILE, AI_SERVICE_ID, MODEL_ID, TOOLS, TITLE, STATUS
                    FROM T_CHAT_CONVERSATION
                    WHERE CONVERSATION_ID = %s
                    """,
                    (conversation_id,),
                )
                conversation = cursor.fetchone()

        globals.logger.debug(
            f"Conversation created: id={conversation_id}, "
            f"prompt_profile={prompt_profile}, ai_service={conversation['AI_SERVICE_ID']}, model={conversation['MODEL_ID']}, "
            f"org={organization_id}, workspace={workspace_id}, user={user_id}"
        )

        return common.response_200_ok(
            {
                "conversation_id": conversation_id,
                "prompt_profile": conversation["PROMPT_PROFILE"],
                "ai_service_id": conversation["AI_SERVICE_ID"],
                "model_id": conversation["MODEL_ID"],
                "tools": json.loads(conversation["TOOLS"]) if conversation["TOOLS"] else [],
                "title": title,
                "status": conversation["STATUS"],
            }
        )

    except CredentialNotFound:
        # 指定したai_service_idのactiveなCredentialが未登録
        # No active credential registered for the specified ai_service_id
        message_id = "404-44001"
        message = multi_lang.get_text(
            message_id,
            "指定したai_service_idのCredentialが登録されていません: {}",
            ai_service_id
        )
        raise common.NotFoundException(message_id=message_id, message=message)

    except Exception as e:
        globals.logger.error(f"Failed to create conversation: {e}", exc_info=True)
        message_id = "500-44008"
        message = multi_lang.get_text(
            message_id,
            "会話作成に失敗しました: {}",
            str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)


@common.platform_exception_handler
@require_ai_assistant_driver
def list_conversations(organization_id, workspace_id, prompt_profile, status=None, limit=50, offset=0):
    """
    会話一覧を取得

    :param organization_id:
    :type organization_id: str
    :param workspace_id:
    :type workspace_id: str
    :param prompt_profile:
    :type prompt_profile: str
    :param status:
    :type status: str
    :param limit:
    :type limit: int
    :param offset:
    :type offset: int

    :rtype: dict
    """
    globals.logger.info(f"### func:{inspect.currentframe().f_code.co_name}")

    r = connexion.request
    user_id = r.headers.get("User-id")

    try:
        service = get_conversation_service()

        conversations, total_count = service.list_conversations(
            organization_id=organization_id,
            workspace_id=workspace_id,
            user_id=user_id,
            prompt_profile=prompt_profile,
            status=status,
            limit=limit,
            offset=offset,
        )

        # レスポンス用に整形
        conversations_data = []
        for conv in conversations:
            conversations_data.append({
                "conversation_id": conv["CONVERSATION_ID"],
                "prompt_profile": conv["PROMPT_PROFILE"],
                "ai_service_id": conv["AI_SERVICE_ID"],
                "model_id": conv["MODEL_ID"],
                "title": conv["TITLE"],
                "status": conv["STATUS"],
                "current_token_count": conv["CURRENT_TOKEN_COUNT"] or 0,
                "message_count": conv.get("MESSAGE_COUNT", 0),
                "created_at": conv["CREATE_TIMESTAMP"].isoformat() if conv["CREATE_TIMESTAMP"] else None,
                "updated_at": conv["LAST_UPDATE_TIMESTAMP"].isoformat() if conv["LAST_UPDATE_TIMESTAMP"] else None,
            })

        return common.response_200_ok(
            {
                "conversations": conversations_data,
                "count": len(conversations_data),
                "total_count": total_count,
            }
        )

    except Exception as e:
        globals.logger.error(f"Failed to list conversations: {e}", exc_info=True)
        message_id = "500-44009"
        message = multi_lang.get_text(
            message_id,
            "会話一覧取得に失敗しました: {}",
            str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)


@common.platform_exception_handler
@require_ai_assistant_driver
def create_completion(body, conversation_id, organization_id, workspace_id):
    """
    AI応答を生成（会話を1ターン進める）

    :param body:
    :type body: dict
    :param conversation_id:
    :type conversation_id: str
    :param organization_id:
    :type organization_id: str
    :param workspace_id:
    :type workspace_id: str

    :rtype: dict
    """
    globals.logger.info(f"### func:{inspect.currentframe().f_code.co_name}")

    r = connexion.request
    user_id = r.headers.get("User-id")

    body = r.get_json()
    # message省略時は、会話の既存履歴(T_CHAT_MESSAGE)のみでAIに問い合わせる（結果は保存しない）
    message_text = body.get("message")
    ai_service_id = body.get("ai_service_id")  # メッセージ固有のAIサービスID（任意、会話のデフォルトをオーバーライド）
    model_id = body.get("model_id")  # メッセージ固有のモデルID（任意、省略時は会話作成時に保存したデフォルトを使用）
    menu_id = body.get("menu_id")  # ITA画面ID（任意）

    try:
        service = get_conversation_service()

        # ユーザー言語を取得 (Accept-Languageヘッダーから)
        # Determine the user's language from the Accept-Language header
        user_language = None
        accept_language = connexion.request.headers.get('Accept-Language', '')
        # "ja"/"jp"を含む部分一致で判定（"ja-JP"等の地域付き表記もカバーするため）。該当しなければenを見る
        # Match by substring on "ja"/"jp" (to also cover region variants like "ja-JP"); fall back to checking for en
        if 'ja' in accept_language or 'jp' in accept_language:
            user_language = 'jp'
        elif 'en' in accept_language:
            user_language = 'en'

        globals.logger.debug(
            f"User language detected: {user_language} (Accept-Language: {accept_language}), "
            f"ai_service_id: {ai_service_id}, menu_id: {menu_id}"
        )

        result = service.create_completion(
            organization_id=organization_id,
            workspace_id=workspace_id,
            user_id=user_id,
            conversation_id=conversation_id,
            message_text=message_text,
            ai_service_id=ai_service_id,
            model_id=model_id,
            user_language=user_language,
            menu_id=menu_id,
        )

        globals.logger.debug(
            f"Completion created: conv={conversation_id}, "
            f"workspace={workspace_id}, "
            f"saved={result['saved']}, "
            f"message_id={result['message_id']}, "
            f"user_seq={result['user_message_seq']}, "
            f"assistant_seq={result['assistant_message_seq']}"
        )

        return common.response_200_ok(result)

    except ConversationNotFound:
        message_id = "404-44002"
        message = multi_lang.get_text(
            message_id,
            "会話が見つかりません"
        )
        raise common.NotFoundException(message_id=message_id, message=message)

    except common.BadRequestException:
        # サービス層で判定したバリデーションエラー（message省略時の会話状態チェック等）を500に潰さずそのまま伝播させる
        # Re-raise validation errors detected in the service layer (e.g. conversation-state checks when message is omitted) instead of collapsing them into 500
        raise

    except common.OtherException:
        # AIサービスが返した実際のHTTPステータスコードを500に潰さずそのまま伝播させる（呼び出し元でリトライ判断に使うため）
        # Re-raise the actual HTTP status code returned by the AI service instead of collapsing it into 500 (the caller uses it for retry decisions)
        raise

    except Exception as e:
        globals.logger.error(f"Failed to create completion: {e}", exc_info=True)
        message_id = "500-44010"
        message = multi_lang.get_text(
            message_id,
            "AI応答の生成に失敗しました: {}",
            str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)


@common.platform_exception_handler
@require_ai_assistant_driver
def create_message(conversation_id, organization_id, workspace_id):
    """
    会話メッセージを作成

    Args:
        conversation_id: Conversation ID
        organization_id: Organization ID
        workspace_id: Workspace ID

    Returns:
        作成したメッセージレコード
    """
    globals.logger.info(f"### func:create_message")

    user_id = connexion.request.headers.get('User-Id')
    body = connexion.request.get_json()

    # バリデーション（共通のvalidationモジュールを使用）：contentsフィールド（JSON配列）が必須
    validate = validation.validate_message_contents(body.get('contents'))
    if not validate.ok:
        return common.response_validation_error(validate)

    try:
        service = get_message_service()

        result = service.create_message(
            organization_id=organization_id,
            workspace_id=workspace_id,
            user_id=user_id,
            conversation_id=conversation_id,
            contents=body['contents'],
        )

        globals.logger.debug(
            f"Message created: conv={conversation_id}, "
            f"message_id={result['message_id']}, "
            f"seq={result['message_seq']}"
        )

        return common.response_200_ok(result)

    except ValueError as e:
        message_id = "404-44003"
        message = multi_lang.get_text(
            message_id,
            f"会話が見つかりません: {str(e)}"
        )
        raise common.NotFoundException(message_id=message_id, message=message)

    except Exception as e:
        globals.logger.error(f"Failed to create message: {e}", exc_info=True)
        message_id = "500-44011"
        message = multi_lang.get_text(
            message_id,
            "メッセージ作成に失敗しました: {}",
            str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)


@common.platform_exception_handler
@require_ai_assistant_driver
def list_messages(conversation_id, organization_id, workspace_id, limit=100, offset=0):
    """
    会話メッセージ一覧を取得

    Args:
        conversation_id: Conversation ID
        organization_id: Organization ID
        workspace_id: Workspace ID
        limit: 取得件数
        offset: オフセット

    Returns:
        メッセージ一覧
    """
    globals.logger.info(f"### func:list_messages")

    user_id = connexion.request.headers.get('User-Id')

    try:
        service = get_message_service()

        messages = service.list_messages(
            organization_id=organization_id,
            workspace_id=workspace_id,
            user_id=user_id,
            conversation_id=conversation_id,
            limit=limit,
            offset=offset,
        )

        globals.logger.debug(
            f"Listed {len(messages)} messages: conv={conversation_id}"
        )

        return common.response_200_ok({
            "messages": messages,
            "count": len(messages),
            "conversation_id": conversation_id,
        })

    except ValueError as e:
        message_id = "404-44004"
        message = multi_lang.get_text(
            message_id,
            f"会話が見つかりません: {str(e)}"
        )
        raise common.NotFoundException(message_id=message_id, message=message)

    except Exception as e:
        globals.logger.error(f"Failed to list messages: {e}", exc_info=True)
        message_id = "500-44012"
        message = multi_lang.get_text(
            message_id,
            "メッセージ一覧取得に失敗しました: {}",
            str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)


@common.platform_exception_handler
@require_ai_assistant_driver
def replace_messages(conversation_id, organization_id, workspace_id):
    """
    会話メッセージを全置き換え

    GETで取得できる内容をそのまま置き換えるイメージ。既存のメッセージは全て削除され、
    リクエストで指定した内容に入れ替わる。

    Args:
        conversation_id: Conversation ID
        organization_id: Organization ID
        workspace_id: Workspace ID

    Returns:
        置き換え後のメッセージ一覧
    """
    globals.logger.info(f"### func:replace_messages")

    user_id = connexion.request.headers.get('User-Id')
    body = connexion.request.get_json()

    # バリデーション（共通のvalidationモジュールを使用）：messagesフィールド（JSON配列）が必須。
    # 各要素はcontentsキーを持つオブジェクトである必要がある（GETのレスポンス形式に合わせる）
    # Each element of messages must be an object with a contents key (matches the GET response shape)
    validate = validation.validate_messages(body.get('messages'))
    if not validate.ok:
        return common.response_validation_error(validate)

    # 各要素のcontents（JSON配列）を取り出す
    # Extract each element's contents (JSON array)
    contents_list = [item['contents'] for item in body['messages']]

    try:
        service = get_message_service()

        messages = service.replace_messages(
            organization_id=organization_id,
            workspace_id=workspace_id,
            user_id=user_id,
            conversation_id=conversation_id,
            messages=contents_list,
        )

        globals.logger.debug(
            f"Replaced messages: conv={conversation_id}, count={len(messages)}"
        )

        return common.response_200_ok({
            "messages": messages,
            "count": len(messages),
            "conversation_id": conversation_id,
        })

    except ValueError as e:
        message_id = "404-44005"
        message = multi_lang.get_text(
            message_id,
            f"会話が見つかりません: {str(e)}"
        )
        raise common.NotFoundException(message_id=message_id, message=message)

    except Exception as e:
        globals.logger.error(f"Failed to replace messages: {e}", exc_info=True)
        message_id = "500-44013"
        message = multi_lang.get_text(
            message_id,
            "メッセージの置き換えに失敗しました: {}",
            str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)


@common.platform_exception_handler
@require_ai_assistant_driver
def delete_messages(conversation_id, organization_id, workspace_id):
    """
    会話メッセージを全削除

    Args:
        conversation_id: Conversation ID
        organization_id: Organization ID
        workspace_id: Workspace ID

    Returns:
        削除結果
    """
    globals.logger.info(f"### func:delete_messages")

    user_id = connexion.request.headers.get('User-Id')

    try:
        service = get_message_service()

        deleted_count = service.delete_messages(
            organization_id=organization_id,
            workspace_id=workspace_id,
            user_id=user_id,
            conversation_id=conversation_id,
        )

        globals.logger.debug(
            f"Deleted messages: conv={conversation_id}, count={deleted_count}"
        )

        return common.response_200_ok({
            "conversation_id": conversation_id,
            "deleted_count": deleted_count,
        })

    except ValueError as e:
        message_id = "404-44006"
        message = multi_lang.get_text(
            message_id,
            f"会話が見つかりません: {str(e)}"
        )
        raise common.NotFoundException(message_id=message_id, message=message)

    except Exception as e:
        globals.logger.error(f"Failed to delete messages: {e}", exc_info=True)
        message_id = "500-44014"
        message = multi_lang.get_text(
            message_id,
            "メッセージの削除に失敗しました: {}",
            str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)
