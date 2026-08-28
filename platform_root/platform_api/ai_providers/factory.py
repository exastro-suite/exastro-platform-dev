#   Copyright 2026 NEC Corporation
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
AI Provider Factory

AIプロバイダーのファクトリー関数
"""

from typing import Dict, Any
from ai_providers.base import AIProvider
from ai_providers.bedrock.provider import BedrockProvider
# from ai_providers.openai.provider import OpenAIProvider
# from ai_providers.gemini.provider import GeminiProvider
from services.ai_assistant.user_manual_credential_service import AwsRoleCredential


class UnsupportedAIServiceError(Exception):
    """サポートされていないAIサービス"""
    pass


def create_ai_provider(
    ai_service_id: str,
    credential_data: Dict[str, Any],
    timeout_seconds: int = 120,
) -> AIProvider:
    """
    AIプロバイダーを作成

    Args:
        ai_service_id: AIサービスID（bedrock, openai, gemini等）
        credential_data: 認証情報データ
        timeout_seconds: タイムアウト秒数

    Returns:
        AIProvider: プロバイダーインスタンス

    Raises:
        UnsupportedAIServiceError: サポートされていないサービス
    """
    if ai_service_id in ["bedrock", "bedrock-cache"]:
        # AWS Bedrock
        region = credential_data.get("region", "ap-northeast-1")
        credential = AwsRoleCredential(
            access_key_id=credential_data.get("access_key_id"),
            secret_access_key=credential_data.get("secret_access_key"),
            session_token=credential_data.get("session_token"),
        )
        return BedrockProvider(
            credential=credential,
            region_name=region,
            timeout_seconds=timeout_seconds,
        )

    # elif ai_service_id == "openai":
    #     # OpenAI
    #     api_key = credential_data.get("api_key")
    #     base_url = credential_data.get("base_url")  # Azure OpenAI用
    #     return OpenAIProvider(
    #         api_key=api_key,
    #         base_url=base_url,
    #         timeout_seconds=timeout_seconds,
    #     )

    # elif ai_service_id == "gemini":
    #     # Google Gemini
    #     api_key = credential_data.get("api_key")
    #     return GeminiProvider(
    #         api_key=api_key,
    #         timeout_seconds=timeout_seconds,
    #     )

    else:
        raise UnsupportedAIServiceError(
            f"Unsupported AI service: {ai_service_id}. "
            f"Supported services: bedrock, bedrock-cache, openai, gemini"
        )
