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
from contextlib import closing
import json

from common_library.common import common
from common_library.common.db import DBconnector
from libs import queries_workspaces

# import globals

MSG_FUNCTION_ID = "22"


@common.platform_exception_handler
def workspace_create(body, organization_id):
    """Create creates an workspace

    :param body:
    :type body: dict | bytes
    :param organization_id:
    :type organization_id: str

    :rtype: Workspace
    """
    if not connexion.request.is_json:
        raise

    body = connexion.request.get_json()
    with closing(DBconnector().connect_orgdb(organization_id)) as conn:
        with conn.cursor() as cursor:
            parameter = {
                "workspace_id": body["workspace_id"],
                "workspace_name": body["workspace_name"],
                "informations": "{}",
            }

            cursor.execute(queries_workspaces.SQL_INSERT_WORKSPACE, parameter)
            conn.commit()

    return common.response_200_ok(body)


@common.platform_exception_handler
def workspace_info(organization_id, workspace_id):
    """workspace info returns infmation of workspaces

    :param organization_id:
    :type organization_id: str
    :param workspace_id:
    :type workspace_id: str

    :rtype: Workspace
    """

    with closing(DBconnector().connect_orgdb(organization_id)) as conn:
        with conn.cursor() as cursor:
            parameter = {
                "workspace_id": workspace_id,
            }

            str_where = " WHERE workspace_id = %(workspace_id)s"
            cursor.execute(queries_workspaces.SQL_QUERY_WORKSPACES + str_where, parameter)

            result = cursor.fetchall()

    # 取得したデータがあるかチェック
    # Check if there is acquired data
    if len(result) > 0:

        row = result[0]
        data = {
            "id": row["WORKSPACE_ID"],
            "name": row["WORKSPACE_NAME"],
            "informations": json.loads(row["INFORMATIONS"]),
            "create_timestamp": common.datetime_to_str(row["CREATE_TIMESTAMP"]),
            "create_user": row["CREATE_USER"],
            "last_update_timestamp": common.datetime_to_str(row["LAST_UPDATE_TIMESTAMP"]),
            "last_update_user": row["LAST_UPDATE_USER"],
        }

        return common.response_200_ok(data)
    else:
        return common.response_status(404, None, f"404-{MSG_FUNCTION_ID}001", "ワークスペース情報が存在しません")


@common.platform_exception_handler
def workspace_list(organization_id, workspace_name=None):
    """List returns list of workspaces

    :param organization_id:
    :type organization_id: str
    :param workspace_name: the workspace's name.
    :type workspace_name: str

    :rtype: WorkspaceList
    """

    with closing(DBconnector().connect_orgdb(organization_id)) as conn:
        with conn.cursor() as cursor:
            if workspace_name:
                str_where = " WHERE workspace_name = %(workspace_name)s"
                parameter = {
                    "workspace_name": workspace_name,
                }
            else:
                str_where = ""
                parameter = {}

            cursor.execute(queries_workspaces.SQL_QUERY_WORKSPACES + str_where, parameter)
            result = cursor.fetchall()

    data = []
    for row in result:
        row = {
            "id": row["WORKSPACE_ID"],
            "name": row["WORKSPACE_NAME"],
            "informations": json.loads(row["INFORMATIONS"]),
            "create_timestamp": common.datetime_to_str(row["CREATE_TIMESTAMP"]),
            "create_user": row["CREATE_USER"],
            "last_update_timestamp": common.datetime_to_str(row["LAST_UPDATE_TIMESTAMP"]),
            "last_update_user": row["LAST_UPDATE_USER"],
        }
        data.append(row)

    return common.response_200_ok(data)
