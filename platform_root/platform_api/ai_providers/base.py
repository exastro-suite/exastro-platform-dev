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
AI Provider Base Classes

AIプロバイダー共通のインターフェース定義
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class ContentBlock:
    """コンテンツブロック（テキスト、画像、ドキュメント）"""
    type: str  # text, image, document
    data: Any  # テキストの場合はstr、画像/ドキュメントの場合はdict


@dataclass
class AIMessage:
    """チャットメッセージ"""
    role: str  # user, assistant, system
    content: str
    cache_control: Optional[Dict[str, Any]] = None  # Prompt Caching用
    content_blocks: Optional[List[ContentBlock]] = None  # マルチモーダル用


@dataclass
class AIRequest:
    """AI呼び出しリクエスト"""
    messages: List[AIMessage]
    model_id: str
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    stop_sequences: Optional[List[str]] = None


@dataclass
class AIUsage:
    """トークン使用量"""
    input_tokens: int
    output_tokens: int
    total_tokens: int


@dataclass
class AIResponse:
    """AI呼び出しレスポンス"""
    content: str
    role: str
    usage: AIUsage
    model_id: str
    stop_reason: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AIProviderError(Exception):
    """AIプロバイダーエラー基底クラス"""
    pass


class AIProviderAuthError(AIProviderError):
    """認証エラー"""
    pass


class AIProviderQuotaError(AIProviderError):
    """クォータ超過エラー"""
    pass


class AIProviderValidationError(AIProviderError):
    """バリデーションエラー"""
    pass


class AIProviderTimeoutError(AIProviderError):
    """タイムアウトエラー"""
    pass


class AIProvider(ABC):
    """
    AI Provider Base Class

    各AIサービス(Bedrock, Gemini, Azure OpenAI等)の
    共通インターフェース
    """

    @abstractmethod
    def converse(self, request: AIRequest) -> AIResponse:
        """
        チャット実行

        Args:
            request: AIリクエスト

        Returns:
            AIResponse: レスポンス

        Raises:
            AIProviderError: 呼び出しエラー
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """
        プロバイダー名を取得

        Returns:
            str: プロバイダー名 (bedrock, gemini等)
        """
        pass

    @abstractmethod
    def validate_model_id(self, model_id: str) -> bool:
        """
        モデルIDの妥当性チェック

        Args:
            model_id: モデルID

        Returns:
            bool: 妥当ならTrue
        """
        pass
