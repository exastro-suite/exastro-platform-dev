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

import os
import re
import time
import base64

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError, ReadTimeoutError, MissingDependencyException

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


# 画像フォーマットマッピング
_IMAGE_FORMAT_BY_MIME = {
    "image/jpeg": "jpeg",
    "image/png": "png",
    "image/gif": "gif",
    "image/webp": "webp",
}

# ドキュメントフォーマットマッピング
_DOC_FORMAT_BY_MIME = {
    "application/pdf": "pdf",
    "text/plain": "txt",
    "text/csv": "csv",
    "text/html": "html",
    "application/msword": "doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "application/vnd.ms-excel": "xls",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
}


class ModelCapabilities:
    """
    Bedrock モデルの機能対応状況

    モデルごとに対応している機能（Prompt Caching、画像、ドキュメント、ツール）を管理
    """

    @staticmethod
    def get_capabilities(model_id: str) -> dict:
        """
        モデルIDから機能対応状況を取得

        Args:
            model_id: モデルID

        Returns:
            dict: 機能対応状況
        """
        name = (model_id or "").lower()

        # Anthropic Claude - フル対応
        if "anthropic" in name or "claude" in name:
            return {
                "prompt_caching": True,
                "image": True,
                "document": True,
                "tools": True,
                "tool_greedy": False,
                "strict_tool_schema": False,
            }

        # Amazon Nova
        if "nova" in name:
            is_micro = "micro" in name
            return {
                "prompt_caching": False,
                "image": not is_micro,
                "document": not is_micro,
                "tools": not is_micro,
                "tool_greedy": True,  # greedy decoding 必須
                "strict_tool_schema": True,  # スキーマ制約あり
            }

        # OpenAI 系
        if "openai" in name or "gpt" in name:
            return {
                "prompt_caching": False,
                "image": False,
                "document": False,
                "tools": True,
                "tool_greedy": False,
                "strict_tool_schema": False,
            }

        # xAI Grok
        if "grok" in name or "xai" in name:
            return {
                "prompt_caching": False,
                "image": True,
                "document": False,
                "tools": True,
                "tool_greedy": False,
                "strict_tool_schema": False,
            }

        # デフォルト（保守的）
        return {
            "prompt_caching": False,
            "image": False,
            "document": False,
            "tools": True,
            "tool_greedy": False,
            "strict_tool_schema": False,
        }


def _extract_max_tokens_limit(message: str) -> int | None:
    """
    ValidationException からモデルの maxTokens 上限を抽出

    Args:
        message: エラーメッセージ

    Returns:
        int | None: 上限値（見つからない場合は None）
    """
    m = re.search(r"model limit of (\d+)", message or "")
    return int(m.group(1)) if m else None


class BedrockProvider(AIProvider):
    """
    Amazon Bedrock Provider

    Bedrock Runtime Converse APIを使用した実装
    """

    def __init__(
        self,
        credential: AwsRoleCredential,
        region_name: str,
        timeout_seconds: int | None = None,
        enable_prompt_caching: bool = True,
        enable_multimodal: bool = True,
    ):
        """
        Args:
            credential: AWS短期Credential
            region_name: Bedrockリージョン (例: ap-northeast-1)
            timeout_seconds: タイムアウト秒数（Noneの場合は環境変数から読み取り）
            enable_prompt_caching: Prompt Caching を有効化
            enable_multimodal: マルチモーダル（画像・ドキュメント）を有効化
        """
        self.region_name = region_name
        self.enable_prompt_caching = enable_prompt_caching
        self.enable_multimodal = enable_multimodal

        # 環境変数からタイムアウト・リトライ設定を読み取り
        read_timeout = timeout_seconds or int(os.getenv("AI_ASSISTANT_READ_TIMEOUT", "120"))
        connect_timeout = int(os.getenv("AI_ASSISTANT_CONNECT_TIMEOUT", "30"))
        max_attempts = int(os.getenv("AI_ASSISTANT_MAX_ATTEMPTS", "1"))

        self.timeout_seconds = read_timeout

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
                read_timeout=read_timeout,
                connect_timeout=connect_timeout,
                retries={"max_attempts": max_attempts, "mode": "standard"},
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
            # モデル capability 取得
            caps = ModelCapabilities.get_capabilities(request.model_id)

            # リクエストパラメータ構築
            converse_params = {
                "modelId": request.model_id,
                "messages": self._build_messages(request.messages, caps),
            }

            # System プロンプト
            if request.system:
                converse_params["system"] = [{"text": request.system}]

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

            # Nova モデルでツール使用時は greedy decoding が必要
            # （現在はツール未実装だが、将来のために準備）
            if caps.get("tool_greedy"):
                converse_params.setdefault("inferenceConfig", {})["temperature"] = 0
                converse_params["additionalModelRequestFields"] = {
                    "inferenceConfig": {"topK": 1}
                }

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

        except MissingDependencyException as e:
            # botocore[crt] がインストールされていない
            globals.logger.error(f"Missing dependency: {e}")
            raise AIProviderError(
                "Missing required dependency. "
                "Install with: pip install 'botocore[crt]'"
            ) from e

        except ReadTimeoutError as e:
            # タイムアウト（408）
            latency_ms = int((time.time() - start_time) * 1000)
            globals.logger.error(f"Read timeout: {e}, latency={latency_ms}ms")
            raise AIProviderTimeoutError(
                f"Bedrock request timeout after {latency_ms}ms: {str(e)}"
            ) from e

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

            # ValidationException: maxTokens 上限超過の自動調整
            if error_code == "ValidationException":
                limit = _extract_max_tokens_limit(error_message)
                if limit:
                    globals.logger.warning(
                        f"maxTokens exceeds model limit; retrying with maxTokens={limit}"
                    )
                    # 上限値で再試行
                    converse_params.setdefault("inferenceConfig", {})["maxTokens"] = limit
                    try:
                        response = self.client.converse(**converse_params)
                        latency_ms = int((time.time() - start_time) * 1000)

                        output_message = response["output"]["message"]
                        usage = response["usage"]
                        stop_reason = response.get("stopReason")
                        content = self._extract_content(output_message)

                        globals.logger.info(
                            f"Bedrock Converse API succeeded (retry): "
                            f"input_tokens={usage['inputTokens']}, "
                            f"output_tokens={usage['outputTokens']}, "
                            f"latency={latency_ms}ms"
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
                                "retry": True,
                                "adjusted_max_tokens": limit,
                            },
                        )
                    except Exception as retry_error:
                        globals.logger.error(f"Retry failed: {retry_error}")
                        raise AIProviderValidationError(
                            f"Bedrock validation error (retry failed): {error_message}"
                        ) from retry_error
                else:
                    raise AIProviderValidationError(
                        f"Bedrock validation error: {error_message}"
                    ) from e

            # エラー分類
            if error_code in ["AccessDeniedException", "UnauthorizedException"]:
                raise AIProviderAuthError(
                    f"Bedrock authentication failed: {error_message}"
                ) from e
            elif error_code in ["ThrottlingException", "ServiceQuotaExceededException"]:
                raise AIProviderQuotaError(
                    f"Bedrock quota exceeded: {error_message}"
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

    def _build_messages(self, messages: list, caps: dict) -> list:
        """
        Bedrock Converse API用のメッセージ形式に変換

        Args:
            messages: AIMessageリスト
            caps: モデル capability

        Returns:
            list: Bedrockメッセージ形式
        """
        bedrock_messages = []

        for msg in messages:
            # systemロールはBedrockではsystemParameterとして別扱い
            # ここではuser/assistantのみ処理
            if msg.role in ["user", "assistant"]:
                content_blocks = []

                # マルチモーダルコンテンツがある場合
                if self.enable_multimodal and msg.content_blocks:
                    for block in msg.content_blocks:
                        if block.type == "text":
                            content_blocks.append({"text": block.data})

                        elif block.type == "image" and caps.get("image"):
                            # 画像ブロック
                            image_data = block.data
                            mime_type = image_data.get("media_type", "")
                            fmt = _IMAGE_FORMAT_BY_MIME.get(mime_type)
                            if fmt and image_data.get("data"):
                                content_blocks.append({
                                    "image": {
                                        "format": fmt,
                                        "source": {
                                            "bytes": base64.b64decode(image_data["data"])
                                        }
                                    }
                                })

                        elif block.type == "document" and caps.get("document"):
                            # ドキュメントブロック
                            doc_data = block.data
                            mime_type = doc_data.get("media_type", "")
                            fmt = _DOC_FORMAT_BY_MIME.get(mime_type)
                            name = doc_data.get("name", "document")
                            if fmt and doc_data.get("data"):
                                content_blocks.append({
                                    "document": {
                                        "format": fmt,
                                        "name": name,
                                        "source": {
                                            "bytes": base64.b64decode(doc_data["data"])
                                        }
                                    }
                                })
                else:
                    # 通常のテキストメッセージ
                    content_blocks.append({"text": msg.content})

                # Prompt Caching 対応
                if (
                    self.enable_prompt_caching
                    and caps.get("prompt_caching")
                    and msg.cache_control
                    and content_blocks
                ):
                    content_blocks.append({"cachePoint": {"type": "default"}})

                bedrock_messages.append({
                    "role": msg.role,
                    "content": content_blocks
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
