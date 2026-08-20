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
AWS Session Manager with Token Auto-Refresh

aws login --remoteのキャッシュファイルを使用して、
自動的にトークンを更新しながらAWSサービスを利用する
"""

import base64
import json
import re
import os
import glob
from typing import Optional

import boto3
import botocore.session
from botocore.credentials import (
    LoginCredentialFetcher,
    LoginRefreshRequired,
    RefreshableCredentials,
)
from botocore.utils import LoginTokenLoader

import globals


class AwsSessionFromToken:
    """
    AWS Login Token からセッションを作成し、自動更新するクラス
    """

    def __init__(
        self,
        token: dict,
        region: str = "ap-northeast-1",
    ):
        """
        Args:
            token: DBから取得したトークン情報
            region: リージョン（省略時はトークンから自動取得）
        """
        self.token: dict = {}
        self._login_session_arn = None
        self._original_token = token.copy()  # 元のトークンを保持
        self._token_updated = False  # トークンが更新されたかのフラグ
        self._token_loader = None  # TokenLoader を保持

        login_session_arn = self._extract_login_session_arn(token)
        token_region = self._extract_login_region(token)
        self._login_session_arn = login_session_arn

        # regionパラメータが指定されていない場合はトークンから取得
        self.region = region if region else token_region

        token_loader = LoginTokenLoader(cache=self.token)
        token_loader.save_token(login_session_arn, token)
        self._token_loader = token_loader  # 後で使うために保持

        botocore_session = botocore.session.Session()

        fetcher = LoginCredentialFetcher(
            session_name=login_session_arn,
            token_loader=token_loader,
            client_creator=botocore_session.create_client,
        )

        cached = fetcher.load_cached_credentials()

        # トークン更新を検知するラッパー
        def refresh_and_mark():
            result = fetcher.refresh_credentials()
            self._token_updated = True  # フラグを立てる
            globals.logger.debug("AWS token refreshed")
            return result

        credentials = RefreshableCredentials(
            access_key=cached["access_key"],
            secret_key=cached["secret_key"],
            token=cached["token"],
            expiry_time=cached["expiry_time"]
            if not isinstance(cached["expiry_time"], str)
            else botocore.credentials._parse_if_needed(cached["expiry_time"]),
            method="login-auto-refresh",
            refresh_using=refresh_and_mark,
            account_id=cached["account_id"],
        )

        botocore_session._credentials = credentials
        botocore_session.set_config_variable("region", self.region)

        self._session = boto3.Session(botocore_session=botocore_session)
        self._refresh_client = None

        globals.logger.debug(
            f"AWS Session initialized: region={self.region}, "
            f"session_arn={login_session_arn}"
        )

    def get_bedrock_client(self):
        """
        Bedrock Runtime クライアントを取得

        Returns:
            boto3.client: bedrock-runtime クライアント
        """
        from botocore.config import Config

        return self._session.client(
            "bedrock-runtime",
            config=Config(
                connect_timeout=5,
                read_timeout=120,
                retries={"max_attempts": 3, "mode": "standard"},
            ),
        )

    def get_current_token(self) -> Optional[dict]:
        """
        メモリ内の最新トークンを取得（トークンが更新された場合のみ）

        Returns:
            dict: 最新のトークン情報（トークンが更新されていない場合はNone）

        Note:
            この関数を呼ぶと、内部の更新フラグがリセットされます。
            次回の refresh_credentials() が呼ばれるまで None を返します。
        """
        if not self._login_session_arn or not self._token_loader:
            return None

        # トークンが更新されていない場合は None を返す
        if not self._token_updated:
            return None

        # LoginTokenLoader を使ってトークンを取得
        try:
            token = self._token_loader.load_token(self._login_session_arn)
        except Exception as e:
            globals.logger.error(f"Failed to load refreshed token: {e}")
            token = None

        # フラグをリセット（次回の更新まで None を返す）
        self._token_updated = False

        return token

    def refresh_token(self) -> bool:
        """
        トークンを明示的に更新

        Returns:
            bool: トークンが更新された場合True

        Raises:
            LoginRefreshRequired: リフレッシュトークンが期限切れの場合
        """
        before_token_str = json.dumps(self.token)

        try:
            # リフレッシュトリガー用のダミー呼び出し
            if self._refresh_client is None:
                self._refresh_client = self._session.client("bedrock")

            self._refresh_client.list_inference_profiles()
        except LoginRefreshRequired:
            globals.logger.error(
                "Refresh token has expired. Run 'aws login --remote' again."
            )
            raise

        after_token_str = json.dumps(self.token)
        refreshed = (before_token_str != after_token_str)

        if refreshed:
            globals.logger.debug("AWS token refreshed successfully")

        return refreshed

    def _extract_login_session_arn(self, token: dict) -> str:
        """idTokenのsubクレームからlogin_session ARNを取り出す"""
        claims = self._decode_id_token(token["idToken"])
        return claims["sub"]

    def _extract_login_region(self, token: dict) -> str:
        """idTokenのissクレーム(https://<region>.signin.aws.amazon.com/signin)からregionを取り出す"""
        claims = self._decode_id_token(token["idToken"])
        match = re.match(r"https://([a-z0-9-]+)\.signin\.aws\.amazon\.com", claims["iss"])
        if not match:
            raise ValueError(f"issからregionを抽出できません: {claims['iss']}")
        return match.group(1)

    def _decode_id_token(self, id_token: str) -> dict:
        """idToken(JWT)のペイロード部分を署名検証なしでデコード"""
        payload_b64 = id_token.split(".")[1]
        padded = payload_b64 + "=" * (-len(payload_b64) % 4)
        return json.loads(base64.urlsafe_b64decode(padded))


def load_latest_login_cache(cache_dir: Optional[str] = None) -> dict:
    """
    ~/.aws/login/cache/ から最新のキャッシュファイルを読み込む

    Args:
        cache_dir: キャッシュディレクトリパス（省略時は~/.aws/login/cache/）

    Returns:
        dict: トークン情報

    Raises:
        FileNotFoundError: キャッシュファイルが見つからない
    """
    if cache_dir is None:
        cache_dir = os.path.expanduser("~/.aws/login/cache")

    cache_files = glob.glob(os.path.join(cache_dir, "*.json"))

    if not cache_files:
        raise FileNotFoundError(
            f"AWS login cache not found in {cache_dir}. "
            "Run 'aws login --remote' first."
        )

    # 最新のファイルを取得
    latest_cache = max(cache_files, key=os.path.getmtime)

    globals.logger.debug(f"Loading AWS login cache from: {latest_cache}")

    with open(latest_cache, "r") as f:
        token = json.load(f)

    return token


def create_bedrock_session_from_cache(
    cache_dir: Optional[str] = None,
    region: str = "ap-northeast-1"
) -> AwsSessionFromToken:
    """
    キャッシュファイルからBedrockセッションを作成

    非推奨: create_bedrock_session_from_credential_data() を使用してください

    Args:
        cache_dir: キャッシュディレクトリパス
        region: リージョン

    Returns:
        AwsSessionFromToken: セッションオブジェクト
    """
    token = load_latest_login_cache(cache_dir)
    return AwsSessionFromToken(token, region)


def create_bedrock_session_from_credential_data(
    credential_data: dict,
    region: str = "ap-northeast-1",
) -> AwsSessionFromToken:
    """
    DBから取得したCredentialデータからBedrockセッションを作成

    Args:
        credential_data: T_USER_AWS_CREDENTIALから取得したトークン情報
                        （ENCRYPTED_CREDENTIAL_DATAを復号化したもの）
        region: リージョン

    Returns:
        AwsSessionFromToken: セッションオブジェクト

    Raises:
        ValueError: credential_dataにidTokenが含まれていない場合

    Note:
        トークンが自動更新された場合、メモリ内（aws_session.token）に保存されます。
        呼び出し側で aws_session.get_current_token() を使って最新トークンを取得し、
        update_last_used(credential_data=latest_token) でDBに保存してください。
    """
    if "idToken" not in credential_data:
        raise ValueError(
            "credential_data must contain 'idToken'. "
            "Make sure the data is from AWS Login Cache."
        )

    return AwsSessionFromToken(
        token=credential_data,
        region=region,
    )
