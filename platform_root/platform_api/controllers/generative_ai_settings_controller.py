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
# import connexion
import inspect
import globals

from common_library.common import common
from common_library.common import bl_generative_ai_settings

# コメントとしてファンクションIDを記載 / Enter the function ID as a comment
# MSG_FUNCTION_ID = "42"


@common.platform_exception_handler
def generative_ai_service_list():
    """生成AI情報一覧 / Generative AI Service list

    Returns:
        Response: HTTP Response
    """
    globals.logger.debug(f"### func:{inspect.currentframe().f_code.co_name}")

    # 生成AI情報を取得して返却する
    # Obtain and return generated AI information
    data = bl_generative_ai_settings.generative_ai_settings_list()
    
    return common.response_200_ok(data)


@common.platform_exception_handler
def organization_generative_ai_service_list(organization_id):
    """オーガナイゼーション用生成AI情報一覧 / Generative AI Service list for organization

    Args:
        organization_id (str): organization id

    Returns:
        Response: HTTP Response
    """
    globals.logger.debug(f"### func:{inspect.currentframe().f_code.co_name}")

    # オーガナイゼーション用の生成AI情報を取得して返却する
    # Obtain and return generated AI information for ogranization
    data = bl_generative_ai_settings.organization_generative_ai_settings_list(organization_id)

    return common.response_200_ok(data)
