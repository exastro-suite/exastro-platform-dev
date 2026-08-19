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
User Credential Service Controller

ユーザーが手動でAWS Credentialを登録・管理するAPI
"""

from flask import request
import connexion
import inspect
from datetime import datetime

from common_library.common import common, multi_lang
from services.ai_assistant.user_manual_credential_service import (
    get_manual_credential_service,
    CredentialNotFound,
    CredentialValidationError,
)

import globals


MSG_FUNCTION_ID = "91"  # User Credential用のFunction ID


@common.platform_exception_handler
def register_aws_credential(body, organization_id):
    """
    AWS Credentialを登録

    :param body:
    :type body: dict
    :param organization_id:
    :type organization_id: str

    :rtype: dict
    """
    globals.logger.info(f"### func:{inspect.currentframe().f_code.co_name}")

    r = connexion.request
    user_id = r.headers.get("User-id")

    body = r.get_json()
    credential_name = body.get("credential_name")
    access_key_id = body.get("access_key_id")
    secret_access_key = body.get("secret_access_key")
    session_token = body.get("session_token")
    aws_region = body.get("aws_region", "ap-northeast-1")
    bedrock_region = body.get("bedrock_region", "ap-northeast-1")
    expires_at_str = body.get("expires_at")
    notes = body.get("notes")

    # バリデーション
    if not credential_name or not access_key_id or not secret_access_key:
        message_id = f"400-{MSG_FUNCTION_ID}001"
        message = multi_lang.get_text(
            message_id,
            "credential_name, access_key_id, secret_access_keyは必須です"
        )
        raise common.BadRequestException(message_id=message_id, message=message)

    # 有効期限のパース
    expires_at = None
    if expires_at_str:
        try:
            expires_at = datetime.fromisoformat(expires_at_str.replace('Z', '+00:00'))
        except ValueError:
            message_id = f"400-{MSG_FUNCTION_ID}002"
            message = multi_lang.get_text(
                message_id,
                "expires_atの形式が不正です (ISO 8601形式を使用してください)"
            )
            raise common.BadRequestException(message_id=message_id, message=message)

    try:
        service = get_manual_credential_service()

        credential_id = service.register_credential(
            organization_id=organization_id,
            user_id=user_id,
            credential_name=credential_name,
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            session_token=session_token,
            aws_region=aws_region,
            bedrock_region=bedrock_region,
            expires_at=expires_at,
            notes=notes,
        )

        globals.logger.info(
            f"AWS Credential registered: id={credential_id}, "
            f"org={organization_id}, user={user_id}"
        )

        return common.response_200_ok(
            {
                "credential_id": credential_id,
                "credential_name": credential_name,
                "status": "active",
                "message": "AWS Credential registered successfully",
            }
        )

    except CredentialValidationError as e:
        message_id = f"400-{MSG_FUNCTION_ID}003"
        message = multi_lang.get_text(
            message_id,
            "Credentialの検証に失敗しました: {}",
            str(e)
        )
        raise common.BadRequestException(message_id=message_id, message=message)

    except Exception as e:
        globals.logger.error(f"Failed to register credential: {e}", exc_info=True)
        message_id = "500-94201"
        message = multi_lang.get_text(
            message_id,
            "Credential登録に失敗しました: {}",
            str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)


@common.platform_exception_handler
def list_aws_credentials(organization_id):
    """
    AWS Credential一覧を取得

    :param organization_id:
    :type organization_id: str

    :rtype: dict
    """
    globals.logger.info(f"### func:{inspect.currentframe().f_code.co_name}")

    r = connexion.request
    user_id = r.headers.get("User-id")

    status = request.args.get("status")

    try:
        service = get_manual_credential_service()

        credentials = service.list_credentials(
            organization_id=organization_id,
            user_id=user_id,
            status=status,
        )

        # レスポンス用に整形（平文Credentialは含まない）
        credentials_data = []
        for cred in credentials:
            credentials_data.append({
                "credential_id": cred["CREDENTIAL_ID"],
                "credential_name": cred["CREDENTIAL_NAME"],
                "aws_region": cred["AWS_REGION"],
                "bedrock_region": cred["BEDROCK_REGION"],
                "status": cred["STATUS"],
                "expires_at": cred["EXPIRES_AT"].isoformat() if cred["EXPIRES_AT"] else None,
                "last_validated_at": cred["LAST_VALIDATED_AT"].isoformat() if cred["LAST_VALIDATED_AT"] else None,
                "last_used_at": cred["LAST_USED_AT"].isoformat() if cred["LAST_USED_AT"] else None,
                "notes": cred["NOTES"],
                "created_at": cred["CREATE_TIMESTAMP"].isoformat(),
            })

        return common.response_200(
            {
                "credentials": credentials_data,
                "count": len(credentials_data),
            }
        )

    except Exception as e:
        globals.logger.error(f"Failed to list credentials: {e}", exc_info=True)
        message_id = "500-94202"
        message = multi_lang.get_text(
            message_id,
            "Credential一覧取得に失敗しました: {}",
            str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)


@common.platform_exception_handler
def validate_aws_credential(credential_id, organization_id):
    """
    AWS Credentialを検証

    :param credential_id:
    :type credential_id: str
    :param organization_id:
    :type organization_id: str

    :rtype: dict
    """
    globals.logger.info(f"### func:{inspect.currentframe().f_code.co_name}")

    r = connexion.request
    user_id = r.headers.get("User-id")

    try:
        service = get_manual_credential_service()

        result = service.validate_credential(
            organization_id=organization_id,
            user_id=user_id,
            credential_id=credential_id,
        )

        return common.response_200(
            {
                "credential_id": credential_id,
                "valid": result["valid"],
                "identity": result.get("identity"),
                "error": result.get("error"),
            }
        )

    except CredentialNotFound as e:
        message_id = f"404-{MSG_FUNCTION_ID}006"
        message = multi_lang.get_text(
            message_id,
            "Credentialが見つかりません"
        )
        raise common.NotFoundException(message_id=message_id, message=message)

    except Exception as e:
        globals.logger.error(f"Failed to validate credential: {e}", exc_info=True)
        message_id = "500-94203"
        message = multi_lang.get_text(
            message_id,
            "Credential検証に失敗しました: {}",
            str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)


@common.platform_exception_handler
def delete_aws_credential(credential_id, organization_id):
    """
    AWS Credentialを削除

    :param credential_id:
    :type credential_id: str
    :param organization_id:
    :type organization_id: str

    :rtype: dict
    """
    globals.logger.info(f"### func:{inspect.currentframe().f_code.co_name}")

    r = connexion.request
    user_id = r.headers.get("User-id")

    try:
        service = get_manual_credential_service()

        service.delete_credential(
            organization_id=organization_id,
            user_id=user_id,
            credential_id=credential_id,
        )

        return common.response_200(
            {
                "credential_id": credential_id,
                "message": "Credential deleted successfully",
            }
        )

    except Exception as e:
        globals.logger.error(f"Failed to delete credential: {e}", exc_info=True)
        message_id = "500-94204"
        message = multi_lang.get_text(
            message_id,
            "Credential削除に失敗しました: {}",
            str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)
