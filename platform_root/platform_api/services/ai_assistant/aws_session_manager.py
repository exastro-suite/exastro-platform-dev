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

    def __init__(self, token: dict, region: str = "ap-northeast-1"):
        """
        Args:
            token: aws loginのキャッシュファイルから読み込んだトークン
            region: リージョン（省略時はトークンから自動取得）
        """
        self.token: dict = {}

        login_session_arn = self._login_session_arn(token)
        token_region = self._login_region(token)

        # regionパラメータが指定されていない場合はトークンから取得
        self.region = region if region else token_region

        token_loader = LoginTokenLoader(cache=self.token)
        token_loader.save_token(login_session_arn, token)

        botocore_session = botocore.session.Session()

        fetcher = LoginCredentialFetcher(
            session_name=login_session_arn,
            token_loader=token_loader,
            client_creator=botocore_session.create_client,
        )

        cached = fetcher.load_cached_credentials()

        credentials = RefreshableCredentials(
            access_key=cached["access_key"],
            secret_key=cached["secret_key"],
            token=cached["token"],
            expiry_time=cached["expiry_time"]
            if not isinstance(cached["expiry_time"], str)
            else botocore.credentials._parse_if_needed(cached["expiry_time"]),
            method="login-auto-refresh",
            refresh_using=fetcher.refresh_credentials,
            account_id=cached["account_id"],
        )

        botocore_session._credentials = credentials
        botocore_session.set_config_variable("region", self.region)

        self._session = boto3.Session(botocore_session=botocore_session)
        self._refresh_client = None

        globals.logger.info(
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
            globals.logger.info("AWS token refreshed successfully")

        return refreshed

    def _login_session_arn(self, token: dict) -> str:
        """idTokenのsubクレームからlogin_session ARNを取り出す"""
        claims = self._decode_id_token(token["idToken"])
        return claims["sub"]

    def _login_region(self, token: dict) -> str:
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

    globals.logger.info(f"Loading AWS login cache from: {latest_cache}")

    with open(latest_cache, "r") as f:
        token = json.load(f)

    return token


def create_bedrock_session_from_cache(
    cache_dir: Optional[str] = None,
    region: str = "ap-northeast-1"
) -> AwsSessionFromToken:
    """
    キャッシュファイルからBedrockセッションを作成

    Args:
        cache_dir: キャッシュディレクトリパス
        region: リージョン

    Returns:
        AwsSessionFromToken: セッションオブジェクト
    """
    token = load_latest_login_cache(cache_dir)
    return AwsSessionFromToken(token, region)
