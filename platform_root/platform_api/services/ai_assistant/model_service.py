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
Model Service

AIサービスの使用可能なモデル一覧を取得
"""

from typing import List, Dict
import boto3
from botocore.config import Config

from services.ai_assistant.ai_credential_service import (
    get_ai_credential_service,
    CredentialNotFound,
)
from services.ai_assistant.aws_session_manager import (
    create_bedrock_session_from_credential_data,
)

import globals


class ModelService:
    """
    Model Service

    AIサービスの使用可能なモデル一覧を取得
    """

    def get_bedrock_models(
        self,
        organization_id: str,
        user_id: str,
        ai_service_id: str,
    ) -> List[Dict]:
        """
        Bedrockの使用可能なモデル一覧を取得

        Args:
            organization_id: Organization ID
            user_id: User ID
            ai_service_id: AIサービスID (aws-cache または bedrock)

        Returns:
            モデル一覧
        """
        try:
            credential_service = get_ai_credential_service()
            credential = credential_service.get_credential(
                organization_id=organization_id,
                user_id=user_id,
                ai_service_id=ai_service_id,
            )

            # 変数を外側で定義
            aws_session = None

            # Bedrock clientを作成
            if ai_service_id == "aws-cache":
                # AWS Login Cache使用（DBから取得したCredentialデータ）
                globals.logger.debug(
                    f"credential_data keys: {list(credential.credential_data.keys())}"
                )

                # credential_dataの内容を確認
                if "idToken" not in credential.credential_data:
                    globals.logger.error(
                        f"credential_data does not contain idToken. "
                        f"Keys found: {list(credential.credential_data.keys())}"
                    )
                    raise ValueError(
                        "AWS Login Cache credential is missing idToken. "
                        "Please re-register with the full cache file content."
                    )

                credential_data = credential.credential_data
                region = credential_data.get("region", "ap-northeast-1")
                aws_session = create_bedrock_session_from_credential_data(
                    credential_data=credential_data,
                    region=region,
                )
                bedrock_client = aws_session._session.client("bedrock")
            else:
                # 手動Credential使用
                credential_data = credential.credential_data
                session = boto3.Session(
                    aws_access_key_id=credential_data.get("access_key_id"),
                    aws_secret_access_key=credential_data.get("secret_access_key"),
                    aws_session_token=credential_data.get("session_token"),
                    region_name=credential_data.get("region", "ap-northeast-1"),
                )
                bedrock_client = session.client(
                    "bedrock",
                    config=Config(
                        connect_timeout=5,
                        read_timeout=120,
                        retries={"max_attempts": 3, "mode": "standard"},
                    ),
                )

            # list_inference_profiles を呼び出し
            response = bedrock_client.list_inference_profiles()

            # モデルリストを整形
            model_list = []
            if "inferenceProfileSummaries" in response:
                for item in response["inferenceProfileSummaries"]:
                    # Anthropicのモデルのみフィルタリング
                    models = item.get("models", [])
                    is_anthropic = any(
                        "anthropic" in model.get("modelArn", "").lower()
                        for model in models
                    )

                    if not is_anthropic:
                        continue

                    # モデル情報を整形
                    model_id = item.get("inferenceProfileId")
                    model_name = item.get("inferenceProfileName", model_id)
                    status = item.get("status", "UNKNOWN")
                    profile_type = item.get("type", "UNKNOWN")

                    model_list.append({
                        "id": model_id,
                        "name": model_name,
                        "description": f"Type: {profile_type} | Status: {status}",
                        "type": profile_type,
                        "status": status,
                        "models": models,
                    })

            globals.logger.debug(
                f"Retrieved {len(model_list)} Bedrock models for "
                f"service={ai_service_id}, org={organization_id}, user={user_id}"
            )

            # 最終使用日時とトークン更新（Bedrock呼び出し後）
            if ai_service_id == "aws-cache" and aws_session:
                # aws-cacheの場合、トークンが自動更新されている可能性がある
                latest_token = aws_session.get_current_token()
                if latest_token:
                    # トークンが更新された場合、Credentialデータも一緒に保存
                    credential_service.update_last_used(
                        credential.credential_id,
                        credential_data=latest_token
                    )
                else:
                    # トークンは更新されていないが、LAST_USED_ATは更新
                    credential_service.update_last_used(credential.credential_id)
            else:
                # bedrock（固定トークン）の場合、LAST_USED_ATのみ更新
                credential_service.update_last_used(credential.credential_id)

            return model_list

        except CredentialNotFound as e:
            globals.logger.error(f"Credential not found: {e}")
            raise

        except Exception as e:
            globals.logger.error(f"Failed to get Bedrock models: {e}", exc_info=True)
            raise


# シングルトンインスタンス
_service_instance = None


def get_model_service() -> ModelService:
    """
    Model Serviceのシングルトンインスタンスを取得

    Returns:
        ModelService
    """
    global _service_instance
    if _service_instance is None:
        _service_instance = ModelService()
    return _service_instance
