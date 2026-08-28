# AI Providers - 汎用AIサービス対応

## 概要

このディレクトリには、複数のAIサービス（AWS Bedrock、OpenAI、Google Gemini等）を統一的に扱うための抽象化層が実装されています。

## 対応AIサービス

| サービス | ai_service_id | System対応 | 備考 |
|---------|--------------|-----------|------|
| AWS Bedrock | `bedrock`, `aws-cache` | ✅ | Claude, Nova等 |
| OpenAI | `openai` | ✅ | GPT-4, GPT-3.5等 |
| Google Gemini | `gemini` | ✅ | Gemini Pro, Flash等 |

## アーキテクチャ

```
ai_providers/
├── base.py              # 抽象基底クラス（AIProvider, AIRequest, AIResponse）
├── factory.py           # プロバイダーファクトリー
├── bedrock/
│   └── provider.py      # Bedrock実装
├── openai/
│   └── provider.py      # OpenAI実装
└── gemini/
    └── provider.py      # Gemini実装
```

## System パラメータの扱い

各AIサービスは異なる方法でシステムプロンプトを指定します：

### AWS Bedrock (Claude)
```python
response = bedrock_client.converse(
    modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
    system=[{"text": "あなたはアシスタントです。"}],  # リスト形式
    messages=[...]
)
```

### OpenAI
```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "あなたはアシスタントです。"},  # messagesの中
        {"role": "user", "content": "こんにちは"}
    ]
)
```

### Google Gemini
```python
model = genai.GenerativeModel(
    model_name="gemini-pro",
    system_instruction="あなたはアシスタントです。"  # モデル作成時に指定
)
```

## 使用例

### 1. 基本的な使用

```python
from ai_providers.factory import create_ai_provider
from ai_providers.base import AIRequest, AIMessage

# プロバイダーを作成
provider = create_ai_provider(
    ai_service_id="bedrock",
    credential_data={
        "access_key_id": "...",
        "secret_access_key": "...",
        "session_token": "...",
        "region": "ap-northeast-1"
    },
    timeout_seconds=120
)

# リクエストを構築
request = AIRequest(
    messages=[
        AIMessage(role="user", content="こんにちは")
    ],
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    system="あなたは親切なアシスタントです。",  # システムプロンプト
    max_tokens=4096,
    temperature=0.7
)

# AI呼び出し
response = provider.converse(request)

print(f"応答: {response.content}")
print(f"トークン使用量: {response.usage.input_tokens} + {response.usage.output_tokens}")
```

### 2. ConversationService での使用

```python
from services.ai_assistant.conversation_service import get_conversation_service

service = get_conversation_service()

# 汎用版メソッドを使用
result = service.send_message_v2(
    organization_id="org123",
    workspace_id="ws456",
    user_id="user789",
    conversation_id="conv001",
    message_text="こんにちは",
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    ai_service_id="bedrock",  # bedrock, openai, gemini等
    system_prompt="あなたはExastro Platform AIアシスタントです。",  # システムプロンプト
    max_tokens=4096,
    temperature=0.7
)

print(f"応答: {result['content']}")
print(f"プロバイダー: {result['provider']}")
```

### 3. 異なるAIサービスへの切り替え

```python
# Bedrockを使用
result1 = service.send_message_v2(
    ...,
    ai_service_id="bedrock",
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    system_prompt="あなたはアシスタントです。"
)

# OpenAIを使用
result2 = service.send_message_v2(
    ...,
    ai_service_id="openai",
    model_id="gpt-4",
    system_prompt="あなたはアシスタントです。"
)

# Geminiを使用
result3 = service.send_message_v2(
    ...,
    ai_service_id="gemini",
    model_id="gemini-1.5-pro",
    system_prompt="あなたはアシスタントです。"
)
```

## 新しいプロバイダーの追加

新しいAIサービスを追加する手順：

1. `ai_providers/<service_name>/provider.py` を作成
2. `AIProvider` 抽象基底クラスを継承
3. `converse()`, `get_provider_name()`, `validate_model_id()` を実装
4. System パラメータを適切に処理
5. `factory.py` にファクトリーロジックを追加

### 実装例

```python
from ai_providers.base import AIProvider, AIRequest, AIResponse

class MyAIProvider(AIProvider):
    def converse(self, request: AIRequest) -> AIResponse:
        # System プロンプトの処理
        system = request.system
        
        # APIコールの実装
        # ...
        
        return AIResponse(
            content=content,
            role="assistant",
            usage=AIUsage(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens
            ),
            model_id=request.model_id
        )
    
    def get_provider_name(self) -> str:
        return "myai"
    
    def validate_model_id(self, model_id: str) -> bool:
        return model_id.startswith("myai-")
```

## エラーハンドリング

各プロバイダーは統一的な例外を投げます：

- `AIProviderAuthError`: 認証エラー
- `AIProviderQuotaError`: クォータ超過
- `AIProviderTimeoutError`: タイムアウト
- `AIProviderValidationError`: バリデーションエラー
- `AIProviderError`: その他のエラー

```python
from ai_providers.base import (
    AIProviderTimeoutError,
    AIProviderAuthError
)

try:
    response = provider.converse(request)
except AIProviderTimeoutError as e:
    # タイムアウト処理
    pass
except AIProviderAuthError as e:
    # 認証エラー処理
    pass
```

## テスト

```bash
# 単体テスト
pytest tests/test_ai_providers.py

# 統合テスト
pytest tests/integration/test_conversation_service.py
```

## パフォーマンス

各プロバイダーのレスポンスタイムは `metadata["latency_ms"]` に記録されます：

```python
response = provider.converse(request)
print(f"レイテンシ: {response.metadata['latency_ms']}ms")
```
