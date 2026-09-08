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
OpenAI Provider

OpenAI Chat Completions APIを使用したAIプロバイダー実装
"""

import time
from typing import Optional

from openai import OpenAI
from openai import APIError, APITimeoutError, RateLimitError, AuthenticationError

from ai_providers.base import (
    AIProvider,
    AIRequest,
    AIResponse,
    AIUsage,
    AIProviderError,
    AIProviderAuthError,
    AIProviderQuotaError,
    AIProviderTimeoutError,
)

import globals


class OpenAIProvider(AIProvider):
    """
    OpenAI Provider

    OpenAI Chat Completions APIを使用した実装
    """

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout_seconds: int = 120,
    ):
        """
        Args:
            api_key: OpenAI API Key
            base_url: カスタムベースURL（Azure OpenAI用など）
            timeout_seconds: タイムアウト秒数
        """
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout_seconds,
        )
        self.timeout_seconds = timeout_seconds

    def converse(self, request: AIRequest) -> AIResponse:
        """
        OpenAI Chat Completions APIでチャット実行

        Args:
            request: AIリクエスト

        Returns:
            AIResponse: レスポンス

        Raises:
            AIProviderError: 呼び出しエラー
        """
        start_time = time.time()

        try:
            # OpenAI形式のメッセージ構築
            messages = []

            # System プロンプトは messages の最初に追加
            if request.system:
                messages.append({
                    "role": "system",
                    "content": request.system
                })

            # ユーザー・アシスタントメッセージを追加
            for msg in request.messages:
                if msg.role in ["user", "assistant"]:
                    messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })

            # API呼び出しパラメータ構築
            api_params = {
                "model": request.model_id,
                "messages": messages,
            }

            if request.max_tokens is not None:
                api_params["max_tokens"] = request.max_tokens
            if request.temperature is not None:
                api_params["temperature"] = request.temperature
            if request.top_p is not None:
                api_params["top_p"] = request.top_p
            if request.stop_sequences:
                api_params["stop"] = request.stop_sequences

            globals.logger.info(
                f"Calling OpenAI Chat Completions API: model={request.model_id}, "
                f"messages={len(messages)}"
            )

            # OpenAI API呼び出し
            response = self.client.chat.completions.create(**api_params)

            latency_ms = int((time.time() - start_time) * 1000)

            # レスポンスパース
            choice = response.choices[0]
            content = choice.message.content or ""
            usage = response.usage

            globals.logger.info(
                f"OpenAI Chat Completions API succeeded: "
                f"prompt_tokens={usage.prompt_tokens}, "
                f"completion_tokens={usage.completion_tokens}, "
                f"latency={latency_ms}ms, "
                f"finish_reason={choice.finish_reason}"
            )

            return AIResponse(
                content=content,
                role=choice.message.role,
                usage=AIUsage(
                    input_tokens=usage.prompt_tokens,
                    output_tokens=usage.completion_tokens,
                    total_tokens=usage.total_tokens,
                ),
                model_id=request.model_id,
                stop_reason=choice.finish_reason,
                metadata={
                    "latency_ms": latency_ms,
                },
            )

        except AuthenticationError as e:
            # 認証エラー
            globals.logger.error(f"OpenAI authentication failed: {e}")
            raise AIProviderAuthError(
                f"OpenAI authentication failed: {str(e)}"
            ) from e

        except RateLimitError as e:
            # レート制限エラー
            globals.logger.error(f"OpenAI rate limit exceeded: {e}")
            raise AIProviderQuotaError(
                f"OpenAI rate limit exceeded: {str(e)}"
            ) from e

        except APITimeoutError as e:
            # タイムアウト
            latency_ms = int((time.time() - start_time) * 1000)
            globals.logger.error(f"OpenAI timeout: {e}, latency={latency_ms}ms")
            raise AIProviderTimeoutError(
                f"OpenAI request timeout after {latency_ms}ms: {str(e)}"
            ) from e

        except APIError as e:
            # その他のAPIエラー
            latency_ms = int((time.time() - start_time) * 1000)
            globals.logger.error(
                f"OpenAI API error: {e}, latency={latency_ms}ms",
                exc_info=True
            )
            raise AIProviderError(
                f"OpenAI API error: {str(e)}"
            ) from e

        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            globals.logger.error(
                f"Unexpected error in OpenAI provider: {e}, latency={latency_ms}ms",
                exc_info=True
            )
            raise AIProviderError(f"Unexpected OpenAI error: {str(e)}") from e

    def get_provider_name(self) -> str:
        """プロバイダー名を取得"""
        return "openai"

    def validate_model_id(self, model_id: str) -> bool:
        """
        OpenAIモデルの妥当性チェック

        Args:
            model_id: モデルID

        Returns:
            bool: 妥当ならTrue
        """
        if not model_id:
            return False

        # OpenAIモデル形式チェック
        valid_models = [
            "gpt-4",
            "gpt-4-turbo",
            "gpt-4o",
            "gpt-3.5-turbo",
            "o1-preview",
            "o1-mini",
        ]

        return any(model_id.startswith(model) for model in valid_models)
