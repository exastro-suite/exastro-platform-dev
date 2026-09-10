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
AI Preference Service

ユーザーごとのAI利用設定（デフォルトAIサービス・デフォルトモデル・ピックアップモデル）の管理
"""

import json
from typing import Optional, List
from dataclasses import dataclass
from contextlib import closing

from common_library.common.db import DBconnector
from libs import queries_ai_assistant

import globals


@dataclass
class AiPreference:
    """User AI Preference（AIサービス単位）"""
    ai_service_id: str
    model_id: str
    model_name: Optional[str]
    pickup_model_ids: List[str]


class AiPreferenceService:
    """
    AI Preference Service

    ユーザーごと・AIサービスごとのAI利用設定を管理
    """

    def get_preference(
        self,
        organization_id: str,
        user_id: str,
        ai_service_id: str,
    ) -> Optional[AiPreference]:
        """
        AI利用設定を取得

        Args:
            organization_id: Organization ID (DB接続用、テーブルには保存しない)
            user_id: User ID
            ai_service_id: AIサービスID

        Returns:
            AiPreference。一度も保存されていない場合はNone
        """
        with closing(DBconnector().connect_orgdb(organization_id)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    queries_ai_assistant.SQL_SELECT_USER_AI_PREFERENCE,
                    {"user_id": user_id, "ai_service_id": ai_service_id},
                )
                row = cursor.fetchone()

        if not row:
            return None

        try:
            pickup_model_ids = json.loads(row["PICKUP_MODEL_IDS"])
        except (json.JSONDecodeError, TypeError):
            # 保存内容が破損していてもエラーにせず空配列扱いにする（Credentialのget_latest_message等と同じ方針）
            # Treat corrupted content as an empty array instead of raising (same policy as e.g. message history parsing)
            pickup_model_ids = []

        return AiPreference(
            ai_service_id=ai_service_id,
            model_id=row["MODEL_ID"],
            model_name=row["MODEL_NAME"],
            pickup_model_ids=pickup_model_ids,
        )

    def save_preference(
        self,
        organization_id: str,
        user_id: str,
        ai_service_id: str,
        model_id: str,
        pickup_model_ids: List[str],
        model_name: Optional[str] = None,
    ) -> None:
        """
        AI利用設定を保存（全置換。既存設定があれば上書き、無ければ新規作成）

        Args:
            organization_id: Organization ID (DB接続用、テーブルには保存しない)
            user_id: User ID
            ai_service_id: AIサービスID
            model_id: デフォルトで使用するモデルID
            pickup_model_ids: UIで選択肢を絞り込むためのモデルID一覧
            model_name: デフォルトモデルの表示名（任意。クライアントが渡した値をそのまま保存する）
        """
        with closing(DBconnector().connect_orgdb(organization_id)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    queries_ai_assistant.SQL_UPSERT_USER_AI_PREFERENCE,
                    {
                        "user_id": user_id,
                        "ai_service_id": ai_service_id,
                        "model_id": model_id,
                        "model_name": model_name,
                        "pickup_model_ids": json.dumps(pickup_model_ids, ensure_ascii=False),
                    },
                )
                conn.commit()

        globals.logger.debug(
            f"AI preference saved: user={user_id}, ai_service_id={ai_service_id}, "
            f"model={model_id}, model_name={model_name}, pickup_count={len(pickup_model_ids)}"
        )


# シングルトンインスタンス
_service_instance: Optional[AiPreferenceService] = None


def get_ai_preference_service() -> AiPreferenceService:
    """
    AI Preference Serviceのシングルトンインスタンスを取得

    Returns:
        AiPreferenceService
    """
    global _service_instance
    if _service_instance is None:
        _service_instance = AiPreferenceService()
    return _service_instance
