# Copyright 2022 NEC Corporation#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
WSGI main module
"""
# from crypt import methods
from flask import Flask, request, jsonify, make_response
import os
import requests
from datetime import datetime
from dotenv import load_dotenv  # python-dotenv
import logging
from logging.config import dictConfig as dictLogConf
from flask_log_request_id import RequestID
import inspect
import traceback
from pathlib import Path

# User Imports
import globals
import common_library.common.common as common
import common_library.common.maintenancemode as maintenancemode
from common_library.common.exastro_logging import ExastroLogRecordFactory, LOGGING
from common_library.common.db import DBconnector
from common_library.common import multi_lang
import auth_proxy

from audit_logging import audit_getLogger

# load environ variables
load_dotenv(override=True)

# 設定ファイル読み込み・globals初期化
# Read configuration file and initialize globals
app = Flask(__name__)
globals.init(app)


org_factory = logging.getLogRecordFactory()
logging.setLogRecordFactory(ExastroLogRecordFactory(org_factory, request))
globals.logger = logging.getLogger('root')
dictLogConf(LOGGING)

globals.logger.setLevel(os.getenv('LOG_LEVEL'))

RequestID(app)

audit_path = Path('/var/log/exastro')

# 監査ログのLogger設定
globals.audit = audit_getLogger('audit',
                                audit_path.joinpath(os.getenv('AUDIT_LOG_PATH')),
                                os.getenv('AUDIT_LOG_ENABLED').lower() == 'true',
                                int(os.getenv('AUDIT_LOG_FILE_MAX_BYTE')),
                                int(os.getenv('AUDIT_LOG_BACKUP_COUNT')))


@app.route('/health-check/liveness', methods=["GET"])
@common.platform_exception_handler
def liveness():
    """health check - liveness

    Returns:
        Response: HTTP Response
    """
    return "OK", 200


@app.route('/health-check/readness', methods=["GET"])
@common.platform_exception_handler
def readness():
    """health check - readness

    Returns:
        Response: HTTP Response
    """
    return "OK", 200


@app.route('/auth/realms/<string:organization_id>/protocol/openid-connect/token', methods=["POST"])
@common.platform_exception_handler
def openid_connect_token(organization_id):
    """get token
    Args:
        organization_id (str): organization id
    Returns:
        Response: HTTP Response
    """

    # proxy destination
    if (request.form.get('client_id') == f"_{organization_id}-api" or (organization_id == 'master' and request.form.get('client_id') == '_platform-api')) \
        and request.form.get('grant_type') == 'password' \
            and 'offline_access' in request.form.get('scope'):
        # case get refresh token
        # call platform api
        proxy_location_origin = f"{os.environ['PLATFORM_API_PROTOCOL']}://{os.environ['PLATFORM_API_HOST']}:{os.environ['PLATFORM_API_PORT']}"
    else:
        # case other
        # call keycloak
        proxy_location_origin = f"{os.environ['KEYCLOAK_PROTOCOL']}://{os.environ['KEYCLOAK_HOST']}:{os.environ['KEYCLOAK_PORT']}"

    redirect_response = requests.post(
        f"{proxy_location_origin}/auth/realms/{organization_id}/protocol/openid-connect/token",
        data=request.form,
        headers={"Content-Type": request.content_type, "User-Id": "-"},
    )

    # remake response header
    excluded_headers = ['content-encoding', 'content-length', 'connection', 'keep-alive', 'proxy-authenticate',
                        'proxy-authorization', 'te', 'trailers', 'transfer-encoding', 'upgrade']
    headers = {
        k: v for k, v in redirect_response.raw.headers.items()
        if k.lower() not in excluded_headers
    }

    # 戻り値をそのまま返却
    # Return the return value as it is
    response = make_response()
    response.status_code = redirect_response.status_code
    response.data = redirect_response.content
    response.headers = headers

    return response


@app.route('/api/platform/<path:subpath>', methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTION"])
@common.platform_exception_handler
def platform_organization_api_call(subpath):
    """Call the platform organization API after authorization - 認可後にplatform APIを呼び出します

    Args:
        subpath (str): subpath

    Returns:
        Response: HTTP Response
    """
    try:
        extra = extra_init()
        globals.logger.info(f"### start func:{inspect.currentframe().f_code.co_name} {request.method=} {subpath=}")

        # Destination URL settings - 宛先URLの設定
        dest_url = "{}://{}:{}/api/platform/{}".format(
            os.environ['PLATFORM_API_PROTOCOL'], os.environ['PLATFORM_API_HOST'], os.environ['PLATFORM_API_PORT'], subpath)

        # return jsonify({"result": "200", "time": str(datetime.now())}), 200

        # Common authorization proxy processing call - 共通の認可proxy処理呼び出し

        # サービスアカウントを使うためにClientのSercretを取得
        # Get Client Sercret to use service account
        db = DBconnector()
        private = db.get_platform_private()

        # 取得できない場合は、エラー
        # If you cannot get it, an error
        if not private:
            message_id = "500-11002"
            message = multi_lang.get_text(
                message_id, "platform private情報の取得に失敗しました")
            extra['status_code'] = 500
            extra['message_id'] = message_id
            extra['message_text'] = message
            globals.audit.info('audit: error.', extra=extra)
            raise common.InternalErrorException(message_id=message_id, message=message)

        # realm名設定
        # Set realm name
        proxy = auth_proxy.auth_proxy(
            private.token_check_realm_id,
            private.token_check_client_clientid,
            private.token_check_client_secret,
            private.token_check_client_clientid,
            private.token_check_client_secret)

        # 各種チェック check
        response_json = proxy.check_authorization()

        extra['user_id'] = response_json.get("user_info").get("user_id")
        extra['username'] = response_json.get("user_info").get("username")
        extra['request_user_headers'] = response_json.get("data")

        # api呼び出し call api
        return_api = proxy.call_api(dest_url, response_json.get("data"))

        extra['status_code'] = return_api.status_code

        # 戻り値をそのまま返却
        # Return the return value as it is
        response = make_response()
        response.status_code = return_api.status_code
        response.data = return_api.content
        for key, value in return_api.headers.items():
            if key.lower().startswith('content-'):
                response.headers[key] = value

        globals.audit.info(f'audit: response. {response.status_code}', extra=extra)
        globals.logger.info(f"### end func:{inspect.currentframe().f_code.co_name} {response.status_code=}")

        return response

    except common.AuthException as e:
        globals.logger.info(f'authentication error:{e.args}')
        message_id = "401-00002"
        message = multi_lang.get_text(message_id, "認証に失敗しました。")
        extra['status_code'] = 401
        extra['message_id'] = message_id
        extra['message_text'] = message
        globals.audit.info(f'audit: authentication error. {e.args=}', extra=extra)
        raise common.AuthException(message_id=message_id, message=message)

    except common.NotAllowedException as e:
        globals.logger.info(f'permission error:{e.args}')
        message_id = "403-00001"
        info = common.multi_lang.get_text(message_id, "permission error")
        extra['status_code'] = 403
        extra['message_id'] = message_id
        extra['message_text'] = info
        globals.audit.info(f'audit: permission error. {e.args=}', extra=extra)
        raise common.NotAllowedException(message_id=message_id, message=info)

    except Exception as e:
        globals.logger.error(f'exception error:{e.args}')
        extra['status_code'] = 500
        globals.audit.error(f'audit: Exception error.[{e=}], [{type(e)=}]:', stack_info=''.join(list(traceback.TracebackException.from_exception(e).format())), extra=extra)
        return common.response_server_error(e)


def extra_init(organization_id='-', workspace_id='-'):
    """extra fields initialize

    Args:
        organization_id(str) : organization id
        workspace_id(str) : workspace id

    Returns:
        extra(dict): extra items
    """
    extra = {
        'ts': common.datetime_to_str(datetime.now()),
        'user_id': '-',
        'username': '-',
        'org_id': organization_id,
        'ws_id': workspace_id,
        'method': request.method,
        'full_path': request.full_path,
        'access_route': request.access_route,
        'remote_addr': request.remote_addr,
        'request_headers': request.headers,
        'request_user_headers': '-',
        'content_type': '-',
        'status_code': '-',
        'message_id': '-',
        'message_text': '-',
    }

    # パラメータを形成
    # Form parameters
    if request.is_json:
        try:
            extra['request_body'] = request.json.copy()
        except Exception:
            pass

    # パラメータを形成(multipart/form-data)
    # form parameters, files parameters
    if request.form:
        try:
            extra['request_form'] = request.form.copy()
        except Exception:
            pass
    if request.files:
        try:
            extra['request_files'] = request.files.copy()
        except Exception:
            pass

    # content-type
    if request.content_type:
        extra['content_type'] = request.content_type.lower()

    return extra


@app.route('/api/ita/<path:subpath>', methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTION"])
@common.platform_exception_handler
def ita_admin_api_call(subpath):
    """Call the ita admin API after authorization - 認可後にita admin APIを呼び出します

    Args:
        subpath (str): subpath

    Returns:
        Response: HTTP Response
    """
    try:
        extra = extra_init()
        globals.logger.info(f"### start func:{inspect.currentframe().f_code.co_name} {request.method=} {subpath=}")

        # Destination URL settings - 宛先URLの設定
        dest_url = "{}://{}:{}/api/ita/{}".format(
            os.environ['ITA_API_ADMIN_PROTOCOL'], os.environ['ITA_API_ADMIN_HOST'], os.environ['ITA_API_ADMIN_PORT'], subpath)

        # return jsonify({"result": "200", "time": str(datetime.now())}), 200

        # メンテナンスモード(DATA_UPDATE_STOP)中、GET以外は、エラー
        # During maintenance mode (data_update_stop), except for GET, error
        mode_name = "data_update_stop"
        target_name = "Exastro IT Automation API (System Management)"
        maintenance_mode = maintenancemode.maintenace_mode_get(mode_name)
        if maintenance_mode == "1" and request.method != "GET":
            message_id = "498-00001"
            message = multi_lang.get_text(
                message_id,
                "メンテナンス中の為、{}は利用出来ません。({}:/api/ita/{})",
                target_name, request.method, subpath
            )
            info = 'MaintenanceMode({}:{})'.format(mode_name, maintenance_mode)
            extra['status_code'] = 498
            extra['message_id'] = message_id
            extra['message_text'] = message
            globals.audit.info('audit: maintenance.', extra=extra)
            raise common.MaintenanceException(info, message_id=message_id, message=message)

        # Common authorization proxy processing call - 共通の認可proxy処理呼び出し

        # サービスアカウントを使うためにClientのSercretを取得
        # Get Client Sercret to use service account
        db = DBconnector()
        private = db.get_platform_private()

        # 取得できない場合は、エラー
        # If you cannot get it, an error
        if not private:
            message_id = "500-11002"
            message = multi_lang.get_text(
                message_id, "platform private情報の取得に失敗しました")
            extra['status_code'] = 500
            extra['message_id'] = message_id
            extra['message_text'] = message
            globals.audit.info('audit: error.', extra=extra)
            raise common.InternalErrorException(essage_id=message_id, message=message)

        # realm名設定
        # Set realm name
        proxy = auth_proxy.auth_proxy(
            private.token_check_realm_id,
            private.token_check_client_clientid,
            private.token_check_client_secret,
            private.token_check_client_clientid,
            private.token_check_client_secret)

        # 各種チェック check
        response_json = proxy.check_authorization()

        extra['user_id'] = response_json.get("user_info").get("user_id")
        extra['username'] = response_json.get("user_info").get("username")
        extra['request_user_headers'] = response_json.get("data")

        # api呼び出し call api
        return_api = proxy.call_api(dest_url, response_json.get("data"))

        extra['status_code'] = return_api.status_code

        # 戻り値をそのまま返却
        # Return the return value as it is
        response = make_response()
        response.status_code = return_api.status_code
        response.data = return_api.content
        for key, value in return_api.headers.items():
            if key.lower().startswith('content-'):
                response.headers[key] = value

        globals.audit.info(f'audit: response. {response.status_code}', extra=extra)
        globals.logger.info(f"### end func:{inspect.currentframe().f_code.co_name} {response.status_code=}")

        return response

    except common.AuthException as e:
        globals.logger.error(f'authentication error:{e.args}')
        message_id = "401-00002"
        message = multi_lang.get_text(message_id, "認証に失敗しました。")
        extra['status_code'] = 401
        extra['message_id'] = message_id
        extra['message_text'] = message
        globals.audit.info(f'audit: authentication error. {e.args=}', extra=extra)
        raise common.AuthException(message_id=message_id, message=message)

    except common.NotAllowedException as e:
        globals.logger.info(f'permission error:{e.args}')
        message_id = "403-00001"
        info = common.multi_lang.get_text(message_id, "permission error")
        extra['status_code'] = 403
        extra['message_id'] = message_id
        extra['message_text'] = info
        globals.audit.info(f'audit: permission error. {e.args=}', extra=extra)
        raise common.NotAllowedException(message_id=message_id, message=info)

    except common.MaintenanceException as e:
        globals.logger.info(f'under maintenance:{e.args}')
        raise e

    except Exception as e:
        globals.logger.error(f'exception error:{e.args}')
        extra['status_code'] = 500
        globals.audit.error(f'audit: Exception error.[{e=}], [{type(e)=}]:', stack_info=''.join(list(traceback.TracebackException.from_exception(e).format())), extra=extra)
        return common.response_server_error(e)


@app.route('/api/<string:organization_id>/platform/<path:subpath>', methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTION"])
@common.platform_exception_handler
def platform_api_call(organization_id, subpath):
    """Call the platform API after authorization - 認可後にplatform APIを呼び出します

    Args:
        subpath (str): subpath

    Returns:
        Response: HTTP Response
    """
    try:
        extra = extra_init(organization_id=organization_id)
        globals.logger.info(f"### start func:{inspect.currentframe().f_code.co_name} {request.method=} {subpath=} {organization_id=}")

        # Destination URL settings - 宛先URLの設定
        dest_url = "{}://{}:{}/api/{}/platform/{}".format(
            os.environ['PLATFORM_API_PROTOCOL'], os.environ['PLATFORM_API_HOST'], os.environ['PLATFORM_API_PORT'], organization_id, subpath)

        # return jsonify({"result": "200", "time": str(datetime.now())}), 200

        # Common authorization proxy processing call - 共通の認可proxy処理呼び出し

        # サービスアカウントを使うためにClientのSercretを取得
        # Get Client Sercret to use service account
        db = DBconnector()
        private = db.get_organization_private(organization_id)

        # 取得できない場合は、エラー
        # If you cannot get it, an error
        if not private:
            message_id = "500-11001"
            message = multi_lang.get_text(message_id,
                                          "organization private情報の取得に失敗しました")
            extra['status_code'] = 500
            extra['message_id'] = message_id
            extra['message_text'] = message
            globals.audit.info('audit: error.', extra=extra)
            raise common.InternalErrorException(essage_id=message_id, message=message)

        # organization idをrealm名として設定
        # Set organization id as realm name
        proxy = auth_proxy.auth_proxy(organization_id,
                                      private.token_check_client_clientid,
                                      private.token_check_client_secret,
                                      private.user_token_client_clientid,
                                      None)

        # 各種チェック check
        response_json = proxy.check_authorization()

        extra['user_id'] = response_json.get("user_info").get("user_id")
        extra['username'] = response_json.get("user_info").get("username")
        extra['request_user_headers'] = response_json.get("data")

        # api呼び出し call api
        return_api = proxy.call_api(dest_url, response_json.get("data"))

        extra['status_code'] = return_api.status_code

        # 戻り値をそのまま返却
        # Return the return value as it is
        response = make_response()
        response.status_code = return_api.status_code
        response.data = return_api.content
        for key, value in return_api.headers.items():
            if key.lower().startswith('content-'):
                response.headers[key] = value

        globals.audit.info(f'audit: response. {response.status_code}', extra=extra)
        globals.logger.info(f"### end func:{inspect.currentframe().f_code.co_name} {response.status_code=}")

        return response

    except common.NotFoundException:
        raise

    except common.AuthException as e:
        globals.logger.error(f'authentication error:{e.args}')
        message_id = "401-00002"
        message = multi_lang.get_text(message_id, "認証に失敗しました。")
        extra['status_code'] = 401
        extra['message_id'] = message_id
        extra['message_text'] = message
        globals.audit.info(f'audit: authentication error. {e.args=}', extra=extra)
        raise common.AuthException(message_id=message_id, message=message)

    except common.NotAllowedException as e:
        globals.logger.info(f'permission error:{e.args}')
        message_id = "403-00001"
        info = common.multi_lang.get_text(message_id, "permission error")
        extra['status_code'] = 403
        extra['message_id'] = message_id
        extra['message_text'] = info
        globals.audit.info(f'audit: permission error. {e.args=}', extra=extra)
        raise common.NotAllowedException(message_id=message_id, message=info)

    except Exception as e:
        globals.logger.error(f'exception error:{e.args}')
        extra['status_code'] = 500
        globals.audit.error(f'audit: Exception error.[{e=}], [{type(e)=}]:', stack_info=''.join(list(traceback.TracebackException.from_exception(e).format())), extra=extra)
        return common.response_server_error(e)


@app.route('/api/<string:organization_id>/workspaces/<string:workspace_id>/ita/<path:subpath>', methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTION"])  # noqa: E501
@common.platform_exception_handler
def ita_workspace_api_call(organization_id, workspace_id, subpath):
    """Call the IT-automation API after authorization - 認可後にIT-automation APIを呼び出します

    Args:
        organization_id (str): organization id
        workspace_id (str): workspace id
        subpath (str): subpath

    Returns:
        Response: HTTP Response
    """
    try:
        extra = extra_init(organization_id=organization_id, workspace_id=workspace_id)
        globals.logger.info(f"### start func:{inspect.currentframe().f_code.co_name} {request.method=} {subpath=} {organization_id=} {workspace_id=}")

        # Destination URL settings - 宛先URLの設定
        dest_url = "{}://{}:{}/api/{}/workspaces/{}/ita/{}".format(
            os.environ['ITA_API_PROTOCOL'], os.environ['ITA_API_HOST'], os.environ['ITA_API_PORT'], organization_id, workspace_id, subpath)

        # サービスアカウントを使うためにClientのSercretを取得
        # Get Client Sercret to use service account
        db = DBconnector()
        private = db.get_organization_private(organization_id)

        # 取得できない場合は、エラー
        # If you cannot get it, an error
        if not private:
            message_id = "500-11001"
            message = multi_lang.get_text(message_id,
                                          "organization private情報の取得に失敗しました")
            extra['status_code'] = 500
            extra['message_id'] = message_id
            extra['message_text'] = message
            globals.audit.info('audit: error.', extra=extra)
            raise common.InternalErrorException(essage_id=message_id, message=message)

        # organization idをrealm名として設定
        # Set organization id as realm name
        proxy = auth_proxy.auth_proxy(organization_id,
                                      private.token_check_client_clientid,
                                      private.token_check_client_secret,
                                      private.user_token_client_clientid,
                                      None)

        # 各種チェック check
        response_json = proxy.check_authorization()

        extra['user_id'] = response_json.get("user_info").get("user_id")
        extra['username'] = response_json.get("user_info").get("username")
        extra['request_user_headers'] = response_json.get("data")

        # api呼び出し call api
        return_api = proxy.call_api(dest_url, response_json.get("data"))

        extra['status_code'] = return_api.status_code

        # 戻り値をそのまま返却
        # Return the return value as it is
        response = make_response()
        response.status_code = return_api.status_code
        response.data = return_api.content
        for key, value in return_api.headers.items():
            if key.lower().startswith('content-'):
                response.headers[key] = value

        globals.audit.info(f'audit: response. {response.status_code}', extra=extra)
        globals.logger.info(f"### end func:{inspect.currentframe().f_code.co_name} {response.status_code=}")

        return response

    except common.NotFoundException:
        raise

    except common.AuthException as e:
        globals.logger.error(f'authentication error:{e.args}')
        message_id = "401-00002"
        message = multi_lang.get_text(message_id, "認証に失敗しました。")
        extra['status_code'] = 401
        extra['message_id'] = message_id
        extra['message_text'] = message
        globals.audit.info(f'audit: authentication error. {e.args=}', extra=extra)
        raise common.AuthException(message_id=message_id, message=message)

    except common.NotAllowedException as e:
        globals.logger.info(f'permission error:{e.args}')
        message_id = "403-00001"
        info = common.multi_lang.get_text(message_id, "permission error")
        extra['status_code'] = 403
        extra['message_id'] = message_id
        extra['message_text'] = info
        globals.audit.info(f'audit: permission error. {e.args=}', extra=extra)
        raise common.NotAllowedException(message_id=message_id, message=info)

    except Exception as e:
        globals.logger.error(f'exception error:{e.args}')
        extra['status_code'] = 500
        globals.audit.error(f'audit: Exception error.[{e=}], [{type(e)=}]:', stack_info=''.join(list(traceback.TracebackException.from_exception(e).format())), extra=extra)
        return common.response_server_error(e)


@app.route('/api/<string:organization_id>/workspaces/<string:workspace_id>/oase_agent/<path:subpath>', methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTION"])  # noqa: E501
@common.platform_exception_handler
def ita_oase_recever_api_call(organization_id, workspace_id, subpath):
    """Call the IT-automation OASE RECIVER API after authorization - 認可後にIT-automation OASE RECIVER APIを呼び出します

    Args:
        organization_id (str): organization id
        workspace_id (str): workspace id
        subpath (str): subpath

    Returns:
        Response: HTTP Response
    """
    try:
        extra = extra_init(organization_id=organization_id, workspace_id=workspace_id)
        globals.logger.info(f"### start func:{inspect.currentframe().f_code.co_name} {request.method=} {subpath=} {organization_id=} {workspace_id=}")

        # Destination URL settings - 宛先URLの設定
        dest_url = "{}://{}:{}/api/{}/workspaces/{}/oase_agent/{}".format(
            os.environ['ITA_API_OASE_RECEIVER_PROTOCOL'], os.environ['ITA_API_OASE_RECEIVER_HOST'], os.environ['ITA_API_OASE_RECEIVER_PORT'], organization_id, workspace_id, subpath)

        # サービスアカウントを使うためにClientのSercretを取得
        # Get Client Sercret to use service account
        db = DBconnector()
        private = db.get_organization_private(organization_id)

        # 取得できない場合は、エラー
        # If you cannot get it, an error
        if not private:
            message_id = "500-11001"
            message = multi_lang.get_text(message_id,
                                          "organization private情報の取得に失敗しました")
            extra['status_code'] = 500
            extra['message_id'] = message_id
            extra['message_text'] = message
            globals.audit.info('audit: error.', extra=extra)
            raise common.InternalErrorException(essage_id=message_id, message=message)

        # organization idをrealm名として設定
        # Set organization id as realm name
        proxy = auth_proxy.auth_proxy(organization_id,
                                      private.token_check_client_clientid,
                                      private.token_check_client_secret,
                                      private.user_token_client_clientid,
                                      None)

        # 各種チェック check
        response_json = proxy.check_authorization()

        extra['user_id'] = response_json.get("user_info").get("user_id")
        extra['username'] = response_json.get("user_info").get("username")
        extra['request_user_headers'] = response_json.get("data")

        # api呼び出し call api
        return_api = proxy.call_api(dest_url, response_json.get("data"))

        extra['status_code'] = return_api.status_code

        # 戻り値をそのまま返却
        # Return the return value as it is
        response = make_response()
        response.status_code = return_api.status_code
        response.data = return_api.content
        for key, value in return_api.headers.items():
            if key.lower().startswith('content-'):
                response.headers[key] = value

        globals.audit.info(f'audit: response. {response.status_code}', extra=extra)
        globals.logger.info(f"### end func:{inspect.currentframe().f_code.co_name} {response.status_code=}")

        return response

    except common.NotFoundException:
        raise

    except common.AuthException as e:
        globals.logger.info(f'authentication error:{e.args}')
        message_id = "401-00002"
        message = multi_lang.get_text(message_id, "認証に失敗しました。")
        extra['status_code'] = 401
        extra['message_id'] = message_id
        extra['message_text'] = message
        globals.audit.info(f'audit: authentication error. {e.args=}', extra=extra)
        raise common.AuthException(message_id=message_id, message=message)

    except common.NotAllowedException as e:
        globals.logger.info(f'permission error:{e.args}')
        message_id = "403-00001"
        info = common.multi_lang.get_text(message_id, "permission error")
        extra['status_code'] = 403
        extra['message_id'] = message_id
        extra['message_text'] = info
        globals.audit.info(f'audit: permission error. {e.args=}', extra=extra)
        raise common.NotAllowedException(message_id=message_id, message=info)

    except Exception as e:
        globals.logger.error(f'exception error:{e.args}')
        extra['status_code'] = 500
        globals.audit.error(f'audit: Exception error.[{e=}], [{type(e)=}]:', stack_info=''.join(list(traceback.TracebackException.from_exception(e).format())), extra=extra)
        return common.response_server_error(e)


if __name__ == '__main__':
    app.run(
        debug=(True if os.environ.get('FLASK_ENV', 'produciton') == 'development' else False),
        host='0.0.0.0',
        port=int(os.environ.get('FLASK_SERVER_PORT', '8801')),
        threaded=True)
