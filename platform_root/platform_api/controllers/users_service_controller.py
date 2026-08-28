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

import connexion
import json
import inspect
import os

from common_library.common import common, api_keycloak_tokens, api_keycloak_users, api_keycloak_roles
from common_library.common import validation
from common_library.common import multi_lang
from common_library.common.db import DBconnector
import common_library.common.const as common_const
from common_library.common import bl_plan_service
from common_library.common import resources

import globals

# AI Credential関連のインポート
from services.users.ai_credential_service import (
    get_ai_credential_service,
    CredentialNotFound,
)
from services.ai_assistant.model_service import (
    get_model_service,
)

MSG_FUNCTION_ID = "25"


@common.platform_exception_handler
def user_list(organization_id, first=0, max=100, search=None):
    """List returns list of users

    Args:
        organization_id (str): organization id
        first (int): start data position index
        max (int): max get count
        search (str): search user keyword

    Returns:
        Response: http response
    """

    globals.logger.info(f"### func:{inspect.currentframe().f_code.co_name}")

    db = DBconnector()
    private = db.get_organization_private(organization_id)

    # サービスアカウントのTOKEN取得
    # Get a service account token
    token_response = api_keycloak_tokens.service_account_get_token(
        organization_id, private.internal_api_client_clientid, private.internal_api_client_secret,
    )
    if token_response.status_code != 200:
        raise common.AuthException(
            "client_user_get_token error status:{}, response:{}".format(token_response.status_code, token_response.text)
        )

    token = json.loads(token_response.text)["access_token"]

    # user 情報取得
    # user get to keycloak
    response = api_keycloak_users.user_get(realm_name=organization_id, user_name=None, token=token, first=first, max=max, search=search)
    if response.status_code != 200:
        globals.logger.error(f"response.status_code:{response.status_code}")
        globals.logger.error(f"response.text:{response.text}")
        message_id = f"500-{MSG_FUNCTION_ID}001"
        message = multi_lang.get_text(
            message_id,
            "ユーザーの取得に失敗しました(対象ID:{0})",
            organization_id,
        )
        raise common.InternalErrorException(message_id=message_id, message=message)

    users = json.loads(response.text)

    data = []
    for user in users:
        ret_user = {
            "id": user["id"],
            "firstName": user.get("firstName", ""),
            "lastName": user.get("lastName", ""),
            "email": user.get("email", ""),
            "preferred_username": user.get("username", ""),
            "name": common.get_username(user.get("firstName"), user.get("lastName"), user.get("username")),
            "affiliation": user.get("attributes", {}).get("affiliation", [""])[0],
            "service_account_user_type": user.get("attributes", {}).get("service_account_user_type", [None])[0],
            "description": user.get("attributes", {}).get("description", [""])[0],
            "enabled": user.get("enabled", False),
            "create_timestamp": common.keycloak_timestamp_to_str(user.get("createdTimestamp")),
        }
        data.append(ret_user)

    globals.logger.debug(f"data:{data}")

    globals.logger.info(f"### Succeed func:{inspect.currentframe().f_code.co_name}")

    return common.response_200_ok(data)


@common.platform_exception_handler
def user_create(body, organization_id):
    """Create creates user

    Args:
        body (dict | bytes): _description_
        organization_id (str): _description_. Defaults to None.

    Returns:
        Response: http response
    """

    # 上限チェック
    # uper limit check
    # users limit get
    limits = bl_plan_service.organization_limits_get(organization_id, common_const.RESOURCE_COUNT_USERS)
    if common_const.RESOURCE_COUNT_USERS in limits:
        # 上限値がある場合にチェックする
        # Check if there is an upper limit
        rc = resources.counter(organization_id)
        globals.logger.info("### users count :{}".format(rc(common_const.RESOURCE_COUNT_USERS)))

        if rc(common_const.RESOURCE_COUNT_USERS) >= limits[common_const.RESOURCE_COUNT_USERS]:
            message_id = "400-00022"
            message = multi_lang.get_text(
                message_id,
                "{0}の上限数({1})を超えるため、新しい{0}は作成できません。",
                multi_lang.get_text('000-00135', "ユーザー"),
                limits[common_const.RESOURCE_COUNT_USERS]
            )
            raise common.BadRequestException(message_id=message_id, message=message)

    body = connexion.request.get_json()
    if not body:
        raise common.BadRequestException(
            message_id='400-00002', message='リクエストボディのパラメータ({})が不正です。'.format('Json')
        )

    user_name = body.get("username")
    user_email = body.get("email")
    user_firstName = body.get("firstName")
    user_lastName = body.get("lastName")
    password = body.get("password")
    password_temporary = body.get("password_temporary", "True")
    user_affiliation = body.get("affiliation")
    user_description = body.get("description")
    user_enabled = body.get("enabled", "True")

    # validation check
    validate = validation.validate_user_name(user_name)
    if not validate.ok:
        return common.response_status(validate.status_code, None, validate.message_id, validate.base_message, *validate.args)
    validate = validation.validate_user_email(user_email)
    if not validate.ok:
        return common.response_status(validate.status_code, None, validate.message_id, validate.base_message, *validate.args)
    validate = validation.validate_user_firstName(user_firstName)
    if not validate.ok:
        return common.response_status(validate.status_code, None, validate.message_id, validate.base_message, *validate.args)
    validate = validation.validate_user_lastName(user_lastName)
    if not validate.ok:
        return common.response_status(validate.status_code, None, validate.message_id, validate.base_message, *validate.args)
    validate = validation.validate_password(password)
    if not validate.ok:
        return common.response_status(validate.status_code, None, validate.message_id, validate.base_message, *validate.args)
    validate = validation.validate_password_temporary(password_temporary)
    if not validate.ok:
        return common.response_status(validate.status_code, None, validate.message_id, validate.base_message, *validate.args)
    validate = validation.validate_user_affiliation(user_affiliation)
    if not validate.ok:
        return common.response_status(validate.status_code, None, validate.message_id, validate.base_message, *validate.args)
    validate = validation.validate_user_description(user_description)
    if not validate.ok:
        return common.response_status(validate.status_code, None, validate.message_id, validate.base_message, *validate.args)
    validate = validation.validate_user_enabled(user_enabled)
    if not validate.ok:
        return common.response_status(validate.status_code, None, validate.message_id, validate.base_message, *validate.args)

    db = DBconnector()
    private = db.get_organization_private(organization_id)

    # サービスアカウントのTOKEN取得
    # Get a service account token
    token_response = api_keycloak_tokens.service_account_get_token(
        organization_id, private.internal_api_client_clientid, private.internal_api_client_secret,
    )
    if token_response.status_code != 200:
        raise common.AuthException(
            "client_user_get_token error status:{}, response:{}".format(token_response.status_code, token_response.text)
        )

    token = json.loads(token_response.text)["access_token"]

    # ユーザー作成
    # create user
    user_json = {
        "username": user_name,
        "email": user_email,
        "firstName": user_firstName,
        "lastName": user_lastName,
        "credentials": [
            {
                "type": "password",
                "value": body.get("password"),
                "temporary": body.get("password_temporary")
            }
        ],
        "attributes":
        {
            "affiliation": [user_affiliation],
            "description": [user_description],
        },
        "enabled": body.get("enabled")
    }

    u_create = api_keycloak_users.user_create(
        realm_name=organization_id, user_json=user_json, token=token
    )
    if u_create.status_code == 409:
        globals.logger.debug(f"response:{u_create.text}")
        message_id = f"409-{MSG_FUNCTION_ID}001"
        message = multi_lang.get_text(
            message_id,
            "指定されたユーザーはすでに存在しているため作成できません。[{0}]",
            json.loads(u_create.text)["errorMessage"])

        raise common.BadRequestException(message_id=message_id, message=message)
    elif u_create.status_code == 400:
        globals.logger.debug(f"response:{u_create.text}")
        message_id = f"400-{MSG_FUNCTION_ID}001"
        message = multi_lang.get_text(
            message_id,
            "ユーザー作成に失敗しました({0})",
            common.get_response_error_message(u_create.text))
        raise common.BadRequestException(message_id=message_id, message=message)

    elif u_create.status_code != 201:
        globals.logger.debug(f"response:{u_create.text}")
        message_id = f"500-{MSG_FUNCTION_ID}002"
        message = multi_lang.get_text(
            message_id,
            "ユーザー作成に失敗しました(対象ユーザー:{0})",
            user_name)

        raise common.InternalErrorException(message_id=message_id, message=message)

    return common.response_200_ok(None)


@common.platform_exception_handler
def user_get(organization_id, user_id):
    """List returns list of roles

    Args:
        organization_id (str): organization id
        user_id (str): user id

    Returns:
        Response: http response
    """

    globals.logger.info(f"### func:{inspect.currentframe().f_code.co_name}")

    db = DBconnector()
    private = db.get_organization_private(organization_id)

    # サービスアカウントのTOKEN取得
    # Get a service account token
    token_response = api_keycloak_tokens.service_account_get_token(
        organization_id, private.internal_api_client_clientid, private.internal_api_client_secret,
    )
    if token_response.status_code != 200:
        raise common.AuthException(
            "client_user_get_token error status:{}, response:{}".format(token_response.status_code, token_response.text)
        )

    token = json.loads(token_response.text)["access_token"]

    # user 情報取得
    # user get to keycloak
    response = api_keycloak_users.user_get_by_id(realm_name=organization_id, user_id=user_id, token=token)
    if response.status_code == 404:
        globals.logger.debug(f"response:{response.text}")
        message_id = f"404-{MSG_FUNCTION_ID}001"
        message = multi_lang.get_text(
            message_id,
            "指定されたユーザーは存在していません。")

        raise common.NotFoundException(message_id=message_id, message=message)
    elif response.status_code != 200:
        globals.logger.error(f"response.status_code:{response.status_code}")
        globals.logger.error(f"response.text:{response.text}")
        message_id = f"500-{MSG_FUNCTION_ID}001"
        message = multi_lang.get_text(
            message_id,
            "ユーザーの取得に失敗しました(対象ID:{0})",
            organization_id,
        )
        raise common.InternalErrorException(message_id=message_id, message=message)

    user = json.loads(response.text)
    globals.logger.debug(f"response user:{user}")

    ret_user = {
        "id": user["id"],
        "firstName": user.get("firstName", ""),
        "lastName": user.get("lastName", ""),
        "email": user.get("email", ""),
        "preferred_username": user.get("username", ""),
        "name": common.get_username(user.get("firstName"), user.get("lastName"), user.get("username")),
        "affiliation": user.get("attributes", {}).get("affiliation", [""])[0],
        "service_account_user_type": user.get("attributes", {}).get("service_account_user_type", [None])[0],
        "description": user.get("attributes", {}).get("description", [""])[0],
        "enabled": user.get("enabled", False),
        "create_timestamp": common.keycloak_timestamp_to_str(user.get("createdTimestamp")),
    }

    globals.logger.debug(f"ret_user:{ret_user}")

    globals.logger.info(f"### Succeed func:{inspect.currentframe().f_code.co_name}")

    return common.response_200_ok(ret_user)


@common.platform_exception_handler
def user_update(body, organization_id, user_id):  # noqa: E501
    """update user

    Args:
        body (dict): body
        organization_id (str): organization id
        user_id (str): user id

    Returns:
        Response: http response
    """
    body = connexion.request.get_json()
    if not body:
        raise common.BadRequestException(
            message_id='400-00002', message='リクエストボディのパラメータ({})が不正です。'.format('Json')
        )

    user_email = body.get("email")
    user_firstName = body.get("firstName")
    user_lastName = body.get("lastName")
    password = body.get("password")
    password_temporary = body.get("password_temporary", "True")
    user_affiliation = body.get("affiliation")
    user_description = body.get("description")
    user_enabled = body.get("enabled", "True")

    # validation check
    validate = validation.validate_user_email(user_email)
    if not validate.ok:
        return common.response_status(validate.status_code, None, validate.message_id, validate.base_message, *validate.args)
    validate = validation.validate_user_firstName(user_firstName)
    if not validate.ok:
        return common.response_status(validate.status_code, None, validate.message_id, validate.base_message, *validate.args)
    validate = validation.validate_user_lastName(user_lastName)
    if not validate.ok:
        return common.response_status(validate.status_code, None, validate.message_id, validate.base_message, *validate.args)
    validate = validation.validate_password_temporary(password_temporary)
    if not validate.ok:
        return common.response_status(validate.status_code, None, validate.message_id, validate.base_message, *validate.args)
    if password is not None:
        validate = validation.validate_password(password)
        if not validate.ok:
            return common.response_status(validate.status_code, None, validate.message_id, validate.base_message, *validate.args)
    validate = validation.validate_user_affiliation(user_affiliation)
    if not validate.ok:
        return common.response_status(validate.status_code, None, validate.message_id, validate.base_message, *validate.args)
    validate = validation.validate_user_description(user_description)
    if not validate.ok:
        return common.response_status(validate.status_code, None, validate.message_id, validate.base_message, *validate.args)
    validate = validation.validate_user_enabled(user_enabled)
    if not validate.ok:
        return common.response_status(validate.status_code, None, validate.message_id, validate.base_message, *validate.args)

    db = DBconnector()
    private = db.get_organization_private(organization_id)

    # サービスアカウントのTOKEN取得
    # Get a service account token
    token_response = api_keycloak_tokens.service_account_get_token(
        organization_id, private.internal_api_client_clientid, private.internal_api_client_secret,
    )
    if token_response.status_code != 200:
        raise common.AuthException(
            "client_user_get_token error status:{}, response:{}".format(token_response.status_code, token_response.text)
        )

    token = json.loads(token_response.text)["access_token"]

    if body.get("enabled") is False:
        # organization role user情報取得
        # get organization role user information
        response = api_keycloak_roles.role_uesrs_get(
            realm_name=organization_id, client_id=private.user_token_client_id, role_name=common_const.ORG_ROLE_ORG_MANAGER, token=token,
        )
        if response.status_code != 200:
            globals.logger.error(f"response:{response.text}")
            message_id = f"500-{MSG_FUNCTION_ID}005"
            message = multi_lang.get_text(
                message_id,
                "オーガナイゼーション管理者ロールのユーザー情報が取得できません")
            raise common.InternalErrorException(message_id=message_id, message=message)

        # User role チェック - オーガナイゼーション管理者は無効化不可
        # User role check - organization admin cannot disable
        response_user = json.loads(response.text)
        og_managers = [u.get("id") for u in response_user]
        globals.logger.debug(f"og_managers:{og_managers}")

        if user_id in og_managers:
            message_id = f"400-{MSG_FUNCTION_ID}006"
            message = multi_lang.get_text(
                message_id,
                "オーガナイゼーション管理者は無効にできません")
            raise common.BadRequestException(message_id=message_id, message=message)

    # 更新前のユーザー情報の取得
    # Get user information before update
    res_before_user = api_keycloak_users.user_get_by_id(realm_name=organization_id, user_id=user_id, token=token)
    if res_before_user.status_code == 404:
        globals.logger.debug(f"response:{res_before_user.text}")
        message_id = f"404-{MSG_FUNCTION_ID}001"
        message = multi_lang.get_text(
            message_id,
            "指定されたユーザーは存在していません。")

        raise common.NotFoundException(message_id=message_id, message=message)

    elif res_before_user.status_code != 200:
        globals.logger.error(f"response.status_code:{res_before_user.status_code}")
        globals.logger.error(f"response.text:{res_before_user.text}")
        message_id = f"500-{MSG_FUNCTION_ID}001"
        message = multi_lang.get_text(
            message_id,
            "ユーザーの取得に失敗しました(対象ID:{0})",
            organization_id,
        )
        raise common.InternalErrorException(message_id=message_id, message=message)

    before_user = json.loads(res_before_user.text)

    # ユーザー更新
    # update user
    user_json = {
        "email": user_email,
        "firstName": user_firstName,
        "lastName": user_lastName,
        "attributes": before_user.get("attributes", {}),  # 属性情報をbeforeから設定(localeを残すため)
        "enabled": body.get("enabled")
    }

    user_json["attributes"]["affiliation"] = user_affiliation
    user_json["attributes"]["description"] = user_description

    if body.get("password") is not None:
        user_json["credentials"] = [
            {
                "type": "password",
                "value": body.get("password"),
                "temporary": body.get("password_temporary")
            }
        ]

    u_update = api_keycloak_users.user_update(
        realm_name=organization_id, user_id=user_id, user_json=user_json, token=token
    )
    if u_update.status_code == 404:
        globals.logger.debug(f"response:{u_update.text}")
        message_id = f"404-{MSG_FUNCTION_ID}001"
        message = multi_lang.get_text(
            message_id,
            "指定されたユーザーは存在していません。")

        raise common.NotFoundException(message_id=message_id, message=message)

    elif u_update.status_code == 400:
        globals.logger.debug(f"response:{u_update.text}")
        message_id = f"400-{MSG_FUNCTION_ID}004"
        message = multi_lang.get_text(
            message_id,
            "ユーザー更新に失敗しました({0})",
            common.get_response_error_message(u_update.text))
        raise common.BadRequestException(message_id=message_id, message=message)

    elif u_update.status_code not in [200, 204]:
        globals.logger.debug(f"response:{u_update.text}")
        message_id = f"500-{MSG_FUNCTION_ID}004"
        message = multi_lang.get_text(
            message_id,
            "ユーザー更新に失敗しました(対象ユーザーID:{0})[{1}]",
            user_id,
            json.loads(u_update.text)["errorMessage"])

        raise common.InternalErrorException(message_id=message_id, message=message)

    return common.response_200_ok(None)


@common.platform_exception_handler
def user_delete(organization_id, user_id):
    """delete user

    Args:
        organization_id (str): organization id
        user_id (str): user id

    Returns:
        Response: http response
    """

    db = DBconnector()
    private = db.get_organization_private(organization_id)

    # サービスアカウントのTOKEN取得
    # Get a service account token
    token_response = api_keycloak_tokens.service_account_get_token(
        organization_id, private.internal_api_client_clientid, private.internal_api_client_secret,
    )
    if token_response.status_code != 200:
        raise common.AuthException(
            "client_user_get_token error status:{}, response:{}".format(token_response.status_code, token_response.text)
        )

    token = json.loads(token_response.text)["access_token"]

    # organization role user情報取得
    # get organization role user information
    response = api_keycloak_roles.role_uesrs_get(
        realm_name=organization_id, client_id=private.user_token_client_id, role_name=common_const.ORG_ROLE_ORG_MANAGER, token=token,
    )
    if response.status_code != 200:
        globals.logger.error(f"response:{response.text}")
        message_id = f"500-{MSG_FUNCTION_ID}005"
        message = multi_lang.get_text(
            message_id,
            "オーガナイゼーション管理者ロールのユーザー情報が取得できません")
        raise common.InternalErrorException(message_id=message_id, message=message)

    # User role チェック - オーガナイゼーション管理者は削除不可
    # User role check - organization admin cannot delete
    response_user = json.loads(response.text)
    og_managers = [u.get("id") for u in response_user]
    globals.logger.debug(f"og_managers:{og_managers}")

    if user_id in og_managers:
        message_id = f"400-{MSG_FUNCTION_ID}005"
        message = multi_lang.get_text(
            message_id,
            "オーガナイゼーション管理者は削除できません")
        raise common.BadRequestException(message_id=message_id, message=message)

    response = api_keycloak_users.user_delete(
        realm_name=organization_id, user_id=user_id, token=token
    )
    if response.status_code == 404:
        globals.logger.debug(f"response:{response.text}")
        message_id = f"404-{MSG_FUNCTION_ID}001"
        message = multi_lang.get_text(
            message_id,
            "指定されたユーザーが存在しません")

        raise common.BadRequestException(message_id=message_id, message=message)
    elif response.status_code == 400:
        globals.logger.debug(f"response:{response.text}")
        message_id = f"400-{MSG_FUNCTION_ID}003"
        message = multi_lang.get_text(
            message_id,
            "ユーザー削除に失敗しました(対象ユーザーID:{0})",
            user_id)
        raise common.BadRequestException(message_id=message_id, message=message)

    elif response.status_code != 204:
        globals.logger.debug(f"response:{response.text}")
        message_id = f"500-{MSG_FUNCTION_ID}003"
        message = multi_lang.get_text(
            message_id,
            "ユーザー削除に失敗しました(対象ユーザーID:{0})[{1}]",
            user_id,
            json.loads(response.text)["errorMessage"])

        raise common.InternalErrorException(message_id=message_id, message=message)

    return common.response_200_ok(None)

# =========================================================================
# AI Credential Service Functions
# =========================================================================

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

    # bedrock-cache の特別処理
    if ai_service_id == "bedrock-cache":
        # キャッシュファイルの内容が渡されているか確認
        if "idToken" not in credential_data:
            message_id = "400-94014"
            message = multi_lang.get_text(
                message_id,
                "bedrock-cache requires full cache file content including idToken."
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

        globals.logger.debug(
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

        # Credentialデータはマスク(セキュリティ上、詳細は返さない)
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

        globals.logger.debug(
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
    Credentialを更新(部分更新)

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
            message_id, "更新するフィールドを指定してください(credential_name, credential_data, notes のいずれか)"
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

        # bedrock-cache の特別処理
        if ai_service_id == "bedrock-cache":
            if "idToken" not in credential_data:
                message_id = "400-94017"
                message = multi_lang.get_text(
                    message_id,
                    "bedrock-cache requires full cache file content including idToken."
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

        globals.logger.debug(
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
        from botocore.config import Config

        try:
            # 環境変数からタイムアウト・リトライ設定を読み込み
            read_timeout = int(os.getenv("AI_ASSISTANT_READ_TIMEOUT", "120"))
            connect_timeout = int(os.getenv("AI_ASSISTANT_CONNECT_TIMEOUT", "30"))
            max_attempts = int(os.getenv("AI_ASSISTANT_MAX_ATTEMPTS", "1"))

            session = boto3.Session(
                aws_access_key_id=credential_data.get("access_key_id"),
                aws_secret_access_key=credential_data.get("secret_access_key"),
                aws_session_token=credential_data.get("session_token"),
                region_name=credential_data.get("region", "ap-northeast-1"),
            )
            sts = session.client(
                "sts",
                config=Config(
                    read_timeout=read_timeout,
                    connect_timeout=connect_timeout,
                    retries={"max_attempts": max_attempts, "mode": "standard"},
                ),
            )
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
        if ai_service_id not in ["bedrock-cache", "bedrock"]:
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

    except common.RequestTimeoutException:
        # 408 タイムアウト(serviceレイヤーで生成済み)
        raise

    except Exception as e:
        globals.logger.error(f"Failed to list models: {e}", exc_info=True)
        message_id = "500-94007"
        message = multi_lang.get_text(
            message_id, "モデル一覧取得に失敗しました: {}", str(e)
        )
        raise common.InternalErrorException(message_id=message_id, message=message)
