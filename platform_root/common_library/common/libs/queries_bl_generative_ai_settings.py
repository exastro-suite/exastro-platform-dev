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

SQL_INSERT_GENERATIVE_AI_SERVICES = """
INSERT INTO `T_GENERATIVE_AI_SERVICES`
(`AI_ID`,
`AI_SERVICE`,
`AI_MODEL`,
`AI_DISPLAY_NAME`,
`ENDPOINT_URL`,
`HTTP_HEADERS`,
`EXTERNAL_ACCOUNT_DEFINITION`,
`ENABLED`,
`DISPLAY_ORDER`,
`CREATE_USER`,
`LAST_UPDATE_USER`)
VALUES
(%(ai_id)s,
%(ai_service)s,
%(ai_model)s,
%(ai_display_name)s,
%(endpoint_url)s,
%(http_headers)s,
%(external_account_definition)s,
%(enabled)s,
%(display_order)s,
%(create_user)s,
%(last_update_user)s);
"""

SQL_QUERY_SELECT_GENERATIVE_AI_SERVICES = """SELECT * FROM T_GENERATIVE_AI_SERVICES"""

SQL_QUERY_SELECT_ORG_DB_GENERATIVE_AI_USAGE = """SELECT DISTINCT AI_ID FROM T_GENERATIVE_AI_USAGE"""
