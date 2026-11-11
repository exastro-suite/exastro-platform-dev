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

import pytest

import os
import os.path
import connexion
import requests
import json
import subprocess
import socket
from unittest import mock

from flask import request
import logging
from logging.config import dictConfig as dictLogConf

from tests.common import test_common
import globals
from common_library.common.exastro_logging import ExastroLogRecordFactory, LOGGING
from common_library.common.db import DBconnector
from common_library.common import api_keycloak_tokens, api_keycloak_realms, multi_lang
from common_resources.en import language

# unittest用のkeycloakとDBはproxyを経由しないように設定
for env_var in ['no_proxy', 'NO_PROXY']:
    current_value = os.environ.get(env_var, '')
    unittest_hosts = ['unittest-keycloak', 'unittest-platform-db']
    hosts_to_add = [host for host in unittest_hosts if host not in current_value]
    if hosts_to_add:
        new_value = ','.join([current_value] + hosts_to_add) if current_value else ','.join(hosts_to_add)
        os.environ[env_var] = new_value


#: notification宛先url(Webhook/Teams/ServiceNow)のテスト用サンプルホスト名 -> 解決させたいダミーのグローバルIP
MOCKED_DESTINATION_HOSTS = {
    "example.com": "8.8.8.8",
    "dev999999.service-now.com": "8.8.8.8",
}


@pytest.fixture(autouse=True)
def mock_destination_host_resolution(mocker):
    """notification宛先url(Webhook/Teams/ServiceNow)のホスト名解決をモック化

    テスト用のサンプルURLに含まれるホスト名(dev999999.service-now.com等)は実在しないため、
    SSRF対策(validation.is_webhook_host_allowed)の名前解決(socket.getaddrinfo)が
    実DNSに依存しないよう、MOCKED_DESTINATION_HOSTSに列挙したホスト名のみグローバルIPに解決されるようモックする。
    それ以外のホスト名(unittest-platform-db等、DB/Keycloak接続に必要なもの含む)は実際のsocket.getaddrinfoに
    フォールバックする(socket.getaddrinfoをホスト名問わず広く上書きすると、テスト基盤自体のDB/Keycloak接続まで
    巻き込んで壊れるため)。
    全テストファイルに適用するため、個々のテストファイルではなくconftest.pyに定義している。
    private/予約IPへの解決やDNS失敗を確認するテストでは、patch_getaddrinfo_forで個別に上書きする。

    Args:
        mocker (obj): mocker
    """
    real_getaddrinfo = socket.getaddrinfo

    def fake_getaddrinfo(host, *args, **kwargs):
        if host in MOCKED_DESTINATION_HOSTS:
            ip = MOCKED_DESTINATION_HOSTS[host]
            return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (ip, 0))]
        return real_getaddrinfo(host, *args, **kwargs)

    mocker.patch('socket.getaddrinfo', side_effect=fake_getaddrinfo)


def patch_getaddrinfo_for(overrides):
    """指定したホスト名のみ名前解決を上書きし、それ以外は実際のsocket.getaddrinfoにフォールバックするpatcherを返す

    is_webhook_host_allowedは許可リスト取得のためにDB接続(unittest-platform-dbの名前解決)を行うため、
    socket.getaddrinfoを全ホスト一括で上書きすると、DB接続自体が壊れてテストが失敗する。
    そのため、テスト対象のホスト名のみを個別に差し替える。

    Args:
        overrides (dict): {hostname: [ip, ...]} で解決させたいIPのリストを指定、
            または {hostname: 例外クラス/例外インスタンス} でDNS解決失敗を再現する

    Returns:
        unittest.mock._patch: mock.patchオブジェクト(with文で使用する)
    """
    real_getaddrinfo = socket.getaddrinfo

    def fake_getaddrinfo(host, *args, **kwargs):
        if host in overrides:
            target = overrides[host]
            if (isinstance(target, type) and issubclass(target, BaseException)) or isinstance(target, BaseException):
                raise target
            return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (ip, 0)) for ip in target]
        return real_getaddrinfo(host, *args, **kwargs)

    return mock.patch('socket.getaddrinfo', side_effect=fake_getaddrinfo)


@pytest.fixture(scope='session')
def connexion_client():
    """flask connexion test client 取得

    Returns:
        FlaskClient: _description_
    """
    app_root_dir = os.path.dirname(os.path.dirname(__file__))

    connexion_app = connexion.FlaskApp(
        __name__,
        specification_dir=f'{app_root_dir}/swagger/',
        server_args={'template_folder': '../templates'})

    connexion_app.add_api('swagger.yaml')

    app = connexion_app.app
    globals.init(app)

    org_factory = logging.getLogRecordFactory()
    logging.setLogRecordFactory(ExastroLogRecordFactory(org_factory, request))
    globals.logger = logging.getLogger('root')
    dictLogConf(LOGGING)

    globals.logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))

    return connexion_app.app.test_client()


@pytest.fixture(scope="session")
def docker_compose_command() -> str:
    """pytest-docker docker-composeコマンド設定

    Returns:
        str: docker composeコマンド
    """
    if os.environ.get('DOCKER_COMPOSE_UP_UNITTEST_NODE', 'MANUAL') == 'AUTO':
        return "sudo docker compose "
    else:
        return ":"


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig, autouse=True):
    """pytest-docker docker-compose.ymlファイル指定

    Args:
        pytestconfig (_type_): pytestconfig fixtureパラメータ
        autouse (bool, optional): fixture自動起動=true

    Returns:
        str: docker-compose.ymlファイルパス
    """
    return os.path.join(os.path.dirname(__file__), "docker-compose.yml")


@pytest.fixture(scope='session', autouse=True)
def docker_compose_up(docker_ip, docker_services):
    """docker compose起動

    Args:
        docker_ip (_type_): docker_ip fixtureパラメータ
        docker_services (_type_): docker_services fixtureパラメータ
    """
    if os.environ.get('DOCKER_COMPOSE_UP_UNITTEST_NODE', 'MANUAL') == 'AUTO':
        #
        # Keycloakの起動待ち
        #
        docker_services.wait_until_responsive(
            timeout=300.0,
            pause=1.0,
            check=lambda: is_responsive(f"{test_common.keycloak_origin()}/auth/health"))


def is_responsive(url):
    """http get通信確認

    Args:
        url (str): URL

    Returns:
        bool: 通信結果
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except Exception:
        return False


@pytest.fixture(scope='function', autouse=True)
def data_initalize():
    """データー初期化

    """
    #
    # keycloak token取得
    #
    private = DBconnector().get_platform_private()
    resp_token = api_keycloak_tokens.service_account_get_token(
        private.token_check_realm_id, private.token_check_client_clientid, private.token_check_client_secret)
    if resp_token.status_code != 200:
        raise Exception('FAILED : get keycloak token (tests/conftest.py data_initalize)')

    token = json.loads(resp_token.text).get("access_token")

    #
    # realm一覧取得
    #
    resp_realms = api_keycloak_realms.realms_get(token)
    if resp_realms.status_code != 200:
        raise Exception('FAILED : get keycloak realms (tests/conftest.py data_initalize)')

    #
    # 全レルムキャッシュクリア
    #
    keycloak_api_origin = f"{os.environ['API_KEYCLOAK_PROTOCOL']}://{os.environ['API_KEYCLOAK_HOST']}:{os.environ['API_KEYCLOAK_PORT']}"
    for realm in json.loads(resp_realms.text):
        resp_cache_clear = requests.post(
            f"{keycloak_api_origin}/auth/admin/realms/{realm['realm']}/clear-realm-cache",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
            json={"realm": realm['realm']})

        if resp_cache_clear.status_code < 200 and resp_cache_clear.status_code > 299:
            raise Exception('FAILED : clear keycloak realms cache (tests/conftest.py data_initalize)')

        resp_cache_clear = requests.post(
            f"{keycloak_api_origin}/auth/admin/realms/{realm['realm']}/clear-user-cache",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
            json={"realm": realm['realm']})

        if resp_cache_clear.status_code < 200 and resp_cache_clear.status_code > 299:
            raise Exception('FAILED : clear keycloak user cache (tests/conftest.py data_initalize)')

        resp_cache_clear = requests.post(
            f"{keycloak_api_origin}/auth/admin/realms/{realm['realm']}/clear-keys-cache",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
            json={"realm": realm['realm']})

        if resp_cache_clear.status_code < 200 and resp_cache_clear.status_code > 299:
            raise Exception('FAILED : clear keycloak key cache (tests/conftest.py data_initalize)')
    #
    # データ初期化(platform_db/keycloak)
    #
    sql_file = os.path.join(os.path.dirname(__file__), "db", "exports", "pytest2_restore_data.sql")
    result_command = subprocess.run(
        f"mysql -u {os.environ['DB_ADMIN_USER']} -p{os.environ['DB_ADMIN_PASSWORD']} -h {os.environ['DB_HOST']} < {sql_file}",
        shell=True)

    if result_command.returncode != 0:
        raise Exception('FAILED : mysql command (tests/conftest.py data_initalize)')

    #
    # organization, workspace database drop
    #
    result_command = subprocess.run(
        f"mysql -u {os.environ['DB_ADMIN_USER']} -p{os.environ['DB_ADMIN_PASSWORD']} -h {os.environ['DB_HOST']} -N -e 'show databases;'" +
        " | sed -n -e '/^PF_\\(ORG\\|WS\\)_/{s/^/DROP DATABASE /;s/$/;/p}'" +
        f" | mysql -u {os.environ['DB_ADMIN_USER']} -p{os.environ['DB_ADMIN_PASSWORD']} -h {os.environ['DB_HOST']}",
        shell=True)

    if result_command.returncode != 0:
        raise Exception('FAILED : mysql command (tests/conftest.py data_initalize)')


@pytest.fixture(autouse=True)
def multi_lang_get_text(mocker):
    """multi_lang.get_textモック
        unit testではLanguage textが登録されていない場合、エラーを引き起こします

    Args:
        mocker (obj): mocker

    Returns:
        _type_: _description_
    """
    multi_lang_get_text = multi_lang.get_text

    def mocked_function(text_id, origin_text, *args):
        if text_id is not None and text_id != '000-00000':
            assert text_id in language.LanguageList.lang_array, f'Check lang_array Text id : {text_id}'
        return multi_lang_get_text(text_id, origin_text, *args)

    mocker.patch.object(multi_lang, 'get_text', side_effect=mocked_function)
