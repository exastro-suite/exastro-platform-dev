#   Copyright 2025 NEC Corporation
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

import json
from contextlib import closing

from common_library.common.db import DBconnector
from common_library.common.libs import queries_bl_generative_ai_settings
import common_library.common.const as common_const

# コメントとしてファンクションIDを記載 / Enter the function ID as a comment
# MSG_FUNCTION_ID = "43"


def generative_ai_settings_list():
    """生成AI情報一覧 / Generative AI Service list

    Returns:
        dict: data item for response
    """

    with closing(DBconnector().connect_platformdb()) as conn:
        with conn.cursor() as cursor:
            # 生成AI情報の取得
            # Get generated AI information
            sql_stmt = queries_bl_generative_ai_settings.SQL_QUERY_SELECT_GENERATIVE_AI_SERVICES

            cursor.execute(sql_stmt)
            rows = cursor.fetchall()

    list_data = []
    # 結果数分処理する
    # Process the results
    for row in rows:
        data = {
            "id": row.get("AI_ID"),
            "service": row.get("AI_SERVICE"),
            "model": row.get("AI_MODEL"),
            "display_name": row.get("AI_DISPLAY_NAME"),
            "endpoint_url": row.get("ENDPOINT_URL"),
            "external_account_definition": json.loads(row.get("EXTERNAL_ACCOUNT_DEFINITION")) if row.get("EXTERNAL_ACCOUNT_DEFINITION") is not None else [],
            "enabled": True if row.get("ENABLED") == 1 else False,
            "display_order": row.get("DISPLAY_ORDER")
        }

        list_data.append(data)
        
    return list_data


def organization_generative_ai_settings_list(organization_id):
    """オーガナイゼーション用生成AI情報一覧 / Generative AI Service list for organization

    Args:
        organization_id (str): organization_id

    Returns:
        dict: data item for response
    """

    with closing(DBconnector().connect_orgdb(organization_id)) as conn:
        with conn.cursor() as cursor:
            # 生成AI情報の取得
            # Get generated AI information
            sql_stmt = queries_bl_generative_ai_settings.SQL_QUERY_SELECT_ORG_DB_GENERATIVE_AI_USAGE

            cursor.execute(sql_stmt)
            rows = cursor.fetchall()

    list_data = []
    with closing(DBconnector().connect_platformdb()) as conn:
        with conn.cursor() as cursor:

            # 結果数分処理する
            # Process the results
            for usage_row in rows:

                str_where = " WHERE AI_ID = %(ai_id)s" + \
                            " AND ENABLED = %(enabled)s"

                parameters = {
                    "ai_id": usage_row.get("AI_ID"),
                    "enabled": common_const.ITEMS_ENABLED_TRUE
                }

                # 生成AI情報の取得
                # Get generated AI information
                sql_stmt = queries_bl_generative_ai_settings.SQL_QUERY_SELECT_GENERATIVE_AI_SERVICES

                cursor.execute(sql_stmt + str_where, parameters)
                row = cursor.fetchone()
                
                if row is not None:
                    data = {
                        "id": row.get("AI_ID"),
                        "service": row.get("AI_SERVICE"),
                        "model": row.get("AI_MODEL"),
                        "display_name": row.get("AI_DISPLAY_NAME"),
                        "external_account_definition": json.loads(row.get("EXTERNAL_ACCOUNT_DEFINITION")) if row.get("EXTERNAL_ACCOUNT_DEFINITION") is not None else [],
                        "display_order": row.get("DISPLAY_ORDER")
                    }

                    list_data.append(data)

    return list_data

