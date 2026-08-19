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
Conversation Service Controller

チャット会話・メッセージ管理API
"""

import connexion
import inspect

from common_library.common import common, multi_lang
from services.ai_assistant.conversation_service import (
    get_conversation_service,
    ConversationNotFound,
)

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
        )

        globals.logger.info(
            f"Conversation created: id={conversation_id}, "
            f"org={organization_id}, workspace={workspace_id}, user={user_id}"
        )

        return common.response_200_ok(
            {
                "conversation_id": conversation_id,
                "title": title,
                "status": "active",
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
                "title": conv["TITLE"],
                "status": conv["STATUS"],
                "current_token_count": conv["CURRENT_TOKEN_COUNT"] or 0,
                "message_count": conv.get("MESSAGE_COUNT", 0),
                "created_at": conv["CREATE_TIMESTAMP"].isoformat() if conv["CREATE_TIMESTAMP"] else None,
                "updated_at": conv["LAST_UPDATE_TIMESTAMP"].isoformat() if conv["LAST_UPDATE_TIMESTAMP"] else None,
            })

        return common.response_200(
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
def list_messages(conversation_id, organization_id, workspace_id, limit=100, offset=0):
    """
    メッセージ一覧を取得

    :param conversation_id:
    :type conversation_id: str
    :param organization_id:
    :type organization_id: str
    :param workspace_id:
    :type workspace_id: str
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

        messages = service.list_messages(
            organization_id=organization_id,
            workspace_id=workspace_id,
            user_id=user_id,
            conversation_id=conversation_id,
            limit=limit,
            offset=offset,
        )

        # レスポンス用に整形
        messages_data = []
        for msg in messages:
            messages_data.append({
                "message_id": msg["MESSAGE_ID"],
                "conversation_id": msg["CONVERSATION_ID"],
                "message_seq": msg["MESSAGE_SEQ"],
                "role": msg["ROLE"],
                "message_text": msg["MESSAGE_TEXT"],
                "ai_service_id": msg.get("AI_SERVICE_ID"),
                "ai_model_id": msg.get("AI_MODEL_ID"),
                "token_count": msg.get("TOKEN_COUNT", 0),
                "created_at": msg["CREATE_TIMESTAMP"].isoformat() if msg["CREATE_TIMESTAMP"] else None,
            })

        return common.response_200(
            {
                "messages": messages_data,
                "count": len(messages_data),
                "conversation_id": conversation_id,
            }
        )

    except ConversationNotFound:
        message_id = "404-94004"
        message = multi_lang.get_text(
            message_id,
            "会話が見つかりません"
        )
        raise common.NotFoundException(message_id=message_id, message=message)

    except Exception as e:
        globals.logger.error(f"Failed to list messages: {e}", exc_info=True)
        message_id = "500-94103"
        message = multi_lang.get_text(
            message_id,
            "メッセージ一覧取得に失敗しました: {}",
            str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)


@common.platform_exception_handler
def send_message(body, conversation_id, organization_id, workspace_id):
    """
    メッセージを送信

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
    message_text = body.get("message")
    model_id = body.get("model_id", "anthropic.claude-3-5-sonnet-20240620-v1:0")
    ai_service_id = body.get("ai_service_id", "bedrock")

    # バリデーション
    if not message_text:
        message_id = "400-94006"
        message = multi_lang.get_text(
            message_id,
            "messageは必須です"
        )
        raise common.BadRequestException(message_id=message_id, message=message)

    try:
        service = get_conversation_service()

        result = service.send_message(
            organization_id=organization_id,
            workspace_id=workspace_id,
            user_id=user_id,
            conversation_id=conversation_id,
            message_text=message_text,
            model_id=model_id,
            ai_service_id=ai_service_id,
        )

        globals.logger.info(
            f"Message sent: conv={conversation_id}, "
            f"workspace={workspace_id}, "
            f"user_msg={result['user_message_id']}, "
            f"assistant_msg={result['assistant_message_id']}"
        )

        return common.response_200_ok(result)

    except ConversationNotFound:
        message_id = "404-94007"
        message = multi_lang.get_text(
            message_id,
            "会話が見つかりません"
        )
        raise common.NotFoundException(message_id=message_id, message=message)

    except Exception as e:
        globals.logger.error(f"Failed to send message: {e}", exc_info=True)
        message_id = "500-94104"
        message = multi_lang.get_text(
            message_id,
            "メッセージ送信に失敗しました: {}",
            str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)
