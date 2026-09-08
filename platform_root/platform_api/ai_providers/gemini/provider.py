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
Google Gemini Provider

Google Generative AI APIを使用したAIプロバイダー実装
"""

import time
from typing import Optional

import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

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


class GeminiProvider(AIProvider):
    """
    Google Gemini Provider

    Google Generative AI APIを使用した実装
    """

    def __init__(
        self,
        api_key: str,
        timeout_seconds: int = 120,
    ):
        """
        Args:
            api_key: Google API Key
            timeout_seconds: タイムアウト秒数
        """
        genai.configure(api_key=api_key)
        self.timeout_seconds = timeout_seconds

    def converse(self, request: AIRequest) -> AIResponse:
        """
        Google Generative AI APIでチャット実行

        Args:
            request: AIリクエスト

        Returns:
            AIResponse: レスポンス

        Raises:
            AIProviderError: 呼び出しエラー
        """
        start_time = time.time()

        try:
            # Generation Config
            generation_config = {}
            if request.max_tokens is not None:
                generation_config["max_output_tokens"] = request.max_tokens
            if request.temperature is not None:
                generation_config["temperature"] = request.temperature
            if request.top_p is not None:
                generation_config["top_p"] = request.top_p
            if request.stop_sequences:
                generation_config["stop_sequences"] = request.stop_sequences

            # モデル作成（system instruction付き）
            model = genai.GenerativeModel(
                model_name=request.model_id,
                generation_config=generation_config,
                system_instruction=request.system if request.system else None,
            )

            # 会話履歴を構築
            history = []
            for msg in request.messages[:-1]:  # 最後のメッセージ以外
                if msg.role in ["user", "model"]:  # Geminiでは "assistant" は "model"
                    role = "model" if msg.role == "assistant" else msg.role
                    history.append({
                        "role": role,
                        "parts": [msg.content]
                    })

            # チャットセッション開始
            chat = model.start_chat(history=history)

            # 最後のユーザーメッセージを送信
            last_message = request.messages[-1]
            if last_message.role != "user":
                raise AIProviderError("Last message must be from user")

            globals.logger.info(
                f"Calling Google Gemini API: model={request.model_id}, "
                f"messages={len(request.messages)}"
            )

            response = chat.send_message(last_message.content)

            latency_ms = int((time.time() - start_time) * 1000)

            # レスポンスパース
            content = response.text

            # 使用量情報（Geminiではtoken countが取得できる）
            input_tokens = 0
            output_tokens = 0
            if hasattr(response, 'usage_metadata'):
                input_tokens = response.usage_metadata.prompt_token_count or 0
                output_tokens = response.usage_metadata.candidates_token_count or 0

            globals.logger.info(
                f"Google Gemini API succeeded: "
                f"input_tokens={input_tokens}, "
                f"output_tokens={output_tokens}, "
                f"latency={latency_ms}ms"
            )

            return AIResponse(
                content=content,
                role="assistant",
                usage=AIUsage(
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    total_tokens=input_tokens + output_tokens,
                ),
                model_id=request.model_id,
                stop_reason=response.candidates[0].finish_reason.name if response.candidates else None,
                metadata={
                    "latency_ms": latency_ms,
                },
            )

        except google_exceptions.Unauthenticated as e:
            # 認証エラー
            globals.logger.error(f"Gemini authentication failed: {e}")
            raise AIProviderAuthError(
                f"Gemini authentication failed: {str(e)}"
            ) from e

        except google_exceptions.ResourceExhausted as e:
            # クォータ超過
            globals.logger.error(f"Gemini quota exceeded: {e}")
            raise AIProviderQuotaError(
                f"Gemini quota exceeded: {str(e)}"
            ) from e

        except google_exceptions.DeadlineExceeded as e:
            # タイムアウト
            latency_ms = int((time.time() - start_time) * 1000)
            globals.logger.error(f"Gemini timeout: {e}, latency={latency_ms}ms")
            raise AIProviderTimeoutError(
                f"Gemini request timeout after {latency_ms}ms: {str(e)}"
            ) from e

        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            globals.logger.error(
                f"Unexpected error in Gemini provider: {e}, latency={latency_ms}ms",
                exc_info=True
            )
            raise AIProviderError(f"Unexpected Gemini error: {str(e)}") from e

    def get_provider_name(self) -> str:
        """プロバイダー名を取得"""
        return "gemini"

    def validate_model_id(self, model_id: str) -> bool:
        """
        Geminiモデルの妥当性チェック

        Args:
            model_id: モデルID

        Returns:
            bool: 妥当ならTrue
        """
        if not model_id:
            return False

        # Geminiモデル形式チェック
        valid_models = [
            "gemini-pro",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-2.0-flash",
        ]

        return any(model_id.startswith(model) for model in valid_models)
