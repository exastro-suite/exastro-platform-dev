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
AI Credential Service Controller

汎用AIサービスのCredential管理API
"""

import connexion
import inspect

from common_library.common import common, multi_lang
from services.ai_assistant.ai_credential_service import (
    get_ai_credential_service,
    CredentialNotFound,
)
from services.ai_assistant.model_service import (
    get_model_service,
)

import globals


@common.platform_exception_handler
def register_credential(body, organization_id, ai_service_id):
    """
    Credentialを登録

    :param body:
    :type body: dict
    :param organization_id:
    :type organization_id: str
    :param ai_service_id:
    :type ai_service_id: str

    :rtype: dict
    """
    globals.logger.info(f"### func:{inspect.currentframe().f_code.co_name}")

    r = connexion.request
    user_id = r.headers.get("User-id")

    body = r.get_json()
    credential_name = body.get("credential_name")
    credential_data = body.get("credential_data")
    notes = body.get("notes")

    # バリデーション
    if not credential_name:
        message_id = "400-94001"
        message = multi_lang.get_text(message_id, "credential_nameは必須です")
        raise common.BadRequestException(message_id=message_id, message=message)

    if not credential_data or not isinstance(credential_data, dict):
        message_id = "400-94002"
        message = multi_lang.get_text(
            message_id, "credential_dataは必須でJSON形式である必要があります"
        )
        raise common.BadRequestException(message_id=message_id, message=message)

    # aws-cache の特別処理
    if ai_service_id == "aws-cache":
        # キャッシュファイルの内容が渡されているか確認
        if "idToken" not in credential_data:
            message_id = "400-94014"
            message = multi_lang.get_text(
                message_id,
                "aws-cache requires full cache file content including idToken. "
                "Please pass the entire content of ~/.aws/login/cache/*.json file."
            )
            raise common.BadRequestException(message_id=message_id, message=message)

        if not notes:
            notes = "AWS Login Cache (automatic token refresh)"

    try:
        service = get_ai_credential_service()

        credential_id = service.register_credential(
            organization_id=organization_id,
            user_id=user_id,
            ai_service_id=ai_service_id,
            credential_name=credential_name,
            credential_data=credential_data,
            notes=notes,
        )

        globals.logger.info(
            f"AI Credential registered: id={credential_id}, "
            f"service={ai_service_id}, org={organization_id}, user={user_id}"
        )

        return common.response_200_ok(
            {
                "credential_id": credential_id,
                "ai_service_id": ai_service_id,
                "credential_name": credential_name,
                "status": "active",
                "message": "Credential registered successfully",
            }
        )

    except Exception as e:
        globals.logger.error(f"Failed to register credential: {e}", exc_info=True)
        message_id = "500-94001"
        message = multi_lang.get_text(
            message_id, "Credential登録に失敗しました: {}", str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)


@common.platform_exception_handler
def list_credentials(organization_id, ai_service_id, status=None):
    """
    Credential一覧を取得

    :param organization_id:
    :type organization_id: str
    :param ai_service_id:
    :type ai_service_id: str
    :param status:
    :type status: str

    :rtype: dict
    """
    globals.logger.info(f"### func:{inspect.currentframe().f_code.co_name}")

    r = connexion.request
    user_id = r.headers.get("User-id")

    try:
        service = get_ai_credential_service()

        credentials = service.list_credentials(
            organization_id=organization_id,
            user_id=user_id,
            ai_service_id=ai_service_id,
            status=status,
        )

        # レスポンス用に整形
        credentials_data = []
        for cred in credentials:
            credentials_data.append(
                {
                    "credential_id": cred["CREDENTIAL_ID"],
                    "ai_service_id": cred["AI_SERVICE_ID"],
                    "credential_name": cred["CREDENTIAL_NAME"],
                    "status": cred["STATUS"],
                    "expires_at": (
                        cred["EXPIRES_AT"].isoformat() if cred["EXPIRES_AT"] else None
                    ),
                    "last_validated_at": (
                        cred["LAST_VALIDATED_AT"].isoformat()
                        if cred["LAST_VALIDATED_AT"]
                        else None
                    ),
                    "last_used_at": (
                        cred["LAST_USED_AT"].isoformat()
                        if cred["LAST_USED_AT"]
                        else None
                    ),
                    "validation_error": cred["VALIDATION_ERROR"],
                    "notes": cred["NOTES"],
                    "created_at": (
                        cred["CREATE_TIMESTAMP"].isoformat()
                        if cred["CREATE_TIMESTAMP"]
                        else None
                    ),
                    "updated_at": (
                        cred["LAST_UPDATE_TIMESTAMP"].isoformat()
                        if cred["LAST_UPDATE_TIMESTAMP"]
                        else None
                    ),
                }
            )

        return common.response_200(
            {
                "credentials": credentials_data,
                "count": len(credentials_data),
                "ai_service_id": ai_service_id,
            }
        )

    except Exception as e:
        globals.logger.error(f"Failed to list credentials: {e}", exc_info=True)
        message_id = "500-94002"
        message = multi_lang.get_text(
            message_id, "Credential一覧取得に失敗しました: {}", str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)


@common.platform_exception_handler
def get_credential(organization_id, ai_service_id, credential_id):
    """
    Credential詳細を取得

    :param organization_id:
    :type organization_id: str
    :param ai_service_id:
    :type ai_service_id: str
    :param credential_id:
    :type credential_id: str

    :rtype: dict
    """
    globals.logger.info(f"### func:{inspect.currentframe().f_code.co_name}")

    r = connexion.request
    user_id = r.headers.get("User-id")

    try:
        service = get_ai_credential_service()

        credential = service.get_credential(
            organization_id=organization_id,
            user_id=user_id,
            ai_service_id=ai_service_id,
            credential_id=credential_id,
        )

        # Credentialデータはマスク（セキュリティ上、詳細は返さない）
        return common.response_200(
            {
                "credential_id": credential.credential_id,
                "ai_service_id": credential.ai_service_id,
                "credential_name": credential.credential_name,
                "status": credential.status,
                "expires_at": (
                    credential.expires_at.isoformat() if credential.expires_at else None
                ),
                "last_used_at": (
                    credential.last_used_at.isoformat()
                    if credential.last_used_at
                    else None
                ),
                "credential_data_keys": list(credential.credential_data.keys()),
            }
        )

    except CredentialNotFound:
        message_id = "404-94005"
        message = multi_lang.get_text(message_id, "Credentialが見つかりません")
        raise common.NotFoundException(message_id=message_id, message=message)

    except Exception as e:
        globals.logger.error(f"Failed to get credential: {e}", exc_info=True)
        message_id = "500-94003"
        message = multi_lang.get_text(
            message_id, "Credential取得に失敗しました: {}", str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)


@common.platform_exception_handler
def delete_credential(organization_id, ai_service_id, credential_id):
    """
    Credentialを削除

    :param organization_id:
    :type organization_id: str
    :param ai_service_id:
    :type ai_service_id: str
    :param credential_id:
    :type credential_id: str

    :rtype: dict
    """
    globals.logger.info(f"### func:{inspect.currentframe().f_code.co_name}")

    r = connexion.request
    user_id = r.headers.get("User-id")

    try:
        service = get_ai_credential_service()

        deleted = service.delete_credential(
            organization_id=organization_id,
            user_id=user_id,
            ai_service_id=ai_service_id,
            credential_id=credential_id,
        )

        if not deleted:
            message_id = "404-94007"
            message = multi_lang.get_text(message_id, "Credentialが見つかりません")
            raise common.NotFoundException(message_id=message_id, message=message)

        globals.logger.info(
            f"AI Credential deleted: id={credential_id}, "
            f"service={ai_service_id}, org={organization_id}, user={user_id}"
        )

        return common.response_200_ok(
            {
                "credential_id": credential_id,
                "message": "Credential deleted successfully",
            }
        )

    except common.NotFoundException:
        raise

    except Exception as e:
        globals.logger.error(f"Failed to delete credential: {e}", exc_info=True)
        message_id = "500-94004"
        message = multi_lang.get_text(
            message_id, "Credential削除に失敗しました: {}", str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)


@common.platform_exception_handler
def update_credential(body, organization_id, ai_service_id, credential_id):
    """
    Credentialを更新（部分更新）

    :param body:
    :type body: dict
    :param organization_id:
    :type organization_id: str
    :param ai_service_id:
    :type ai_service_id: str
    :param credential_id:
    :type credential_id: str

    :rtype: dict
    """
    globals.logger.info(f"### func:{inspect.currentframe().f_code.co_name}")

    r = connexion.request
    user_id = r.headers.get("User-id")

    body = r.get_json()
    credential_name = body.get("credential_name")
    credential_data = body.get("credential_data")
    notes = body.get("notes")

    # 少なくとも1つのフィールドが必要
    if not any([credential_name, credential_data, notes]):
        message_id = "400-94015"
        message = multi_lang.get_text(
            message_id, "更新するフィールドを指定してください（credential_name, credential_data, notes のいずれか）"
        )
        raise common.BadRequestException(message_id=message_id, message=message)

    # credential_dataのバリデーション
    if credential_data is not None:
        if not isinstance(credential_data, dict):
            message_id = "400-94016"
            message = multi_lang.get_text(
                message_id, "credential_dataはJSON形式である必要があります"
            )
            raise common.BadRequestException(message_id=message_id, message=message)

        # aws-cache の特別処理
        if ai_service_id == "aws-cache":
            if "idToken" not in credential_data:
                message_id = "400-94017"
                message = multi_lang.get_text(
                    message_id,
                    "aws-cache requires full cache file content including idToken. "
                    "Please pass the entire content of ~/.aws/login/cache/*.json file."
                )
                raise common.BadRequestException(message_id=message_id, message=message)

    try:
        service = get_ai_credential_service()

        updated = service.update_credential(
            organization_id=organization_id,
            user_id=user_id,
            ai_service_id=ai_service_id,
            credential_id=credential_id,
            credential_name=credential_name,
            credential_data=credential_data,
            notes=notes,
        )

        if not updated:
            message_id = "404-94018"
            message = multi_lang.get_text(message_id, "Credentialが見つかりません")
            raise common.NotFoundException(message_id=message_id, message=message)

        globals.logger.info(
            f"AI Credential updated: id={credential_id}, "
            f"service={ai_service_id}, org={organization_id}, user={user_id}"
        )

        # 更新後の情報を取得
        credential = service.get_credential(
            organization_id=organization_id,
            user_id=user_id,
            ai_service_id=ai_service_id,
            credential_id=credential_id,
        )

        return common.response_200_ok(
            {
                "credential_id": credential.credential_id,
                "ai_service_id": credential.ai_service_id,
                "credential_name": credential.credential_name,
                "status": credential.status,
                "message": "Credential updated successfully",
            }
        )

    except common.NotFoundException:
        raise

    except Exception as e:
        globals.logger.error(f"Failed to update credential: {e}", exc_info=True)
        message_id = "500-94005"
        message = multi_lang.get_text(
            message_id, "Credential更新に失敗しました: {}", str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)


@common.platform_exception_handler
def validate_credential(organization_id, ai_service_id, credential_id):
    """
    Credentialを検証

    :param organization_id:
    :type organization_id: str
    :param ai_service_id:
    :type ai_service_id: str
    :param credential_id:
    :type credential_id: str

    :rtype: dict
    """
    globals.logger.info(f"### func:{inspect.currentframe().f_code.co_name}")

    r = connexion.request
    user_id = r.headers.get("User-id")

    try:
        service = get_ai_credential_service()

        credential = service.get_credential(
            organization_id=organization_id,
            user_id=user_id,
            ai_service_id=ai_service_id,
            credential_id=credential_id,
        )

        # サービスごとの検証ロジック
        validation_result = _validate_by_service(ai_service_id, credential.credential_data)

        return common.response_200_ok(validation_result)

    except CredentialNotFound:
        message_id = "404-94009"
        message = multi_lang.get_text(message_id, "Credentialが見つかりません")
        raise common.NotFoundException(message_id=message_id, message=message)

    except Exception as e:
        globals.logger.error(f"Failed to validate credential: {e}", exc_info=True)
        message_id = "500-94006"
        message = multi_lang.get_text(
            message_id, "Credential検証に失敗しました: {}", str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)


def _validate_by_service(ai_service_id: str, credential_data: dict) -> dict:
    """
    AIサービスごとのCredential検証

    Args:
        ai_service_id: AIサービスID
        credential_data: Credentialデータ

    Returns:
        検証結果
    """
    if ai_service_id == "bedrock":
        # AWS Bedrock検証
        import boto3

        try:
            session = boto3.Session(
                aws_access_key_id=credential_data.get("access_key_id"),
                aws_secret_access_key=credential_data.get("secret_access_key"),
                aws_session_token=credential_data.get("session_token"),
                region_name=credential_data.get("region", "ap-northeast-1"),
            )
            sts = session.client("sts")
            identity = sts.get_caller_identity()

            return {
                "valid": True,
                "message": "Credential is valid",
                "account_id": identity.get("Account"),
                "user_id": identity.get("UserId"),
            }
        except Exception as e:
            return {
                "valid": False,
                "message": f"Credential validation failed: {str(e)}",
            }

    elif ai_service_id == "openai":
        # OpenAI検証
        return {
            "valid": True,
            "message": "OpenAI validation not implemented yet",
        }

    elif ai_service_id == "anthropic":
        # Anthropic検証
        return {
            "valid": True,
            "message": "Anthropic validation not implemented yet",
        }

    else:
        return {
            "valid": False,
            "message": f"Validation not supported for service: {ai_service_id}",
        }


@common.platform_exception_handler
def list_models(organization_id, ai_service_id):
    """
    使用可能なモデル一覧を取得

    :param organization_id:
    :type organization_id: str
    :param ai_service_id:
    :type ai_service_id: str

    :rtype: dict
    """
    globals.logger.info(f"### func:{inspect.currentframe().f_code.co_name}")

    r = connexion.request
    user_id = r.headers.get("User-id")

    try:
        # Bedrockのみ対応
        if ai_service_id not in ["aws-cache", "bedrock"]:
            message_id = "400-94011"
            message = multi_lang.get_text(
                message_id, f"Model list not supported for service: {ai_service_id}"
            )
            raise common.BadRequestException(message_id=message_id, message=message)

        model_service = get_model_service()
        models = model_service.get_bedrock_models(
            organization_id=organization_id,
            user_id=user_id,
            ai_service_id=ai_service_id,
        )

        globals.logger.info(
            f"Retrieved {len(models)} models for "
            f"service={ai_service_id}, org={organization_id}, user={user_id}"
        )

        return common.response_200_ok(
            {
                "models": models,
                "count": len(models),
                "ai_service_id": ai_service_id,
            }
        )

    except CredentialNotFound:
        message_id = "404-94012"
        message = multi_lang.get_text(message_id, "Credentialが見つかりません")
        raise common.NotFoundException(message_id=message_id, message=message)

    except Exception as e:
        globals.logger.error(f"Failed to list models: {e}", exc_info=True)
        message_id = "500-94007"
        message = multi_lang.get_text(
            message_id, "モデル一覧取得に失敗しました: {}", str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)
