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
AI Router

AIモデル利用許可判定とプロバイダー選択
"""

from typing import Optional, Dict, Any
from contextlib import closing

from common_library.common.db import DBconnector
from libs import queries_ai_permissions as queries

import globals


class AIModelNotAllowed(Exception):
    """AIモデル利用不可"""
    pass


class AIServiceNotFound(Exception):
    """AIサービスが見つからない"""
    pass


class AIRouter:
    """
    AI Router

    - ユーザーのモデル利用許可判定
    - AWS権限とExastro権限の二段階チェック
    """

    def __init__(self):
        pass

    def validate_model_permission(
        self,
        organization_id: str,
        user_id: str,
        ai_service_id: str,
        model_id: str,
        capability: str,
    ) -> bool:
        """
        モデル利用許可をチェック

        Args:
            organization_id: Organization ID
            user_id: User ID
            ai_service_id: AIサービスID (例: bedrock)
            model_id: モデルID
            capability: 用途 (例: chat)

        Returns:
            bool: 利用可能ならTrue

        Raises:
            AIModelNotAllowed: 利用不可
        """
        with closing(DBconnector().connect_platformdb()) as conn:
            with closing(conn.cursor()) as cursor:
                # T_USER_AI_MODEL_PERMISSIONをチェック
                cursor.execute(
                    queries.SQL_SELECT_USER_MODEL_PERMISSION,
                    (
                        organization_id,
                        user_id,
                        ai_service_id,
                        model_id,
                        capability,
                    )
                )
                permission = cursor.fetchone()

                if not permission:
                    globals.logger.warning(
                        f"AI model not allowed: "
                        f"org={organization_id}, user={user_id}, "
                        f"service={ai_service_id}, model={model_id}, "
                        f"capability={capability}"
                    )
                    raise AIModelNotAllowed(
                        f"Model {model_id} is not allowed for user {user_id} "
                        f"with capability {capability}"
                    )

                globals.logger.debug(
                    f"AI model permission validated: "
                    f"org={organization_id}, user={user_id}, "
                    f"model={model_id}, capability={capability}"
                )
                return True

    def get_allowed_models(
        self,
        organization_id: str,
        user_id: str,
        ai_service_id: str,
    ) -> list:
        """
        ユーザーが利用可能なモデル一覧を取得

        Args:
            organization_id: Organization ID
            user_id: User ID
            ai_service_id: AIサービスID

        Returns:
            list: モデル一覧
        """
        with closing(DBconnector().connect_platformdb()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    queries.SQL_SELECT_USER_ALLOWED_MODELS,
                    (organization_id, user_id, ai_service_id)
                )
                models = cursor.fetchall()

                globals.logger.debug(
                    f"Retrieved allowed models: "
                    f"org={organization_id}, user={user_id}, "
                    f"service={ai_service_id}, count={len(models)}"
                )
                return models

    def get_service_configuration(self, ai_service_id: str) -> Dict[str, Any]:
        """
        AIサービス設定を取得

        Args:
            ai_service_id: AIサービスID

        Returns:
            Dict: サービス設定

        Raises:
            AIServiceNotFound: サービスが見つからない
        """
        with closing(DBconnector().connect_platformdb()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    """
                    SELECT
                        AI_SERVICE_ID,
                        SERVICE_NAME,
                        PROVIDER_TYPE,
                        ENABLED,
                        CONFIGURATION
                    FROM
                        T_AI_SERVICE_DEFINITION
                    WHERE
                        AI_SERVICE_ID = %s
                        AND ENABLED = TRUE
                    """,
                    (ai_service_id,)
                )
                service = cursor.fetchone()

                if not service:
                    raise AIServiceNotFound(
                        f"AI service not found or disabled: {ai_service_id}"
                    )

                return service

    def get_model_configuration(
        self,
        ai_service_id: str,
        model_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        AIモデル設定を取得

        Args:
            ai_service_id: AIサービスID
            model_id: モデルID

        Returns:
            Dict: モデル設定 (見つからない場合はNone)
        """
        with closing(DBconnector().connect_platformdb()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    """
                    SELECT
                        MODEL_DEFINITION_ID,
                        AI_SERVICE_ID,
                        MODEL_ID,
                        MODEL_NAME,
                        MODEL_VERSION,
                        CAPABILITIES,
                        ENABLED,
                        CONFIGURATION
                    FROM
                        T_AI_MODEL_DEFINITION
                    WHERE
                        AI_SERVICE_ID = %s
                        AND MODEL_ID = %s
                        AND ENABLED = TRUE
                    """,
                    (ai_service_id, model_id)
                )
                return cursor.fetchone()


# グローバルインスタンス
_global_ai_router = AIRouter()


def get_ai_router() -> AIRouter:
    """
    グローバルAIRouterを取得

    Returns:
        AIRouter: インスタンス
    """
    return _global_ai_router
