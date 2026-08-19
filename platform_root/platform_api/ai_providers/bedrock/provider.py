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
Amazon Bedrock Provider

Bedrock Converse APIを使用したAIプロバイダー実装
"""

import time

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from ai_providers.base import (
    AIProvider,
    AIRequest,
    AIResponse,
    AIUsage,
    AIProviderError,
    AIProviderAuthError,
    AIProviderQuotaError,
    AIProviderValidationError,
    AIProviderTimeoutError,
)
from services.ai_assistant.user_manual_credential_service import AwsRoleCredential

import globals


class BedrockProvider(AIProvider):
    """
    Amazon Bedrock Provider

    Bedrock Runtime Converse APIを使用した実装
    """

    def __init__(
        self,
        credential: AwsRoleCredential,
        region_name: str,
        timeout_seconds: int = 120,
    ):
        """
        Args:
            credential: AWS短期Credential
            region_name: Bedrockリージョン (例: ap-northeast-1)
            timeout_seconds: タイムアウト秒数
        """
        self.region_name = region_name
        self.timeout_seconds = timeout_seconds

        # boto3 session with temporary credentials
        session = boto3.Session(
            aws_access_key_id=credential.access_key_id,
            aws_secret_access_key=credential.secret_access_key,
            aws_session_token=credential.session_token,
            region_name=region_name,
        )

        self.client = session.client(
            "bedrock-runtime",
            config=Config(
                connect_timeout=5,
                read_timeout=timeout_seconds,
                retries={"max_attempts": 3, "mode": "standard"},
            ),
        )

    def converse(self, request: AIRequest) -> AIResponse:
        """
        Bedrock Converse APIでチャット実行

        Args:
            request: AIリクエスト

        Returns:
            AIResponse: レスポンス

        Raises:
            AIProviderError: 呼び出しエラー
        """
        start_time = time.time()

        try:
            # リクエストパラメータ構築
            converse_params = {
                "modelId": request.model_id,
                "messages": self._build_messages(request.messages),
            }

            # Inference Configuration
            inference_config = {}
            if request.max_tokens is not None:
                inference_config["maxTokens"] = request.max_tokens
            if request.temperature is not None:
                inference_config["temperature"] = request.temperature
            if request.top_p is not None:
                inference_config["topP"] = request.top_p
            if request.stop_sequences:
                inference_config["stopSequences"] = request.stop_sequences

            if inference_config:
                converse_params["inferenceConfig"] = inference_config

            globals.logger.info(
                f"Calling Bedrock Converse API: model={request.model_id}, "
                f"region={self.region_name}, messages={len(request.messages)}"
            )

            # Bedrock API呼び出し
            response = self.client.converse(**converse_params)

            latency_ms = int((time.time() - start_time) * 1000)

            # レスポンスパース
            output_message = response["output"]["message"]
            usage = response["usage"]
            stop_reason = response.get("stopReason")

            content = self._extract_content(output_message)

            globals.logger.info(
                f"Bedrock Converse API succeeded: "
                f"input_tokens={usage['inputTokens']}, "
                f"output_tokens={usage['outputTokens']}, "
                f"latency={latency_ms}ms, "
                f"stop_reason={stop_reason}"
            )

            return AIResponse(
                content=content,
                role=output_message["role"],
                usage=AIUsage(
                    input_tokens=usage["inputTokens"],
                    output_tokens=usage["outputTokens"],
                    total_tokens=usage["totalTokens"],
                ),
                model_id=request.model_id,
                stop_reason=stop_reason,
                metadata={
                    "latency_ms": latency_ms,
                    "region": self.region_name,
                },
            )

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "")
            error_message = e.response.get("Error", {}).get("Message", str(e))
            latency_ms = int((time.time() - start_time) * 1000)

            globals.logger.error(
                f"Bedrock Converse API failed: "
                f"error_code={error_code}, "
                f"error_message={error_message}, "
                f"latency={latency_ms}ms",
                exc_info=True
            )

            # エラー分類
            if error_code in ["AccessDeniedException", "UnauthorizedException"]:
                raise AIProviderAuthError(
                    f"Bedrock authentication failed: {error_message}"
                ) from e
            elif error_code in ["ThrottlingException", "ServiceQuotaExceededException"]:
                raise AIProviderQuotaError(
                    f"Bedrock quota exceeded: {error_message}"
                ) from e
            elif error_code == "ValidationException":
                raise AIProviderValidationError(
                    f"Bedrock validation error: {error_message}"
                ) from e
            elif error_code in ["RequestTimeoutException", "TimeoutError"]:
                raise AIProviderTimeoutError(
                    f"Bedrock request timeout: {error_message}"
                ) from e
            else:
                raise AIProviderError(
                    f"Bedrock error: {error_code} - {error_message}"
                ) from e

        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            globals.logger.error(
                f"Unexpected error in Bedrock provider: {e}, latency={latency_ms}ms",
                exc_info=True
            )
            raise AIProviderError(f"Unexpected Bedrock error: {str(e)}") from e

    def get_provider_name(self) -> str:
        """プロバイダー名を取得"""
        return "bedrock"

    def validate_model_id(self, model_id: str) -> bool:
        """
        Bedrockモデルの妥当性チェック

        Args:
            model_id: モデルID

        Returns:
            bool: 妥当ならTrue
        """
        # Bedrockモデル形式チェック (例: anthropic.claude-3-sonnet-20240229-v1:0)
        if not model_id:
            return False

        # 一般的なBedrockモデルプレフィックス
        valid_prefixes = [
            "anthropic.",
            "amazon.",
            "meta.",
            "mistral.",
            "cohere.",
            "ai21.",
        ]

        return any(model_id.startswith(prefix) for prefix in valid_prefixes)

    def _build_messages(self, messages: list) -> list:
        """
        Bedrock Converse API用のメッセージ形式に変換

        Args:
            messages: AIMessageリスト

        Returns:
            list: Bedrockメッセージ形式
        """
        bedrock_messages = []

        for msg in messages:
            # systemロールはBedrockではsystemParameterとして別扱い
            # ここではuser/assistantのみ処理
            if msg.role in ["user", "assistant"]:
                bedrock_messages.append({
                    "role": msg.role,
                    "content": [
                        {
                            "text": msg.content
                        }
                    ]
                })

        return bedrock_messages

    def _extract_content(self, message: dict) -> str:
        """
        Bedrockレスポンスメッセージからテキストコンテンツを抽出

        Args:
            message: Bedrockメッセージオブジェクト

        Returns:
            str: テキストコンテンツ
        """
        content_blocks = message.get("content", [])

        # 複数のcontentブロックがある場合は結合
        texts = []
        for block in content_blocks:
            if "text" in block:
                texts.append(block["text"])

        return "\n".join(texts) if texts else ""


def create_bedrock_provider(
    credential: AwsRoleCredential,
    region_name: str,
    timeout_seconds: int = 120,
) -> BedrockProvider:
    """
    BedrockProviderファクトリ関数

    Args:
        credential: AWS短期Credential
        region_name: Bedrockリージョン
        timeout_seconds: タイムアウト秒数

    Returns:
        BedrockProvider: インスタンス
    """
    return BedrockProvider(
        credential=credential,
        region_name=region_name,
        timeout_seconds=timeout_seconds,
    )
