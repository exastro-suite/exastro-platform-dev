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
import time
import datetime
import pymysql
import os
import json
from jinja2 import Template
from contextlib import closing
import traceback

import globals
from libs import queries_common

from common_library.common import api_keycloak_server, api_keycloak_tokens, api_keycloak_clients, api_keycloak_realms

WAIT_INTERVAL = 5


def wait_until_connect_to_db(host, user, password, database):
    """wait until connect to db

    Args:
        host (str): database host
        user (str): database user
        password (str): database password
        database (str): database name

    Returns:
        Connection: Database Connection
    """
    start_time = datetime.datetime.now()
    timeout_seconds_connect_db = int(os.environ.get("TIMEOUT_SECONDS_CONNECT_DB", "-1"))

    globals.logger.info(f'WAIT UNTIL CONNECT DATABASE({user}@{host}/{database})...')

    while True:
        try:
            conn = pymysql.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port=3306,
                charset='utf8mb4',
                collation='utf8mb4_general_ci',
                cursorclass=pymysql.cursors.DictCursor,
            )
            break
        except Exception:
            if timeout_seconds_connect_db != -1 and datetime.datetime.now() > start_time + datetime.timedelta(seconds=timeout_seconds_connect_db):
                raise Exception(f"Connection to database timed out : {timeout_seconds_connect_db}s")

            time.sleep(WAIT_INTERVAL)

    return conn


def get_db_data_version(conn, lock=False):
    """ Get Database data version

    Args:
        conn (Connection): Database Connection
        lock (bool, optional): version record lock. Defaults to False.

    Returns:
        str: Database data version
    """
    with conn.cursor() as cursor:

        # Check Exists Version Table Exists
        globals.logger.debug('Check Exists Version Table')
        template = Template(source=queries_common.EXISTS_VERSION_TABLE)
        query = template.render(os.environ)
        globals.logger.debug(f'EXECUTE SQL:{query}')

        cursor.execute(query)
        result = cursor.fetchone()

        if result is None:
            # Not Exists Version Table
            globals.logger.debug('Not Exists Version Table')
            return None

        # Select version table
        globals.logger.debug('Get Version Table')
        if lock:
            template = Template(source=queries_common.SELECT_VERSION_TABLE_LOCK)
        else:
            template = Template(source=queries_common.SELECT_VERSION_TABLE)

        query = template.render(os.environ)
        globals.logger.debug(f'EXECUTE SQL:{query}')

        cursor.execute(query)
        result = cursor.fetchone()

        if result is None:
            # Not Exists Version Table
            globals.logger.debug('Not Exists Version Table Record')
            return None

        return result.get("VERSION")


def update_db_data_version(conn, version, update_user='system'):
    """Update Database data version

    Args:
        conn (Connection): Database Connection
        version (str): version
    """
    with conn.cursor() as cursor:
        globals.logger.info(f'UPDATE DATABASE VERSION : {version}')
        cursor.execute(queries_common.UPDATE_VERSION_TABLE, {"version": version, "last_update_user": update_user})


def insert_migration_history(version, result, message=None, create_user='system'):
    """Insert migration history

    Args:
        version (str): version
        result (str): "START" or "SUCCEED" or "FAILED"
        message (str): Error Message
        create_user (str, optional): user. Defaults to 'system'.
    """
    message_substr = message[:4095] if message is not None else None

    with closing(connect_platform_db()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                queries_common.INSERT_MIGRATION_HISTORY,
                {
                    "version": version,
                    "result": result,
                    "message": message_substr,
                    "create_user": create_user,
                    "last_update_user": create_user
                }
            )
            conn.commit()


def wait_until_keycloak_to_start():
    """wait until keycloak to start
    """
    globals.logger.info('WAIT UNTIL KEYCLOAK TO START ...')

    start_time = datetime.datetime.now()
    timeout_seconds_keycloak_start = int(os.environ.get("TIMEOUT_SECONDS_KEYCLOAK_START", "-1"))

    with closing(connect_platform_db()) as conn:
        informations = __get_platform_informations(conn)

    while True:
        if timeout_seconds_keycloak_start != -1 and datetime.datetime.now() > start_time + datetime.timedelta(seconds=timeout_seconds_keycloak_start):
            raise Exception(f"keycloak start timed out : {timeout_seconds_keycloak_start}s")

        try:
            health_response = api_keycloak_server.health()
            if health_response.status_code != 200:
                time.sleep(WAIT_INTERVAL)
                continue

            use_service_account = informations.get("TOKEN_CHECK_CLIENT_CLIENTID") is not None \
                and informations.get("TOKEN_CHECK_CLIENT_SECRET") is not None

            if use_service_account:
                token_response = api_keycloak_tokens.service_account_get_token(
                    'master',
                    informations.get("TOKEN_CHECK_CLIENT_CLIENTID"),
                    informations.get("TOKEN_CHECK_CLIENT_SECRET"))
            else:
                token_response = __get_admin_cli_token()

            if token_response.status_code != 200:
                globals.logger.debug(f'token_response.status_code:{token_response.status_code}')
                globals.logger.debug(f'token_response.text:{token_response.text}')
                time.sleep(WAIT_INTERVAL)
                continue

            token = json.loads(token_response.text)["access_token"]

            serverinfo_response = api_keycloak_server.serverinfo(token)

            # Keycloak 26.8.2+ rejects Admin API tokens without the kc-admin-api scope.
            # The service account may not have the scope yet (it is added by ensure_admin_api_client_scope), so retry with admin-cli.
            # Keycloak 26.8.2以降はkc-admin-api scopeのないトークンをAdmin APIで拒否する。
            # サービスアカウントにはまだscopeが付与されていない場合があるため(ensure_admin_api_client_scopeで付与)、admin-cliで再試行する
            if serverinfo_response.status_code == 401 and use_service_account:
                globals.logger.debug('serverinfo returned 401 with service account token, retry with admin-cli')
                token_response = __get_admin_cli_token()
                if token_response.status_code == 200:
                    token = json.loads(token_response.text)["access_token"]
                    serverinfo_response = api_keycloak_server.serverinfo(token)

            if serverinfo_response.status_code != 200:
                time.sleep(WAIT_INTERVAL)
                continue

            serverinfo = json.loads(serverinfo_response.text)

            # Match minor version
            if ".".join(serverinfo["systemInfo"]["version"].split(".")[:2]) == os.environ.get("KEYCLOAK_VERSION"):
                break

            time.sleep(WAIT_INTERVAL)

        except Exception as err:
            globals.logger.debug(''.join(list(traceback.TracebackException.from_exception(err).format())))
            time.sleep(WAIT_INTERVAL)
            continue

    globals.logger.info('KEYCLOAK STARTED')
    return


def ensure_admin_api_client_scope():
    """Add kc-admin-api client scope to the service account clients that call the Admin API

        Keycloak 26.8.2+ rejects Admin API tokens without the kc-admin-api scope (401).
        This runs before every migration (idempotent) because migrations of any version may call the Admin API
        with the service account token.
        Keycloak 26.8.2以降はkc-admin-api scopeのないトークンをAdmin APIで拒否する(401)。
        どのバージョンのmigrationもサービスアカウントのトークンでAdmin APIを呼ぶ可能性があるため、migrationの前に毎回実行する(冪等)。
        Ref: https://www.keycloak.org/docs/latest/upgrading/index.html#admin-rest-api-now-enforces-an-audience-check

    Raises:
        Exception: failed to add the scope
    """
    scope_name = "kc-admin-api"

    with closing(connect_platform_db()) as conn:
        informations = __get_platform_informations(conn)

    platform_client_clientid = informations.get("TOKEN_CHECK_CLIENT_CLIENTID")
    if platform_client_clientid is None:
        # 初回インストール時は、クライアント作成時にテンプレートでscopeを付与する
        # On initial install, the scope is assigned by the client template when the client is created
        globals.logger.info(f'SKIP : add {scope_name} client scope : platform client not created yet')
        return

    token_response = __get_admin_cli_token()
    if token_response.status_code != 200:
        raise Exception(f"failed to get admin-cli token : {token_response.status_code} {token_response.text}")
    token = json.loads(token_response.text)["access_token"]

    # master realm: platform service account client / organization realms: organization service account client
    targets = [("master", platform_client_clientid)]
    targets += [(realm_name, f"{realm_name}-workspaces") for realm_name in api_keycloak_realms.get_organization_realms(token)]

    failed = []
    for realm_name, client_id in targets:
        result = api_keycloak_clients.add_default_client_scope_to_client(realm_name, client_id, scope_name, token)
        if result['added']:
            globals.logger.info(f'add {scope_name} client scope : added : realm={realm_name} client={client_id}')
        elif result['skipped']:
            globals.logger.debug(f'add {scope_name} client scope : already exists : realm={realm_name} client={client_id}')
        elif result.get('error') == 'Client not found':
            # 作成途中・削除途中のオーガナイゼーションはクライアントが無いことがあるためスキップする
            # Organizations being created or deleted may not have the client, so skip
            globals.logger.warning(f'add {scope_name} client scope : client not found : realm={realm_name} client={client_id}')
        else:
            globals.logger.error(f'add {scope_name} client scope : failed : realm={realm_name} client={client_id} error={result.get("error")}')
            failed.append(f'{realm_name}/{client_id}')

    if failed:
        raise Exception(f"failed to add {scope_name} client scope : {failed}")


def __get_admin_cli_token():
    """get master realm admin token via admin-cli

    Returns:
        Response: HTTP Response
    """
    return api_keycloak_tokens.client_user_get_token(
        'master',
        'admin-cli',
        None,
        os.environ.get('KEYCLOAK_USER'),
        os.environ.get('KEYCLOAK_PASSWORD'))


def connect_platform_db():
    conn = pymysql.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_DATABASE'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        port=3306,
        charset='utf8mb4',
        collation='utf8mb4_general_ci',
        cursorclass=pymysql.cursors.DictCursor,
    )
    return conn


def get_table_column(conn, table_name, column_name):
    with conn.cursor() as cursor:
        cursor.execute(
            queries_common.SELECT_COLUMN_INFOMATION,
            {
                "table_name": table_name,
                "column_name": column_name
            }
        )
        return cursor.fetchone()


def exists_table_column(conn, table_name, column_name):
    return get_table_column(conn, table_name, column_name) is not None


def __get_platform_informations(conn):

    with conn.cursor() as cursor:

        # Select version table
        globals.logger.debug('Get Platform Informatios Table')
        template = Template(source=queries_common.SELECT_PLATFORM_PRIVATE)

        query = template.render(os.environ)
        globals.logger.debug(f'EXECUTE SQL:{query}')

        cursor.execute(query)
        result = cursor.fetchone()

        if result is None:
            return {}

        return json.loads(result.get("INFORMATIONS", {}))
