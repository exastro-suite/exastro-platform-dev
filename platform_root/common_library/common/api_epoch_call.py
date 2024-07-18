#   Copyright 2024 NEC Corporation
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

# import inspect
import os
import json
import requests

# User Imports
import globals  # 共通的なglobals Common globals

def __get_api_url_epoch():
    api_url = "{}://{}:{}".format(os.environ['EPOCH_SERVER_PROTOCOL'], os.environ['EPOCH_SERVER_HOST'], os.environ['EPOCH_SERVER_API_PORT'])
    return api_url

def epoch_workspace_create(organization_id, workspace_id, wsadmin_role_name, user_id, encode_roles, language):
    """EPOCH Workspace作成 Create EPOCH Workspace
    Args:
        organization_id (str): organization id
        workspace_id (str): workspace id
        wsadmin_role_name (str): wsadmin role name
        user_id (str): user id
        encode_roles (str): encode roles
        language (str): language
    Returns:
        Response: HTTP Respose (success : .status_code=200)
    """

    globals.logger.info(
        'Create EPOCH Workspace. organization_id={}, workspace_id={}, wsadmin_role_name={}, user_id={}'.format(
            organization_id, workspace_id, wsadmin_role_name, user_id)
    )

    header_para = {
        "Content-Type": "application/json",
        "organization_id": organization_id,
        "User-Id": user_id,
        "Roles": encode_roles,
        "Language": language,
    }
    data_para = {
        "role_id": wsadmin_role_name,
    }

    globals.logger.debug("Create EPOCH Workspace post送信")
    # 呼び出し先設定 call destination setting
    api_url = __get_api_url_epoch()
    request_response = requests.post(
        "{}/internal-api/{}/workspaces/{}/epoch/".format(api_url, organization_id, workspace_id),
        headers=header_para,
        data=json.dumps(data_para),
    )
    globals.logger.debug(request_response.text)

    return request_response
