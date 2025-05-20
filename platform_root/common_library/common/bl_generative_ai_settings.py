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

from common_library.common.libs import queries_bl_generative_ai_settings

# コメントとしてファンクションIDを記載 / Enter the function ID as a comment
# MSG_FUNCTION_ID = "43"


def generative_ai_settings_list(conn):
    """生成AI情報一覧 / Generative AI Service list

    Returns:
        dict: data item for response
    """

    # system config list get
    with conn.cursor() as cursor:

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
