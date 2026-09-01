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
AI Credential Service

汎用AIサービスのCredential管理（Bedrock, OpenAI, Anthropic, etc.）
"""

import json
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from contextlib import closing
from datetime import datetime
import ulid

from common_library.common.db import DBconnector
from common_library.common import encrypt
from libs import queries_ai_assistant

import globals


@dataclass
class AiCredential:
    """AI Service Credential"""
    credential_id: str
    ai_service_id: str
    credential_name: str
    credential_data: Dict[str, Any]  # JSON形式のCredentialデータ
    status: str
    expires_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None


class CredentialNotFound(Exception):
    """Credentialが見つからない"""
    pass


class AiCredentialService:
    """
    AI Credential Service

    汎用AIサービスのCredential管理
    """

    def register_credential(
        self,
        organization_id: str,
        user_id: str,
        ai_service_id: str,
        credential_name: str,
        credential_data: Dict[str, Any],
        notes: Optional[str] = None,
    ) -> str:
        """
        Credentialを登録

        Args:
            organization_id: Organization ID (DB接続用、テーブルには保存しない)
            user_id: User ID
            ai_service_id: AIサービスID (bedrock, openai, anthropic, etc.)
            credential_name: Credential名
            credential_data: Credentialデータ（JSON形式）
            notes: 備考

        Returns:
            credential_id: 登録されたCredential ID
        """
        credential_id = ulid.new().str

        # Credentialデータを暗号化
        credential_json = json.dumps(credential_data)
        encrypted_data = encrypt.encrypt_str(credential_json)

        # expires_atを抽出（存在する場合）
        expires_at = None
        if "expires_at" in credential_data:
            try:
                expires_at = datetime.fromisoformat(
                    credential_data["expires_at"].replace("Z", "+00:00")
                )
            except Exception as e:
                globals.logger.warning(f"Failed to parse expires_at: {e}")

        with closing(DBconnector().connect_orgdb(organization_id)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    queries_ai_assistant.SQL_INSERT_USER_CREDENTIAL,
                    {
                        "credential_id": credential_id,
                        "user_id": user_id,
                        "ai_service_id": ai_service_id,
                        "credential_name": credential_name,
                        "encrypted_credential_data": encrypted_data,
                        "expires_at": expires_at,
                        "notes": notes,
                    },
                )
                conn.commit()

        globals.logger.debug(
            f"AI Credential registered: id={credential_id}, "
            f"service={ai_service_id}, user={user_id}"
        )

        return credential_id

    def get_credential(
        self,
        organization_id: str,
        user_id: str,
        ai_service_id: str,
        credential_id: Optional[str] = None,
    ) -> AiCredential:
        """
        Credentialを取得

        Args:
            organization_id: Organization ID (DB接続用、テーブルには保存しない)
            user_id: User ID
            ai_service_id: AIサービスID
            credential_id: Credential ID（省略時は最新のactiveなものを取得）

        Returns:
            AiCredential

        Raises:
            CredentialNotFound: Credentialが見つからない
        """
        with closing(DBconnector().connect_orgdb(organization_id)) as conn:
            with closing(conn.cursor()) as cursor:
                if credential_id:
                    # 特定のCredentialを取得
                    cursor.execute(
                        queries_ai_assistant.SQL_SELECT_USER_CREDENTIAL_BY_ID,
                        {
                            "credential_id": credential_id,
                            "user_id": user_id,
                            "ai_service_id": ai_service_id,
                        },
                    )
                else:
                    # 最新のactiveなCredentialを取得
                    cursor.execute(
                        queries_ai_assistant.SQL_SELECT_USER_ACTIVE_CREDENTIAL_BY_SERVICE,
                        {
                            "user_id": user_id,
                            "ai_service_id": ai_service_id,
                        },
                    )

                row = cursor.fetchone()

                if not row:
                    raise CredentialNotFound(
                        f"Credential not found: service={ai_service_id}, "
                        f"user={user_id}"
                    )

                # Credentialデータを復号化
                encrypted_data = row["ENCRYPTED_CREDENTIAL_DATA"]
                decrypted_json = encrypt.decrypt_str(encrypted_data)
                credential_data = json.loads(decrypted_json)

                return AiCredential(
                    credential_id=row["CREDENTIAL_ID"],
                    ai_service_id=row["AI_SERVICE_ID"],
                    credential_name=row["CREDENTIAL_NAME"],
                    credential_data=credential_data,
                    status=row["STATUS"],
                    expires_at=row["EXPIRES_AT"],
                    last_used_at=row["LAST_USED_AT"],
                )

    def list_credentials(
        self,
        organization_id: str,
        user_id: str,
        ai_service_id: str,
        status: Optional[str] = None,
    ) -> List[Dict]:
        """
        Credential一覧を取得

        Args:
            organization_id: Organization ID (DB接続用、テーブルには保存しない)
            user_id: User ID
            ai_service_id: AIサービスID
            status: ステータスフィルター

        Returns:
            Credential一覧（Credentialデータは含まない）
        """
        with closing(DBconnector().connect_orgdb(organization_id)) as conn:
            with closing(conn.cursor()) as cursor:
                if status:
                    cursor.execute(
                        queries_ai_assistant.SQL_LIST_USER_CREDENTIALS_WITH_STATUS,
                        {
                            "user_id": user_id,
                            "ai_service_id": ai_service_id,
                            "status": status,
                        },
                    )
                else:
                    cursor.execute(
                        queries_ai_assistant.SQL_LIST_USER_CREDENTIALS,
                        {
                            "user_id": user_id,
                            "ai_service_id": ai_service_id,
                        },
                    )

                rows = cursor.fetchall()
                return rows

    def delete_credential(
        self,
        organization_id: str,
        user_id: str,
        ai_service_id: str,
        credential_id: str,
    ) -> bool:
        """
        Credentialを削除

        Args:
            organization_id: Organization ID (DB接続用、テーブルには保存しない)
            user_id: User ID
            ai_service_id: AIサービスID
            credential_id: Credential ID

        Returns:
            削除成功したかどうか
        """
        with closing(DBconnector().connect_orgdb(organization_id)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    queries_ai_assistant.SQL_DELETE_USER_CREDENTIAL,
                    {
                        "credential_id": credential_id,
                        "user_id": user_id,
                    },
                )
                deleted = cursor.rowcount > 0
                conn.commit()

        if deleted:
            globals.logger.debug(
                f"AI Credential deleted: id={credential_id}, "
                f"service={ai_service_id}, user={user_id}"
            )

        return deleted

    def update_credential(
        self,
        organization_id: str,
        user_id: str,
        ai_service_id: str,
        credential_id: str,
        credential_name: Optional[str] = None,
        credential_data: Optional[Dict] = None,
        notes: Optional[str] = None,
    ) -> bool:
        """
        Credentialを更新（部分更新）

        Args:
            organization_id: Organization ID (DB接続用、テーブルには保存しない)
            user_id: User ID
            ai_service_id: AIサービスID
            credential_id: Credential ID
            credential_name: Credential名（任意）
            credential_data: Credentialデータ（任意）
            notes: 備考（任意）

        Returns:
            更新成功したかどうか
        """
        with closing(DBconnector().connect_orgdb(organization_id)) as conn:
            with closing(conn.cursor()) as cursor:
                # 更新するフィールドを動的に構築
                update_fields = []
                params = []

                if credential_name is not None:
                    update_fields.append("CREDENTIAL_NAME = %s")
                    params.append(credential_name)

                if credential_data is not None:
                    # Credentialデータを暗号化
                    credential_json = json.dumps(credential_data)
                    encrypted_data = encrypt.encrypt_str(credential_json)
                    update_fields.append("ENCRYPTED_CREDENTIAL_DATA = %s")
                    params.append(encrypted_data)

                if notes is not None:
                    update_fields.append("NOTES = %s")
                    params.append(notes)

                # 共通の更新フィールド
                update_fields.append("LAST_UPDATE_TIMESTAMP = NOW(6)")
                update_fields.append("LAST_UPDATE_USER = %s")
                params.append(user_id)

                # WHERE句のパラメータ
                params.extend([credential_id, user_id, ai_service_id])

                query = f"""
                    UPDATE T_USER_AI_CREDENTIAL
                    SET {', '.join(update_fields)}
                    WHERE CREDENTIAL_ID = %s
                      AND USER_ID = %s
                      AND AI_SERVICE_ID = %s
                """

                cursor.execute(query, params)
                updated = cursor.rowcount > 0
                conn.commit()

        if updated:
            globals.logger.debug(
                f"AI Credential updated: id={credential_id}, "
                f"service={ai_service_id}, user={user_id}, "
                f"fields={[k.split('=')[0].strip() for k in update_fields if '=' in k]}"
            )

        return updated

    def update_last_used(
        self,
        organization_id: str,
        credential_id: str,
        credential_data: Optional[dict] = None,
    ) -> None:
        """
        最終使用日時を更新（オプションでCredentialデータも更新）

        Args:
            organization_id: Organization ID (DB接続用、テーブルには保存しない)
            credential_id: Credential ID
            credential_data: 更新するCredentialデータ（Noneの場合は最終使用日時のみ更新）
                           bedrock-cacheの場合、トークン自動更新後の最新データを渡す
        """
        with closing(DBconnector().connect_orgdb(organization_id)) as conn:
            with closing(conn.cursor()) as cursor:
                if credential_data:
                    # Credentialデータと最終使用日時を更新
                    encrypted_data = encrypt.encrypt_str(json.dumps(credential_data))

                    cursor.execute(
                        queries_ai_assistant.SQL_UPDATE_CREDENTIAL_DATA_AND_LAST_USED,
                        {
                            "encrypted_credential_data": encrypted_data,
                            "credential_id": credential_id,
                        },
                    )

                    globals.logger.debug(
                        f"Updated credential data and last_used: credential_id={credential_id}"
                    )
                else:
                    # 最終使用日時のみ更新
                    cursor.execute(
                        queries_ai_assistant.SQL_UPDATE_CREDENTIAL_LAST_USED,
                        {"credential_id": credential_id},
                    )

                    globals.logger.debug(
                        f"Updated last_used only: credential_id={credential_id}"
                    )

                conn.commit()


# シングルトンインスタンス
_service_instance: Optional[AiCredentialService] = None


def get_ai_credential_service() -> AiCredentialService:
    """
    AI Credential Serviceのシングルトンインスタンスを取得

    Returns:
        AiCredentialService
    """
    global _service_instance
    if _service_instance is None:
        _service_instance = AiCredentialService()
    return _service_instance
