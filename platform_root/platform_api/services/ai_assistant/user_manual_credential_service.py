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
User Manual Credential Service

ユーザーが手動で登録したAWS Credentialの管理
UIから入力されたCredentialをDBに暗号化して保存
"""

from typing import Optional, List, Dict
from contextlib import closing
from datetime import datetime
import ulid

from common_library.common import encrypt
from common_library.common.db import DBconnector

import boto3
from botocore.exceptions import ClientError

import globals


class AwsRoleCredential:
    """AWS認証情報を保持するクラス"""
    def __init__(
        self,
        access_key_id: str,
        secret_access_key: str,
        session_token: Optional[str] = None,
        region: str = "ap-northeast-1"
    ):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.session_token = session_token
        self.region = region


class CredentialNotFound(Exception):
    """Credentialが見つからない"""
    pass


class CredentialValidationError(Exception):
    """Credential検証エラー"""
    pass


class UserManualCredentialService:
    """
    User Manual Credential Service

    ユーザーが手動で登録したAWS Credentialの管理
    """

    def register_credential(
        self,
        organization_id: str,
        user_id: str,
        credential_name: str,
        access_key_id: str,
        secret_access_key: str,
        session_token: Optional[str] = None,
        aws_region: str = "ap-northeast-1",
        bedrock_region: str = "ap-northeast-1",
        expires_at: Optional[datetime] = None,
        notes: Optional[str] = None,
    ) -> str:
        """
        AWS Credentialを登録

        Args:
            organization_id: Organization ID
            user_id: User ID
            credential_name: Credential識別名
            access_key_id: AWS Access Key ID
            secret_access_key: AWS Secret Access Key
            session_token: Session Token (オプション)
            aws_region: AWSリージョン
            bedrock_region: Bedrockリージョン
            expires_at: 有効期限
            notes: 備考

        Returns:
            str: Credential ID

        Raises:
            CredentialValidationError: 検証エラー
        """
        credential_id = ulid.new().str

        # Credentialを検証
        validation_result = self._validate_credential(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            session_token=session_token,
            region=aws_region,
        )

        if not validation_result["valid"]:
            raise CredentialValidationError(
                f"Credential validation failed: {validation_result.get('error')}"
            )

        # 暗号化
        encrypted_access_key = encrypt.encrypt_str(access_key_id)
        encrypted_secret_key = encrypt.encrypt_str(secret_access_key)
        encrypted_session_token = (
            encrypt.encrypt_str(session_token) if session_token else None
        )

        with closing(DBconnector().connect_platformdb()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    """
                    INSERT INTO T_USER_AWS_CREDENTIAL
                    (
                        CREDENTIAL_ID, ORGANIZATION_ID, USER_ID, CREDENTIAL_NAME,
                        ENCRYPTED_ACCESS_KEY_ID, ENCRYPTED_SECRET_ACCESS_KEY,
                        ENCRYPTED_SESSION_TOKEN, AWS_REGION, BEDROCK_REGION,
                        STATUS, EXPIRES_AT, LAST_VALIDATED_AT, NOTES,
                        CREATE_TIMESTAMP, CREATE_USER,
                        LAST_UPDATE_TIMESTAMP, LAST_UPDATE_USER
                    )
                    VALUES
                    (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, 'active', %s, NOW(), %s,
                        NOW(), %s, NOW(), %s
                    )
                    """,
                    (
                        credential_id,
                        organization_id,
                        user_id,
                        credential_name,
                        encrypted_access_key,
                        encrypted_secret_key,
                        encrypted_session_token,
                        aws_region,
                        bedrock_region,
                        expires_at,
                        notes,
                        user_id,
                        user_id,
                    ),
                )
                conn.commit()

        globals.logger.info(
            f"AWS Credential registered: id={credential_id}, "
            f"org={organization_id}, user={user_id}, name={credential_name}"
        )

        return credential_id

    def list_credentials(
        self,
        organization_id: str,
        user_id: str,
        status: Optional[str] = None,
    ) -> List[Dict]:
        """
        Credential一覧を取得

        Args:
            organization_id: Organization ID
            user_id: User ID
            status: ステータスフィルター (オプション)

        Returns:
            List[Dict]: Credential一覧（平文のCredentialは含まない）
        """
        with closing(DBconnector().connect_platformdb()) as conn:
            with closing(conn.cursor()) as cursor:
                if status:
                    cursor.execute(
                        """
                        SELECT
                            CREDENTIAL_ID, CREDENTIAL_NAME, AWS_REGION, BEDROCK_REGION,
                            STATUS, EXPIRES_AT, LAST_VALIDATED_AT, LAST_USED_AT,
                            NOTES, CREATE_TIMESTAMP, LAST_UPDATE_TIMESTAMP
                        FROM T_USER_AWS_CREDENTIAL
                        WHERE ORGANIZATION_ID = %s AND USER_ID = %s AND STATUS = %s
                        ORDER BY CREATE_TIMESTAMP DESC
                        """,
                        (organization_id, user_id, status),
                    )
                else:
                    cursor.execute(
                        """
                        SELECT
                            CREDENTIAL_ID, CREDENTIAL_NAME, AWS_REGION, BEDROCK_REGION,
                            STATUS, EXPIRES_AT, LAST_VALIDATED_AT, LAST_USED_AT,
                            NOTES, CREATE_TIMESTAMP, LAST_UPDATE_TIMESTAMP
                        FROM T_USER_AWS_CREDENTIAL
                        WHERE ORGANIZATION_ID = %s AND USER_ID = %s
                        ORDER BY CREATE_TIMESTAMP DESC
                        """,
                        (organization_id, user_id),
                    )

                credentials = cursor.fetchall()

                globals.logger.info(
                    f"Listed {len(credentials)} credentials: "
                    f"org={organization_id}, user={user_id}"
                )

                return credentials

    def get_bedrock_credential(
        self,
        organization_id: str,
        user_id: str,
        credential_id: Optional[str] = None,
    ) -> AwsRoleCredential:
        """
        Bedrock用のAWS Credentialを取得

        Args:
            organization_id: Organization ID
            user_id: User ID
            credential_id: Credential ID (省略時は最新のactiveを使用)

        Returns:
            AwsRoleCredential: AWS Credential

        Raises:
            CredentialNotFound: Credentialが見つからない
        """
        with closing(DBconnector().connect_platformdb()) as conn:
            with closing(conn.cursor()) as cursor:
                if credential_id:
                    cursor.execute(
                        """
                        SELECT
                            CREDENTIAL_ID, ENCRYPTED_ACCESS_KEY_ID,
                            ENCRYPTED_SECRET_ACCESS_KEY, ENCRYPTED_SESSION_TOKEN,
                            EXPIRES_AT, STATUS
                        FROM T_USER_AWS_CREDENTIAL
                        WHERE CREDENTIAL_ID = %s AND ORGANIZATION_ID = %s AND USER_ID = %s
                        """,
                        (credential_id, organization_id, user_id),
                    )
                else:
                    # 最新のactiveなCredentialを取得
                    cursor.execute(
                        """
                        SELECT
                            CREDENTIAL_ID, ENCRYPTED_ACCESS_KEY_ID,
                            ENCRYPTED_SECRET_ACCESS_KEY, ENCRYPTED_SESSION_TOKEN,
                            EXPIRES_AT, STATUS
                        FROM T_USER_AWS_CREDENTIAL
                        WHERE ORGANIZATION_ID = %s AND USER_ID = %s AND STATUS = 'active'
                        ORDER BY CREATE_TIMESTAMP DESC
                        LIMIT 1
                        """,
                        (organization_id, user_id),
                    )

                credential = cursor.fetchone()

                if not credential:
                    raise CredentialNotFound(
                        f"AWS Credential not found: org={organization_id}, user={user_id}"
                    )

                # 復号化
                access_key_id = encrypt.decrypt_str(credential["ENCRYPTED_ACCESS_KEY_ID"])
                secret_access_key = encrypt.decrypt_str(
                    credential["ENCRYPTED_SECRET_ACCESS_KEY"]
                )
                session_token = (
                    encrypt.decrypt_str(credential["ENCRYPTED_SESSION_TOKEN"])
                    if credential["ENCRYPTED_SESSION_TOKEN"]
                    else None
                )

                # 最終使用日時を更新
                cursor.execute(
                    """
                    UPDATE T_USER_AWS_CREDENTIAL
                    SET LAST_USED_AT = NOW(), LAST_UPDATE_TIMESTAMP = NOW()
                    WHERE CREDENTIAL_ID = %s
                    """,
                    (credential["CREDENTIAL_ID"],),
                )
                conn.commit()

                globals.logger.info(
                    f"Retrieved AWS Credential: id={credential['CREDENTIAL_ID']}, "
                    f"org={organization_id}, user={user_id}"
                )

                return AwsRoleCredential(
                    access_key_id=access_key_id,
                    secret_access_key=secret_access_key,
                    session_token=session_token,
                    region="ap-northeast-1",  # デフォルトリージョン
                )

    def validate_credential(
        self,
        organization_id: str,
        user_id: str,
        credential_id: str,
    ) -> Dict:
        """
        Credentialを検証

        Args:
            organization_id: Organization ID
            user_id: User ID
            credential_id: Credential ID

        Returns:
            Dict: 検証結果
        """
        with closing(DBconnector().connect_platformdb()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    """
                    SELECT
                        ENCRYPTED_ACCESS_KEY_ID, ENCRYPTED_SECRET_ACCESS_KEY,
                        ENCRYPTED_SESSION_TOKEN, AWS_REGION
                    FROM T_USER_AWS_CREDENTIAL
                    WHERE CREDENTIAL_ID = %s AND ORGANIZATION_ID = %s AND USER_ID = %s
                    """,
                    (credential_id, organization_id, user_id),
                )
                credential = cursor.fetchone()

                if not credential:
                    raise CredentialNotFound(f"Credential not found: {credential_id}")

                # 復号化
                access_key_id = encrypt.decrypt_str(credential["ENCRYPTED_ACCESS_KEY_ID"])
                secret_access_key = encrypt.decrypt_str(
                    credential["ENCRYPTED_SECRET_ACCESS_KEY"]
                )
                session_token = (
                    encrypt.decrypt_str(credential["ENCRYPTED_SESSION_TOKEN"])
                    if credential["ENCRYPTED_SESSION_TOKEN"]
                    else None
                )

                # 検証
                result = self._validate_credential(
                    access_key_id=access_key_id,
                    secret_access_key=secret_access_key,
                    session_token=session_token,
                    region=credential["AWS_REGION"],
                )

                # 検証結果をDBに保存
                cursor.execute(
                    """
                    UPDATE T_USER_AWS_CREDENTIAL
                    SET
                        LAST_VALIDATED_AT = NOW(),
                        STATUS = %s,
                        VALIDATION_ERROR = %s,
                        LAST_UPDATE_TIMESTAMP = NOW()
                    WHERE CREDENTIAL_ID = %s
                    """,
                    (
                        "active" if result["valid"] else "expired",
                        result.get("error"),
                        credential_id,
                    ),
                )
                conn.commit()

                globals.logger.info(
                    f"Validated credential: id={credential_id}, "
                    f"valid={result['valid']}"
                )

                return result

    def delete_credential(
        self,
        organization_id: str,
        user_id: str,
        credential_id: str,
    ):
        """
        Credentialを削除

        Args:
            organization_id: Organization ID
            user_id: User ID
            credential_id: Credential ID
        """
        with closing(DBconnector().connect_platformdb()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    """
                    DELETE FROM T_USER_AWS_CREDENTIAL
                    WHERE CREDENTIAL_ID = %s AND ORGANIZATION_ID = %s AND USER_ID = %s
                    """,
                    (credential_id, organization_id, user_id),
                )
                conn.commit()

                globals.logger.info(
                    f"Deleted credential: id={credential_id}, "
                    f"org={organization_id}, user={user_id}"
                )

    def _validate_credential(
        self,
        access_key_id: str,
        secret_access_key: str,
        session_token: Optional[str],
        region: str,
    ) -> Dict:
        """
        CredentialをAWS APIで検証

        Args:
            access_key_id: Access Key ID
            secret_access_key: Secret Access Key
            session_token: Session Token
            region: リージョン

        Returns:
            Dict: {"valid": bool, "identity": dict, "error": str}
        """
        try:
            session = boto3.Session(
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                aws_session_token=session_token,
                region_name=region,
            )

            sts = session.client("sts")
            identity = sts.get_caller_identity()

            globals.logger.info(
                f"Credential validation succeeded: "
                f"account={identity.get('Account')}, "
                f"arn={identity.get('Arn')}"
            )

            return {
                "valid": True,
                "identity": {
                    "user_id": identity.get("UserId"),
                    "account": identity.get("Account"),
                    "arn": identity.get("Arn"),
                },
                "error": None,
            }

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "")
            error_message = e.response.get("Error", {}).get("Message", str(e))

            globals.logger.error(
                f"Credential validation failed: "
                f"error_code={error_code}, error={error_message}"
            )

            return {
                "valid": False,
                "identity": None,
                "error": f"{error_code}: {error_message}",
            }

        except Exception as e:
            globals.logger.error(f"Unexpected validation error: {e}", exc_info=True)
            return {
                "valid": False,
                "identity": None,
                "error": str(e),
            }


# グローバルインスタンス
_global_manual_credential_service = UserManualCredentialService()


def get_manual_credential_service() -> UserManualCredentialService:
    """
    グローバルManualCredentialServiceを取得

    Returns:
        UserManualCredentialService: インスタンス
    """
    return _global_manual_credential_service
