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
import inspect
from contextlib import closing

from common_library.common import common, multi_lang
from common_library.common.db import DBconnector
from services.ai_assistant.conversation_service import (
    get_conversation_service,
    ConversationNotFound,
)
from services.ai_assistant.message_service import get_message_service

import globals


@common.platform_exception_handler
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
    service_id = body.get("service_id", "LLMEditor")

    # バリデーション
    if not title:
        message_id = "400-94001"
        message = multi_lang.get_text(
            message_id,
            "titleは必須です"
        )
        raise common.BadRequestException(message_id=message_id, message=message)

    try:
        service = get_conversation_service()

        conversation_id = service.create_conversation(
            organization_id=organization_id,
            workspace_id=workspace_id,
            user_id=user_id,
            title=title,
            service_id=service_id,
        )

        # 作成された会話を取得してAI_SERVICE_IDを含む完全な情報を返す
        with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    """
                    SELECT CONVERSATION_ID, SERVICE_ID, AI_SERVICE_ID, TITLE, STATUS
                    FROM T_CHAT_CONVERSATION
                    WHERE CONVERSATION_ID = %s
                    """,
                    (conversation_id,),
                )
                conversation = cursor.fetchone()

        globals.logger.debug(
            f"Conversation created: id={conversation_id}, "
            f"service={service_id}, ai_service={conversation['AI_SERVICE_ID']}, "
            f"org={organization_id}, workspace={workspace_id}, user={user_id}"
        )

        return common.response_200_ok(
            {
                "conversation_id": conversation_id,
                "service_id": conversation["SERVICE_ID"],
                "ai_service_id": conversation["AI_SERVICE_ID"],
                "title": title,
                "status": conversation["STATUS"],
            }
        )

    except Exception as e:
        globals.logger.error(f"Failed to create conversation: {e}", exc_info=True)
        message_id = "500-94101"
        message = multi_lang.get_text(
            message_id,
            "会話作成に失敗しました: {}",
            str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)


@common.platform_exception_handler
def list_conversations(organization_id, workspace_id, status=None, limit=50, offset=0):
    """
    会話一覧を取得

    :param organization_id:
    :type organization_id: str
    :param workspace_id:
    :type workspace_id: str
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

        conversations = service.list_conversations(
            organization_id=organization_id,
            workspace_id=workspace_id,
            user_id=user_id,
            status=status,
            limit=limit,
            offset=offset,
        )

        # レスポンス用に整形
        conversations_data = []
        for conv in conversations:
            conversations_data.append({
                "conversation_id": conv["CONVERSATION_ID"],
                "service_id": conv["SERVICE_ID"],
                "ai_service_id": conv["AI_SERVICE_ID"],
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
                "total_count": len(conversations_data),  # TODO: 実装改善時に総件数を取得
            }
        )

    except Exception as e:
        globals.logger.error(f"Failed to list conversations: {e}", exc_info=True)
        message_id = "500-94102"
        message = multi_lang.get_text(
            message_id,
            "会話一覧取得に失敗しました: {}",
            str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)


@common.platform_exception_handler
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
    model_id = body.get("model_id", "anthropic.claude-3-5-sonnet-20240620-v1:0")
    menu_id = body.get("menu_id")  # ITA画面ID（任意）

    try:
        service = get_conversation_service()

        # ユーザー言語を取得 (Accept-Languageヘッダーから)
        user_language = None
        accept_language = connexion.request.headers.get('Accept-Language', '')
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
        message_id = "404-94007"
        message = multi_lang.get_text(
            message_id,
            "会話が見つかりません"
        )
        raise common.NotFoundException(message_id=message_id, message=message)

    except common.BadRequestException:
        # サービス層で判定したバリデーションエラー（message省略時の会話状態チェック等）はそのまま伝播する
        raise

    except Exception as e:
        globals.logger.error(f"Failed to create completion: {e}", exc_info=True)
        message_id = "500-94104"
        message = multi_lang.get_text(
            message_id,
            "AI応答の生成に失敗しました: {}",
            str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)


@common.platform_exception_handler
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

    # バリデーション：contentsフィールド（JSON配列）が必須
    if 'contents' not in body:
        message_id = "400-94201"
        message = multi_lang.get_text(
            message_id,
            "必須フィールドが不足しています: contents"
        )
        raise common.BadRequestException(message_id=message_id, message=message)

    # contentsが配列であることを確認
    if not isinstance(body['contents'], list):
        message_id = "400-94202"
        message = multi_lang.get_text(
            message_id,
            "contentsはJSON配列である必要があります"
        )
        raise common.BadRequestException(message_id=message_id, message=message)

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
        message_id = "404-94203"
        message = multi_lang.get_text(
            message_id,
            f"会話が見つかりません: {str(e)}"
        )
        raise common.NotFoundException(message_id=message_id, message=message)

    except Exception as e:
        globals.logger.error(f"Failed to create message: {e}", exc_info=True)
        message_id = "500-94204"
        message = multi_lang.get_text(
            message_id,
            "メッセージ作成に失敗しました: {}",
            str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)


@common.platform_exception_handler
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
        message_id = "404-94204"
        message = multi_lang.get_text(
            message_id,
            f"会話が見つかりません: {str(e)}"
        )
        raise common.NotFoundException(message_id=message_id, message=message)

    except Exception as e:
        globals.logger.error(f"Failed to list messages: {e}", exc_info=True)
        message_id = "500-94205"
        message = multi_lang.get_text(
            message_id,
            "メッセージ一覧取得に失敗しました: {}",
            str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)


@common.platform_exception_handler
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

    # バリデーション：messagesフィールド（JSON配列）が必須
    if 'messages' not in body:
        message_id = "400-94206"
        message = multi_lang.get_text(
            message_id,
            "必須フィールドが不足しています: messages"
        )
        raise common.BadRequestException(message_id=message_id, message=message)

    if not isinstance(body['messages'], list):
        message_id = "400-94207"
        message = multi_lang.get_text(
            message_id,
            "messagesはJSON配列である必要があります"
        )
        raise common.BadRequestException(message_id=message_id, message=message)

    # 各要素のcontents（JSON配列）を取り出す
    contents_list = []
    for item in body['messages']:
        if not isinstance(item, dict) or not isinstance(item.get('contents'), list):
            message_id = "400-94207"
            message = multi_lang.get_text(
                message_id,
                "messagesの各要素はcontents(JSON配列)を持つ必要があります"
            )
            raise common.BadRequestException(message_id=message_id, message=message)
        contents_list.append(item['contents'])

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
        message_id = "404-94208"
        message = multi_lang.get_text(
            message_id,
            f"会話が見つかりません: {str(e)}"
        )
        raise common.NotFoundException(message_id=message_id, message=message)

    except Exception as e:
        globals.logger.error(f"Failed to replace messages: {e}", exc_info=True)
        message_id = "500-94209"
        message = multi_lang.get_text(
            message_id,
            "メッセージの置き換えに失敗しました: {}",
            str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)


@common.platform_exception_handler
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
        message_id = "404-94210"
        message = multi_lang.get_text(
            message_id,
            f"会話が見つかりません: {str(e)}"
        )
        raise common.NotFoundException(message_id=message_id, message=message)

    except Exception as e:
        globals.logger.error(f"Failed to delete messages: {e}", exc_info=True)
        message_id = "500-94211"
        message = multi_lang.get_text(
            message_id,
            "メッセージの削除に失敗しました: {}",
            str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)
