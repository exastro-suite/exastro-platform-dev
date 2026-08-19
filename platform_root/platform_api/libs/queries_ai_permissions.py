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
AI Model Permission Database Queries

AIモデル利用許可関連のデータベースクエリ定義
"""


# ==============================================================================
# T_USER_AI_MODEL_PERMISSION
# ==============================================================================

SQL_SELECT_USER_MODEL_PERMISSION = """
    SELECT
        PERMISSION_ID,
        ORGANIZATION_ID,
        USER_ID,
        AI_SERVICE_ID,
        MODEL_ID,
        CAPABILITY,
        ENABLED,
        VALID_FROM,
        VALID_TO
    FROM
        T_USER_AI_MODEL_PERMISSION
    WHERE
        ORGANIZATION_ID = %s
        AND USER_ID = %s
        AND AI_SERVICE_ID = %s
        AND MODEL_ID = %s
        AND CAPABILITY = %s
        AND ENABLED = TRUE
        AND (VALID_FROM IS NULL OR VALID_FROM <= NOW())
        AND (VALID_TO IS NULL OR VALID_TO > NOW())
"""

SQL_SELECT_USER_ALLOWED_MODELS = """
    SELECT DISTINCT
        AI_SERVICE_ID,
        MODEL_ID,
        CAPABILITY
    FROM
        T_USER_AI_MODEL_PERMISSION
    WHERE
        ORGANIZATION_ID = %s
        AND USER_ID = %s
        AND AI_SERVICE_ID = %s
        AND ENABLED = TRUE
        AND (VALID_FROM IS NULL OR VALID_FROM <= NOW())
        AND (VALID_TO IS NULL OR VALID_TO > NOW())
    ORDER BY
        MODEL_ID, CAPABILITY
"""
