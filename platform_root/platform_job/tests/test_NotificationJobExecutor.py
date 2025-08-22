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
import requests_mock

import ulid
import base64
import json
import datetime
from contextlib import closing
from importlib import import_module

from unittest import mock
from email.message import EmailMessage
from email.utils import formataddr

from common_library.common import const
from common_library.common import encrypt
from common_library.common.db import DBconnector

from jobs import jobs_common
import job_manager_const
import job_manager_config
from jobs.NotificationJobExecutor import NotificationJobExecutor

from tests.common import test_common


def test_execute_teams_wf_nomally():
    """teams workflow 送信正常パターン / teams workflow sending successful pattern
    """
    testdata = import_module("tests.db.exports.testdata")

    organization_id = list(testdata.ORGANIZATIONS.keys())[0]
    workspace_id = testdata.ORGANIZATIONS[organization_id]["workspace_id"][0]

    webhook_url_path = "/test_execute_teams_wf_nomally"
    message_title = "test_execute_teams_wf_nomally title"
    message_text = "test_execute_teams_wf_nomally text"

    queue = make_notification_teams_wf(
        organization_id,
        workspace_id,
        f"{test_common.TEST_HTTPCODE200_ORIGIN}/{webhook_url_path}",
        message_title,
        message_text)

    with test_common.requsts_mocker_default() as requsts_mocker:
        executor = NotificationJobExecutor(queue)
        result = executor.execute_base()

        # 成功を返すこと
        assert result
        # ステータスが成功に更新されていること
        assert get_notification_status(organization_id, workspace_id, queue['PROCESS_EXEC_ID']) == const.NOTIFICATION_STATUS_SUCCESSFUL
        # 指定したwebhookが1回呼ばれていること
        request_webhooks = [history for history in requsts_mocker.request_history if history.url == f"{test_common.TEST_HTTPCODE200_ORIGIN}/{webhook_url_path}"]
        assert len(request_webhooks) == 1
        # 送信webhookの内容が正しいこと
        assert request_webhooks[0].method == 'POST'
        assert json.loads(request_webhooks[0].text)["attachments"][0]["content"]["body"][0]["text"] == message_title
        assert json.loads(request_webhooks[0].text)["attachments"][0]["content"]["body"][1]["text"] == message_text


def test_execute_teams_wf_http_error():
    """teams workflow 送信httpエラーパターン / teams workflow send http error pattern
    """
    testdata = import_module("tests.db.exports.testdata")

    organization_id = list(testdata.ORGANIZATIONS.keys())[0]
    workspace_id = testdata.ORGANIZATIONS[organization_id]["workspace_id"][0]

    webhook_url_path = "/test_execute_teams_wf_http_error"
    message_title = "test_execute_teams_wf_http_error title"
    message_text = "test_execute_teams_wf_http_error text"

    queue = make_notification_teams_wf(
        organization_id,
        workspace_id,
        f"{test_common.TEST_HTTPCODE500_ORIGIN}/{webhook_url_path}",
        message_title,
        message_text)

    with test_common.requsts_mocker_default() as requsts_mocker:
        executor = NotificationJobExecutor(queue)
        result = executor.execute_base()

        # 失敗を返すこと
        assert not result
        # ステータスが失敗に更新されていること
        assert get_notification_status(organization_id, workspace_id, queue['PROCESS_EXEC_ID']) == const.NOTIFICATION_STATUS_FAILED
        # 指定したwebhookが1回呼ばれていること
        request_webhooks = [history for history in requsts_mocker.request_history if history.url == f"{test_common.TEST_HTTPCODE500_ORIGIN}/{webhook_url_path}"]
        assert len(request_webhooks) == 1
        # 送信webhookの内容が正しいこと
        assert request_webhooks[0].method == 'POST'
        assert json.loads(request_webhooks[0].text)["attachments"][0]["content"]["body"][0]["text"] == message_title
        assert json.loads(request_webhooks[0].text)["attachments"][0]["content"]["body"][1]["text"] == message_text


def test_execute_webhook_nomally():
    """webhook 送信正常パターン / webhook sending successful pattern
    """
    testdata = import_module("tests.db.exports.testdata")

    organization_id = list(testdata.ORGANIZATIONS.keys())[0]
    workspace_id = testdata.ORGANIZATIONS[organization_id]["workspace_id"][0]

    webhook_url_path = "/test_execute_webhook_nomally"
    webhook_header = '{"X-Api-Key": "test_execute_webhook_nomally"}'
    message_title = "test_execute_webhook_nomally title"
    message_text = "test_execute_webhook_nomally text"

    queue = make_notification_webhook(
        organization_id,
        workspace_id,
        f"{test_common.TEST_HTTPCODE200_ORIGIN}/{webhook_url_path}",
        webhook_header,
        message_title,
        message_text)

    with test_common.requsts_mocker_default() as requsts_mocker:
        executor = NotificationJobExecutor(queue)
        result = executor.execute_base()

        # 成功を返すこと
        assert result
        # ステータスが成功に更新されていること
        assert get_notification_status(organization_id, workspace_id, queue['PROCESS_EXEC_ID']) == const.NOTIFICATION_STATUS_SUCCESSFUL
        # 指定したwebhookが1回呼ばれていること
        request_webhooks = [history for history in requsts_mocker.request_history if history.url == f"{test_common.TEST_HTTPCODE200_ORIGIN}/{webhook_url_path}"]
        assert len(request_webhooks) == 1
        # 送信webhookの内容が正しいこと
        assert request_webhooks[0].method == 'POST'
        assert json.loads(request_webhooks[0].text)["text"] == message_title + "\n\n" + message_text
        assert request_webhooks[0].headers["X-Api-Key"] == "test_execute_webhook_nomally"


def test_execute_webhook_http_error():
    """webhook 送信httpエラーパターン / webhook send http error pattern
    """
    testdata = import_module("tests.db.exports.testdata")

    organization_id = list(testdata.ORGANIZATIONS.keys())[0]
    workspace_id = testdata.ORGANIZATIONS[organization_id]["workspace_id"][0]

    webhook_url_path = "/test_execute_webhook_http_error"
    webhook_header = None
    message_title = "test_execute_webhook_http_error title"
    message_text = "test_execute_webhook_http_error text"

    queue = make_notification_webhook(
        organization_id,
        workspace_id,
        f"{test_common.TEST_HTTPCODE500_ORIGIN}/{webhook_url_path}",
        webhook_header,
        message_title,
        message_text)

    with test_common.requsts_mocker_default() as requsts_mocker:
        executor = NotificationJobExecutor(queue)
        result = executor.execute_base()

        # 失敗を返すこと
        assert not result
        # ステータスが失敗に更新されていること
        assert get_notification_status(organization_id, workspace_id, queue['PROCESS_EXEC_ID']) == const.NOTIFICATION_STATUS_FAILED
        # 指定したwebhookが1回呼ばれていること
        request_webhooks = [history for history in requsts_mocker.request_history if history.url == f"{test_common.TEST_HTTPCODE500_ORIGIN}/{webhook_url_path}"]
        assert len(request_webhooks) == 1
        # 送信webhookの内容が正しいこと
        assert request_webhooks[0].method == 'POST'
        assert json.loads(request_webhooks[0].text)["text"] == message_title + "\n\n" + message_text


def test_execute_mail_smtp_normally():
    """email送信(smtp認証無し)正常パターン / email sending(no smtp authentication) successful pattern
    """
    testdata = import_module("tests.db.exports.testdata")

    organization_id = list(testdata.ORGANIZATIONS.keys())[0]
    workspace_id = testdata.ORGANIZATIONS[organization_id]["workspace_id"][0]

    message_title = "test_execute_mail_smtp_normal title"
    message_text = "test_execute_mail_smtp_normal text"
    mail_to = ["test_to1@test"]
    mail_cc = []
    mail_bcc = []

    mserver = make_mailserver_setting(organization_id, {
        "SMTP_HOST": "test_mailserver",
        "SMTP_PORT": 25,
        "SEND_FROM": "from@test",
    })

    queue = make_notification_mail(
        organization_id,
        workspace_id,
        mail_to,
        mail_cc,
        mail_bcc,
        message_title,
        message_text)

    with test_common.requsts_mocker_default(), \
            mock.patch("smtplib.SMTP", mocked_smtp), \
            mock.patch("smtplib.SMTP_SSL", mocked_smtps):

        mocked_smtp_base.init_instances()
        executor = NotificationJobExecutor(queue)
        result = executor.execute_base()

        # 成功を返すこと
        assert result
        # ステータスが成功に更新されていること
        assert get_notification_status(organization_id, workspace_id, queue['PROCESS_EXEC_ID']) == const.NOTIFICATION_STATUS_SUCCESSFUL

        # SMTPへのパラメータが正しいこと
        smtp_instances = mocked_smtp_base.get_instances()
        assert len(smtp_instances) == 1
        assert smtp_instances[0].kind == 'smtp'
        assert not smtp_instances[0].tls
        assert smtp_instances[0].host == mserver['SMTP_HOST']
        assert smtp_instances[0].port == mserver['SMTP_PORT']
        assert smtp_instances[0].timeout == job_manager_config.JOBS[const.PROCESS_KIND_NOTIFICATION]['extra_config']['smtp_timeout']
        assert smtp_instances[0].auth_user is None
        assert smtp_instances[0].auth_password is None
        assert smtp_instances[0].message['Subject'] == message_title
        assert message_text in smtp_instances[0].message.get_content()
        assert smtp_instances[0].message.get('From') == formataddr((mserver['SEND_NAME'], mserver['SEND_FROM']))
        assert smtp_instances[0].message.get('To', "").replace(" ", "") == ",".join(mail_to)
        assert smtp_instances[0].message.get('Cc', "").replace(" ", "") == ",".join(mail_cc)
        assert smtp_instances[0].message.get('Bcc', "").replace(" ", "") == ",".join(mail_bcc)
        assert smtp_instances[0].message.get('reply-to') is None
        assert smtp_instances[0].from_addr == mserver['SEND_FROM']
        assert sorted(smtp_instances[0].to_addrs) == sorted(mail_to + mail_cc + mail_bcc)
        assert smtp_instances[0].auth_user is None
        assert smtp_instances[0].auth_password is None


def test_execute_mail_smtp_error():
    """email送信エラーパターン / email sending error pattern
    """
    testdata = import_module("tests.db.exports.testdata")

    organization_id = list(testdata.ORGANIZATIONS.keys())[0]
    workspace_id = testdata.ORGANIZATIONS[organization_id]["workspace_id"][0]

    message_title = "test_execute_mail_smtp_error title"
    message_text = "test_execute_mail_smtp_error text"
    mail_to = ["test_to1@test", "test_to2@test"]
    mail_cc = ["test_cc1@test", "test_cc2@test"]
    mail_bcc = ["test_bcc1@test", "test_bcc2@test"]

    # mail server情報なし / No mail server information

    queue = make_notification_mail(
        organization_id,
        workspace_id,
        mail_to,
        mail_cc,
        mail_bcc,
        message_title,
        message_text)

    with test_common.requsts_mocker_default(), \
            mock.patch("smtplib.SMTP", mocked_smtp), \
            mock.patch("smtplib.SMTP_SSL", mocked_smtps):

        mocked_smtp_base.init_instances()
        executor = NotificationJobExecutor(queue)
        result = executor.execute_base()

        # 異常を返すこと
        assert not result
        # ステータスが失敗に更新されていること
        assert get_notification_status(organization_id, workspace_id, queue['PROCESS_EXEC_ID']) == const.NOTIFICATION_STATUS_FAILED


def test_execute_mail_smtp_tls_normally():
    """email送信(smtp starttls認証あり)正常パターン / email sending(smtp start tls authentication) successful pattern
    """
    testdata = import_module("tests.db.exports.testdata")

    organization_id = list(testdata.ORGANIZATIONS.keys())[0]
    workspace_id = testdata.ORGANIZATIONS[organization_id]["workspace_id"][0]

    message_title = "test_execute_mail_smtp_tls_normally title"
    message_text = "test_execute_mail_smtp_tls_normally text"
    mail_to = []
    mail_cc = ["test_cc1@test"]
    mail_bcc = []

    mserver = make_mailserver_setting(
        organization_id,
        {
            "SMTP_HOST": "test_mailserver",
            "SMTP_PORT": 587,
            "SEND_FROM": "from@test",
            "SEND_NAME": "from_name",
            "REPLY_TO": "replay@test",
            "ENVELOPE_FROM": "envelope_from@test",
            "START_TLS_ENABLE": 1,
            "AUTHENTICATION_ENABLE": 1,
            "AUTHENTICATION_USER": "auth_user",
            "AUTHENTICATION_PASSWORD": encrypt.encrypt_str("auth_password"),
        })

    queue = make_notification_mail(
        organization_id,
        workspace_id,
        mail_to,
        mail_cc,
        mail_bcc,
        message_title,
        message_text)

    with test_common.requsts_mocker_default(), \
            mock.patch("smtplib.SMTP", mocked_smtp), \
            mock.patch("smtplib.SMTP_SSL", mocked_smtps):

        mocked_smtp_base.init_instances()
        executor = NotificationJobExecutor(queue)
        result = executor.execute_base()

        # 成功を返すこと
        assert result
        # ステータスが成功に更新されていること
        assert get_notification_status(organization_id, workspace_id, queue['PROCESS_EXEC_ID']) == const.NOTIFICATION_STATUS_SUCCESSFUL

        # SMTPへのパラメータが正しいこと
        smtp_instances = mocked_smtp_base.get_instances()
        assert len(smtp_instances) == 1
        assert smtp_instances[0].kind == 'smtp'
        assert smtp_instances[0].tls
        assert smtp_instances[0].host == mserver['SMTP_HOST']
        assert smtp_instances[0].port == mserver['SMTP_PORT']
        assert smtp_instances[0].timeout == job_manager_config.JOBS[const.PROCESS_KIND_NOTIFICATION]['extra_config']['smtp_timeout']
        assert smtp_instances[0].auth_user == mserver['AUTHENTICATION_USER']
        assert smtp_instances[0].auth_password == encrypt.decrypt_str(mserver['AUTHENTICATION_PASSWORD'])
        assert smtp_instances[0].message['Subject'] == message_title
        assert message_text in smtp_instances[0].message.get_content()
        assert smtp_instances[0].message.get('From') == formataddr((mserver['SEND_NAME'], mserver['SEND_FROM']))
        assert smtp_instances[0].message.get('To', "").replace(" ", "") == ",".join(mail_to)
        assert smtp_instances[0].message.get('Cc', "").replace(" ", "") == ",".join(mail_cc)
        assert smtp_instances[0].message.get('Bcc', "").replace(" ", "") == ",".join(mail_bcc)
        assert smtp_instances[0].message.get('reply-to', "") == formataddr((mserver['REPLY_NAME'], mserver['REPLY_TO']))
        assert smtp_instances[0].from_addr == mserver['ENVELOPE_FROM']
        assert sorted(smtp_instances[0].to_addrs) == sorted(mail_to + mail_cc + mail_bcc)


def test_execute_mail_smtp_ssl_normally():
    """email送信(smtps認証あり)正常パターン / email sending(smtps authentication) successful pattern
    """
    testdata = import_module("tests.db.exports.testdata")

    organization_id = list(testdata.ORGANIZATIONS.keys())[0]
    workspace_id = testdata.ORGANIZATIONS[organization_id]["workspace_id"][0]

    message_title = "test_execute_mail_smtp_ssl_normally title"
    message_text = "test_execute_mail_smtp_ssl_normally text"
    mail_to = []
    mail_cc = []
    mail_bcc = ["test_bcc1@test"]

    mserver = make_mailserver_setting(
        organization_id,
        {
            "SMTP_HOST": "test_mailserver",
            "SMTP_PORT": 465,
            "SEND_FROM": "from@test",
            "SEND_NAME": "from_name",
            "REPLY_TO": "replay@test",
            "REPLY_NAME": "reply_name",
            "ENVELOPE_FROM": "envelope_from@test",
            "SSL_ENABLE": 1,
            "AUTHENTICATION_ENABLE": 1,
            "AUTHENTICATION_USER": "auth_user",
            "AUTHENTICATION_PASSWORD": encrypt.encrypt_str("auth_password"),
        })

    queue = make_notification_mail(
        organization_id,
        workspace_id,
        mail_to,
        mail_cc,
        mail_bcc,
        message_title,
        message_text)

    with test_common.requsts_mocker_default(), \
            mock.patch("smtplib.SMTP", mocked_smtp), \
            mock.patch("smtplib.SMTP_SSL", mocked_smtps):

        mocked_smtp_base.init_instances()
        executor = NotificationJobExecutor(queue)
        result = executor.execute_base()

        # 成功を返すこと
        assert result
        # ステータスが成功に更新されていること
        assert get_notification_status(organization_id, workspace_id, queue['PROCESS_EXEC_ID']) == const.NOTIFICATION_STATUS_SUCCESSFUL

        # SMTPへのパラメータが正しいこと
        smtp_instances = mocked_smtp_base.get_instances()
        assert len(smtp_instances) == 1
        assert smtp_instances[0].kind == 'smtps'
        assert not smtp_instances[0].tls
        assert smtp_instances[0].host == mserver['SMTP_HOST']
        assert smtp_instances[0].port == mserver['SMTP_PORT']
        assert smtp_instances[0].timeout == job_manager_config.JOBS[const.PROCESS_KIND_NOTIFICATION]['extra_config']['smtp_timeout']
        assert smtp_instances[0].auth_user == mserver['AUTHENTICATION_USER']
        assert smtp_instances[0].auth_password == encrypt.decrypt_str(mserver['AUTHENTICATION_PASSWORD'])
        assert smtp_instances[0].message['Subject'] == message_title
        assert message_text in smtp_instances[0].message.get_content()
        assert smtp_instances[0].message.get('From') == formataddr((mserver['SEND_NAME'], mserver['SEND_FROM']))
        assert smtp_instances[0].message.get('To', "").replace(" ", "") == ",".join(mail_to)
        assert smtp_instances[0].message.get('Cc', "").replace(" ", "") == ",".join(mail_cc)
        assert smtp_instances[0].message.get('Bcc', "").replace(" ", "") == ",".join(mail_bcc)
        assert smtp_instances[0].message.get('reply-to', "") == formataddr((mserver['REPLY_NAME'], mserver['REPLY_TO']))
        assert smtp_instances[0].from_addr == mserver['ENVELOPE_FROM']
        assert sorted(smtp_instances[0].to_addrs) == sorted(mail_to + mail_cc + mail_bcc)


def test_execute_servicenow_one_normallry():
    """servicenow連携(個別送信) 正常系
    """
    testdata = import_module("tests.db.exports.testdata")

    organization_id = list(testdata.ORGANIZATIONS.keys())[0]
    workspace_id = testdata.ORGANIZATIONS[organization_id]["workspace_id"][0]

    sn_api_url = "http://sn.dummy/api/api_url"
    sn_user = "sn_user01"
    sn_pw = "sn-password01"
    sn_auth_header = 'Basic ' + base64.b64encode(f'{sn_user}:{sn_pw}'.encode('utf-8')).decode('utf-8')

    sn_body = {"field1": "value1", "field2": "value2"}
    sn_resp = {"unit-test-response": "OK"}

    queue = make_notification_servicenow_one(organization_id, workspace_id, sn_api_url, sn_user, sn_pw, sn_body)

    with test_common.requsts_mocker_default() as requests_mocker:
        # ServiceNowへの要求をmockする
        requests_mocker.register_uri(
            requests_mock.POST,
            sn_api_url,
            status_code=200,
            json=sn_resp)

        executor = NotificationJobExecutor(queue)
        result = executor.execute_base()

        # 成功を返すこと
        assert result
        # ステータスが成功に更新されていること
        assert get_notification_status(organization_id, workspace_id, queue['PROCESS_EXEC_ID']) == const.NOTIFICATION_STATUS_SUCCESSFUL
        # HTTPCODEとRESPONSE BODYが更新されていること
        assert_notification_response(organization_id, workspace_id, queue['PROCESS_EXEC_ID'], 200, json.dumps(sn_resp))

        # sn_api_urlへの要求を取得する
        sn_requests_history = [his for his in requests_mocker.request_history if his.url == sn_api_url]

        # sn_api_urlへの要求は1回であること
        assert len(sn_requests_history) == 1
        # sn_api_urlへ要求したbodyが要求したものと等しいこと
        assert json.dumps(json.loads(sn_requests_history[0].body)) == json.dumps(sn_body)
        # sn_api_urlへ要求した際にAuthorizationヘッダが存在こと
        assert 'Authorization' in sn_requests_history[0].headers
        # sn_api_urlへ要求した際にAuthorizationヘッダの内容が設定した内容であること
        assert sn_requests_history[0].headers['Authorization'] == sn_auth_header


def test_execute_servicenow_one_error():
    """servicenow連携(個別送信) 異常系
    """
    testdata = import_module("tests.db.exports.testdata")

    organization_id = list(testdata.ORGANIZATIONS.keys())[0]
    workspace_id = testdata.ORGANIZATIONS[organization_id]["workspace_id"][0]

    sn_api_url = "http://sn.dummy/api/api_url"
    sn_user = "sn_user01"
    sn_pw = "sn-password01"
    sn_auth_header = 'Basic ' + base64.b64encode(f'{sn_user}:{sn_pw}'.encode('utf-8')).decode('utf-8')

    sn_body = {"field1": "value1", "field2": "value2"}
    sn_resp = {"unit-test-response": "OK"}

    queue = make_notification_servicenow_one(organization_id, workspace_id, sn_api_url, sn_user, sn_pw, sn_body)

    with test_common.requsts_mocker_default() as requests_mocker:
        # ServiceNowへの要求をmockする
        requests_mocker.register_uri(
            requests_mock.POST,
            sn_api_url,
            status_code=500,
            json=sn_resp)

        executor = NotificationJobExecutor(queue)
        result = executor.execute_base()

        # 失敗を返すこと
        assert not result
        # ステータスが失敗に更新されていること
        assert get_notification_status(organization_id, workspace_id, queue['PROCESS_EXEC_ID']) == const.NOTIFICATION_STATUS_FAILED
        # HTTPCODEとRESPONSE BODYが更新されていること
        assert_notification_response(organization_id, workspace_id, queue['PROCESS_EXEC_ID'], 500, json.dumps(sn_resp))

        # sn_api_urlへの要求を取得する
        sn_requests_history = [his for his in requests_mocker.request_history if his.url == sn_api_url]

        # sn_api_urlへの要求は1回であること
        assert len(sn_requests_history) == 1
        # sn_api_urlへ要求したbodyが要求したものと等しいこと
        assert json.dumps(json.loads(sn_requests_history[0].body)) == json.dumps(sn_body)
        # sn_api_urlへ要求した際にAuthorizationヘッダが存在こと
        assert 'Authorization' in sn_requests_history[0].headers
        # sn_api_urlへ要求した際にAuthorizationヘッダの内容が設定した内容であること
        assert sn_requests_history[0].headers['Authorization'] == sn_auth_header


def test_execute_servicenow_batch_normallry():
    """servicenow連携(一括送信) 正常系
    """
    testdata = import_module("tests.db.exports.testdata")

    organization_id = list(testdata.ORGANIZATIONS.keys())[0]
    workspace_id = testdata.ORGANIZATIONS[organization_id]["workspace_id"][0]

    sn_batch_url = "http://sn.dummy/api/batch_url"
    sn_api_url = "http://sn.dummy/api/api_url"
    sn_api_path = "/api/api_url"
    sn_user = "sn_user01"
    sn_pw = "sn-password01"
    sn_auth_header = 'Basic ' + base64.b64encode(f'{sn_user}:{sn_pw}'.encode('utf-8')).decode('utf-8')

    sn_bodys = [
        {"field1": "value1-1", "field2": "value1-2"},
        {"field1": "value2-1", "field2": "value2-2"},
        {"field1": "value3-1", "field2": "value3-2"},
    ]

    sn_resps = [
        {"status": 200, "body": {"unit-test-response": "1-OK"}},
        {"status": 201, "body": {"unit-test-response": "2-OK"}},
        {"status": 202, "body": {"unit-test-response": "3-OK"}},
    ]

    queues = make_notification_servicenow_batch(organization_id, workspace_id, sn_batch_url, sn_api_url, sn_user, sn_pw, sn_bodys)

    # ServiceNowのbatchのレスポンス情報の生成
    sn_resp_body = {
        "serviced_requests": [
            {
                "id": queues[index]['PROCESS_EXEC_ID'],
                "status_code": sn_resp["status"],
                "body": base64.b64encode(json.dumps(sn_resp["body"]).encode()).decode('ascii')
            }
            for index, sn_resp in enumerate(sn_resps)
        ]
    }

    with test_common.requsts_mocker_default() as requests_mocker:
        # ServiceNowへの要求をmockする
        requests_mocker.register_uri(
            requests_mock.POST,
            sn_batch_url,
            status_code=200,
            json=sn_resp_body)

        executor = NotificationJobExecutor(queues[0], queues)
        result = executor.execute_base()

        # 全て成功なのでTrueを返すこと
        assert result

        for index, queue in enumerate(queues):
            # ステータスが成功に更新されていること
            assert get_notification_status(organization_id, workspace_id, queue['PROCESS_EXEC_ID']) == const.NOTIFICATION_STATUS_SUCCESSFUL

            # HTTPCODEとRESPONSE BODYが更新されていること
            assert_notification_response(organization_id, workspace_id, queue['PROCESS_EXEC_ID'], sn_resps[index]["status"], json.dumps(sn_resps[index]["body"]))

        # sn_batch_urlへの要求を取得する
        sn_requests_history = [his for his in requests_mocker.request_history if his.url == sn_batch_url]

        # sn_batch_urlへの要求は1回であること
        assert len(sn_requests_history) == 1
        # sn_batch_urlへ要求したbodyが要求したものと等しいこと
        sn_batch_body = json.loads(sn_requests_history[0].body).get("rest_requests", [])
        assert len(sn_batch_body) == len(queues)
        for i, queue in enumerate(queues):
            assert sn_batch_body[i]['id'] == queue['PROCESS_EXEC_ID']
            assert sn_batch_body[i]['method'] == 'POST'
            assert sn_batch_body[i]['url'] == sn_api_path
            assert sn_batch_body[i]['body'] == base64.b64encode(json.dumps(sn_bodys[i]).encode()).decode('ascii')

        # sn_api_urlへ要求した際にAuthorizationヘッダが存在こと
        assert 'Authorization' in sn_requests_history[0].headers
        # sn_api_urlへ要求した際にAuthorizationヘッダの内容が設定した内容であること
        assert sn_requests_history[0].headers['Authorization'] == sn_auth_header


def test_execute_servicenow_batch_partially_failed():
    """servicenow連携(一括送信) 一部失敗
    """
    testdata = import_module("tests.db.exports.testdata")

    organization_id = list(testdata.ORGANIZATIONS.keys())[0]
    workspace_id = testdata.ORGANIZATIONS[organization_id]["workspace_id"][0]

    sn_batch_url = "http://sn.dummy/api/batch_url"
    sn_api_url = "http://sn.dummy/api/api_url"
    sn_api_path = "/api/api_url"
    sn_user = "sn_user01"
    sn_pw = "sn-password01"
    sn_auth_header = 'Basic ' + base64.b64encode(f'{sn_user}:{sn_pw}'.encode('utf-8')).decode('utf-8')

    sn_bodys = [
        {"field1": "value1-1", "field2": "value1-2"},
        {"field1": "value2-1", "field2": "value2-2"},
        {"field1": "value3-1", "field2": "value3-2"},
        {"field1": "value4-1", "field2": "value4-2"},
    ]

    sn_resps = [
        {"status": 200, "body": {"unit-test-response": "1-OK"}},
        {"status": 400, "body": {"unit-test-response": "2-OK"}},
        {"status": 401, "body": {"unit-test-response": "3-OK"}},
        {"status": 200, "body": {"unit-test-response": "4-OK"}},
    ]

    queues = make_notification_servicenow_batch(organization_id, workspace_id, sn_batch_url, sn_api_url, sn_user, sn_pw, sn_bodys)

    # ServiceNowのbatchのレスポンス情報の生成
    sn_resp_body = {
        "serviced_requests": [
            {
                "id": queues[index]['PROCESS_EXEC_ID'],
                "status_code": sn_resp["status"],
                "body": base64.b64encode(json.dumps(sn_resp["body"]).encode()).decode('ascii')
            }
            for index, sn_resp in enumerate(sn_resps)
        ]
    }

    with test_common.requsts_mocker_default() as requests_mocker:
        # ServiceNowへの要求をmockする
        requests_mocker.register_uri(
            requests_mock.POST,
            sn_batch_url,
            status_code=200,
            json=sn_resp_body)

        executor = NotificationJobExecutor(queues[0], queues)
        result = executor.execute_base()

        # 一部失敗なのでFalseを返すこと
        assert not result

        for index, queue in enumerate(queues):
            # ステータスがstatus_code毎に更新されていること
            assert get_notification_status(organization_id, workspace_id, queue['PROCESS_EXEC_ID']) \
                == const.NOTIFICATION_STATUS_SUCCESSFUL if sn_resps[index]["status"] == 200 else const.NOTIFICATION_STATUS_FAILED

            # HTTPCODEとRESPONSE BODYが更新されていること
            assert_notification_response(organization_id, workspace_id, queue['PROCESS_EXEC_ID'], sn_resps[index]["status"], json.dumps(sn_resps[index]["body"]))

        # sn_batch_urlへの要求を取得する
        sn_requests_history = [his for his in requests_mocker.request_history if his.url == sn_batch_url]

        # sn_batch_urlへの要求は1回であること
        assert len(sn_requests_history) == 1
        # sn_batch_urlへ要求したbodyが要求したものと等しいこと
        sn_batch_body = json.loads(sn_requests_history[0].body).get("rest_requests", [])
        assert len(sn_batch_body) == len(queues)
        for i, queue in enumerate(queues):
            assert sn_batch_body[i]['id'] == queue['PROCESS_EXEC_ID']
            assert sn_batch_body[i]['method'] == 'POST'
            assert sn_batch_body[i]['url'] == sn_api_path
            assert sn_batch_body[i]['body'] == base64.b64encode(json.dumps(sn_bodys[i]).encode()).decode('ascii')

        # sn_api_urlへ要求した際にAuthorizationヘッダが存在こと
        assert 'Authorization' in sn_requests_history[0].headers
        # sn_api_urlへ要求した際にAuthorizationヘッダの内容が設定した内容であること
        assert sn_requests_history[0].headers['Authorization'] == sn_auth_header


def test_execute_servicenow_batch_error():
    """servicenow連携(一括送信) 異常系
    """
    testdata = import_module("tests.db.exports.testdata")

    organization_id = list(testdata.ORGANIZATIONS.keys())[0]
    workspace_id = testdata.ORGANIZATIONS[organization_id]["workspace_id"][0]

    sn_batch_url = "http://sn.dummy/api/batch_url"
    sn_api_url = "http://sn.dummy/api/api_url"
    sn_user = "sn_user01"
    sn_pw = "sn-password01"

    sn_bodys = [
        {"field1": "value1-1", "field2": "value1-2"},
        {"field1": "value2-1", "field2": "value2-2"},
        {"field1": "value3-1", "field2": "value3-2"},
    ]

    queues = make_notification_servicenow_batch(organization_id, workspace_id, sn_batch_url, sn_api_url, sn_user, sn_pw, sn_bodys)

    # ServiceNowのbatchのレスポンス情報の生成
    sn_resp_body = {"messege": "error!!"}

    with test_common.requsts_mocker_default() as requests_mocker:
        # ServiceNowへの要求をmockする
        requests_mocker.register_uri(
            requests_mock.POST,
            sn_batch_url,
            status_code=500,
            json=sn_resp_body)

        executor = NotificationJobExecutor(queues[0], queues)
        result = executor.execute_base()

        # 失敗なのでFalseを返すこと
        assert not result

        for index, queue in enumerate(queues):
            # ステータスが成功に更新されていること
            assert get_notification_status(organization_id, workspace_id, queue['PROCESS_EXEC_ID']) == const.NOTIFICATION_STATUS_FAILED

            # HTTPCODEとRESPONSE BODYがAPIで返された応答であること
            assert_notification_response(organization_id, workspace_id, queue['PROCESS_EXEC_ID'], 500, json.dumps(sn_resp_body))


def test_execute_no_notification():
    """通知情報なしパターン / No notification information pattern
    """
    testdata = import_module("tests.db.exports.testdata")

    organization_id = list(testdata.ORGANIZATIONS.keys())[0]
    workspace_id = testdata.ORGANIZATIONS[organization_id]["workspace_id"][0]

    queue = {
        "PROCESS_ID": ulid.new().str,
        "PROCESS_KIND": const.PROCESS_KIND_NOTIFICATION,
        "PROCESS_EXEC_ID": ulid.new().str,
        "ORGANIZATION_ID": organization_id,
        "WORKSPACE_ID": workspace_id,
        "LAST_UPDATE_USER": job_manager_const.SYSTEM_USER_ID,
        "LAST_UPDATE_TIMESTAMP": datetime.datetime.now(),
    }

    with test_common.requsts_mocker_default():
        executor = NotificationJobExecutor(queue)
        result = executor.execute_base()

        # 失敗を返すこと
        assert not result


def test_cancel_normally():
    """cancel実行パターン / cancel execution pattern
    """
    testdata = import_module("tests.db.exports.testdata")

    organization_id = list(testdata.ORGANIZATIONS.keys())[0]
    workspace_id = testdata.ORGANIZATIONS[organization_id]["workspace_id"][0]

    webhook_url_path = "/test_cancel_normal"
    message_title = "test_cancel_normal title"
    message_text = "test_cancel_normal text"

    queue = make_notification_teams_wf(
        organization_id,
        workspace_id,
        f"{test_common.TEST_HTTPCODE500_ORIGIN}/{webhook_url_path}",
        message_title,
        message_text)

    executor = NotificationJobExecutor(queue)
    result = executor.cancel_base()

    # 成功を返すこと
    assert result
    # ステータスが失敗に更新されていること
    assert get_notification_status(organization_id, workspace_id, queue['PROCESS_EXEC_ID']) == const.NOTIFICATION_STATUS_FAILED


def test_force_update_status_normally():
    """ 強制ステータス更新正常パターン / Forced status update normal pattern
    """
    testdata = import_module("tests.db.exports.testdata")

    datas = [
        {
            "organization_id": list(testdata.ORGANIZATIONS.keys())[0],
            "workspace_id": testdata.ORGANIZATIONS[list(testdata.ORGANIZATIONS.keys())[0]]["workspace_id"][0],
            "queue_exists": False,
            "too_old_date": True,
            "expired_date": False,
            "queue": None,
        },
        {
            "organization_id": list(testdata.ORGANIZATIONS.keys())[0],
            "workspace_id": testdata.ORGANIZATIONS[list(testdata.ORGANIZATIONS.keys())[0]]["workspace_id"][1],
            "queue_exists": False,
            "too_old_date": True,
            "expired_date": False,
            "queue": None,
        },
        {
            "organization_id": list(testdata.ORGANIZATIONS.keys())[1],
            "workspace_id": testdata.ORGANIZATIONS[list(testdata.ORGANIZATIONS.keys())[1]]["workspace_id"][0],
            "queue_exists": False,
            "too_old_date": True,
            "expired_date": False,
            "queue": None,
        },
        {
            "organization_id": list(testdata.ORGANIZATIONS.keys())[1],
            "workspace_id": testdata.ORGANIZATIONS[list(testdata.ORGANIZATIONS.keys())[1]]["workspace_id"][0],
            "queue_exists": True,
            "too_old_date": True,
            "expired_date": False,
            "queue": None,
        },
        {
            "organization_id": list(testdata.ORGANIZATIONS.keys())[2],
            "workspace_id": testdata.ORGANIZATIONS[list(testdata.ORGANIZATIONS.keys())[2]]["workspace_id"][0],
            "queue_exists": False,
            "too_old_date": True,
            "expired_date": False,
            "queue": None,
        },
        {
            "organization_id": list(testdata.ORGANIZATIONS.keys())[2],
            "workspace_id": testdata.ORGANIZATIONS[list(testdata.ORGANIZATIONS.keys())[2]]["workspace_id"][0],
            "queue_exists": False,
            "too_old_date": False,
            "expired_date": False,
            "queue": None,
        },
        {
            "organization_id": list(testdata.ORGANIZATIONS.keys())[2],
            "workspace_id": testdata.ORGANIZATIONS[list(testdata.ORGANIZATIONS.keys())[2]]["workspace_id"][0],
            "queue_exists": True,
            "too_old_date": True,
            "expired_date": True,
            "queue": None,
        },
    ]

    for data in datas:
        queue = make_notification_teams_wf(data['organization_id'], data['workspace_id'], test_common.TEST_HTTPCODE200_ORIGIN, 'title', 'message')
        data['queue'] = queue
        if data["queue_exists"]:
            # queueにデータをinsert
            test_common.insert_queue([queue])

        if data["expired_date"]:
            # データを古い時間に更新
            with closing(DBconnector().connect_workspacedb(data['organization_id'], data['workspace_id'])) as conn, \
                    conn.cursor() as cursor:

                cursor.execute(
                    """
                    UPDATE T_NOTIFICATION_MESSAGE
                        SET LAST_UPDATE_TIMESTAMP = DATE_SUB(LAST_UPDATE_TIMESTAMP, INTERVAL %(MINUTES)s MINUTE)
                        ,   CREATE_TIMESTAMP = DATE_SUB(CREATE_TIMESTAMP, INTERVAL %(MINUTES)s MINUTE)
                        WHERE NOTIFICATION_ID = %(NOTIFICATION_ID)s
                    """,
                    {
                        "NOTIFICATION_ID": queue['PROCESS_EXEC_ID'],
                        "MINUTES": job_manager_config.JOBS[const.PROCESS_KIND_NOTIFICATION]['extra_config']['aborted_expired_duration_minutes'] + 1
                    })
                conn.commit()

        elif data["too_old_date"]:
            # データを古い時間に更新
            with closing(DBconnector().connect_workspacedb(data['organization_id'], data['workspace_id'])) as conn, \
                    conn.cursor() as cursor:

                cursor.execute(
                    """
                    UPDATE T_NOTIFICATION_MESSAGE
                        SET LAST_UPDATE_TIMESTAMP = DATE_SUB(LAST_UPDATE_TIMESTAMP, INTERVAL %(SECONDS)s SECOND)
                        ,   CREATE_TIMESTAMP = DATE_SUB(CREATE_TIMESTAMP, INTERVAL %(SECONDS)s SECOND)
                        WHERE NOTIFICATION_ID = %(NOTIFICATION_ID)s
                    """,
                    {
                        "NOTIFICATION_ID": queue['PROCESS_EXEC_ID'],
                        "SECONDS": job_manager_config.JOBS[job_manager_const.PROCESS_KIND_FORCE_UPDATE_STATUS]['extra_config']['prograss_seconds'] + 1
                    })
                conn.commit()

    # 強制ステータス更新を実行
    NotificationJobExecutor.force_update_status()
    # データの更新状況を確認
    for i, data in enumerate(datas):
        status = get_notification_status(data['queue']['ORGANIZATION_ID'], data['queue']['WORKSPACE_ID'], data['queue']['PROCESS_EXEC_ID'])
        if data["expired_date"]:
            assert status == const.NOTIFICATION_STATUS_ABORTED_EXPIRED, f"assert status data[{i}]"
            with closing(DBconnector().connect_platformdb()) as conn_pf:
                assert not jobs_common.exists_queue(conn_pf, data['queue']['PROCESS_EXEC_ID'])
        elif data['queue_exists']:
            # queueに情報が残っている場合は、日時とは関係なく更新しない
            assert status == const.NOTIFICATION_STATUS_UNSENT, f"assert status data[{i}]"
        elif not data['too_old_date']:
            # 日時が古くない場合は、更新しない
            assert status == const.NOTIFICATION_STATUS_UNSENT, f"assert status data[{i}]"
        else:
            # queueにデータがなく、日付が古い場合、エラーに更新していること
            assert status == const.NOTIFICATION_STATUS_FAILED, f"assert status data[{i}]"


def make_notification_teams_wf(organization_id: str, workspace_id: str, webhook_uri: str, title: str, message: str):
    process_id = ulid.new().str
    notification_id = ulid.new().str

    data = {
        "NOTIFICATION_ID": notification_id,
        "DESTINATION_KIND": const.DESTINATION_KIND_TEAMS_WF,
        "DESTINATION_INFORMATIONS": encrypt.encrypt_str(json.dumps(
            [{
                "url": webhook_uri,
            }])),
        "MESSAGE_INFORMATIONS": json.dumps(
            {
                "title": title,
                "message": message
            }),
        "NOTIFICATION_STATUS": const.NOTIFICATION_STATUS_UNSENT,
        "CREATE_USER": job_manager_const.SYSTEM_USER_ID,
        "LAST_UPDATE_USER": job_manager_const.SYSTEM_USER_ID,
    }

    with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn, \
            conn.cursor() as cursor:

        conn.begin()
        cursor.execute("""
                INSERT INTO T_NOTIFICATION_MESSAGE
                    (
                        NOTIFICATION_ID,
                        DESTINATION_KIND,
                        DESTINATION_INFORMATIONS,
                        MESSAGE_INFORMATIONS,
                        NOTIFICATION_STATUS,
                        CREATE_USER,
                        LAST_UPDATE_USER
                    ) VALUES (
                        %(NOTIFICATION_ID)s,
                        %(DESTINATION_KIND)s,
                        %(DESTINATION_INFORMATIONS)s,
                        %(MESSAGE_INFORMATIONS)s,
                        %(NOTIFICATION_STATUS)s,
                        %(CREATE_USER)s,
                        %(LAST_UPDATE_USER)s
                    )
            """, data)
        conn.commit()

    queue = {
        "PROCESS_ID": process_id,
        "PROCESS_KIND": const.PROCESS_KIND_NOTIFICATION,
        "PROCESS_EXEC_ID": notification_id,
        "ORGANIZATION_ID": organization_id,
        "WORKSPACE_ID": workspace_id,
        "LAST_UPDATE_USER": job_manager_const.SYSTEM_USER_ID,
        "LAST_UPDATE_TIMESTAMP": str(datetime.datetime.now()),
    }
    # test_common.insert_queue([queue])
    return queue


def make_notification_webhook(organization_id: str, workspace_id: str, webhook_uri: str, webhook_header: str, title: str, message: str):
    process_id = ulid.new().str
    notification_id = ulid.new().str

    data = {
        "NOTIFICATION_ID": notification_id,
        "DESTINATION_KIND": const.DESTINATION_KIND_WEBHOOK,
        "DESTINATION_INFORMATIONS": encrypt.encrypt_str(json.dumps(
            [{
                "url": webhook_uri,
                "header": webhook_header,
            }])),
        "MESSAGE_INFORMATIONS": json.dumps(
            {
                "title": title,
                "message": message
            }),
        "NOTIFICATION_STATUS": const.NOTIFICATION_STATUS_UNSENT,
        "CREATE_USER": job_manager_const.SYSTEM_USER_ID,
        "LAST_UPDATE_USER": job_manager_const.SYSTEM_USER_ID,
    }

    with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn, \
            conn.cursor() as cursor:

        conn.begin()
        cursor.execute("""
                INSERT INTO T_NOTIFICATION_MESSAGE
                    (
                        NOTIFICATION_ID,
                        DESTINATION_KIND,
                        DESTINATION_INFORMATIONS,
                        MESSAGE_INFORMATIONS,
                        NOTIFICATION_STATUS,
                        CREATE_USER,
                        LAST_UPDATE_USER
                    ) VALUES (
                        %(NOTIFICATION_ID)s,
                        %(DESTINATION_KIND)s,
                        %(DESTINATION_INFORMATIONS)s,
                        %(MESSAGE_INFORMATIONS)s,
                        %(NOTIFICATION_STATUS)s,
                        %(CREATE_USER)s,
                        %(LAST_UPDATE_USER)s
                    )
            """, data)
        conn.commit()

    queue = {
        "PROCESS_ID": process_id,
        "PROCESS_KIND": const.PROCESS_KIND_NOTIFICATION,
        "PROCESS_EXEC_ID": notification_id,
        "ORGANIZATION_ID": organization_id,
        "WORKSPACE_ID": workspace_id,
        "LAST_UPDATE_USER": job_manager_const.SYSTEM_USER_ID,
        "LAST_UPDATE_TIMESTAMP": str(datetime.datetime.now()),
    }
    # test_common.insert_queue([queue])
    return queue


def make_mailserver_setting(organization_id: str, smtp_server: dict):
    smtp_server_default = {
        "SMTP_ID": const.DEFAULT_SMTP_ID,
        "SMTP_HOST": None,
        "SMTP_PORT": None,
        "SEND_FROM": None,
        "SEND_NAME": None,
        "REPLY_TO": None,
        "REPLY_NAME": None,
        "ENVELOPE_FROM": None,
        "SSL_ENABLE": 0,
        "START_TLS_ENABLE": 0,
        "AUTHENTICATION_ENABLE": 0,
        "AUTHENTICATION_USER": None,
        "AUTHENTICATION_PASSWORD": None,
        "CREATE_USER": job_manager_const.SYSTEM_USER_ID,
    }
    ret = dict(smtp_server_default, **smtp_server)
    with closing(DBconnector().connect_orgdb(organization_id)) as conn, \
            conn.cursor() as cursor:
        conn.begin()
        cursor.execute("""
                INSERT INTO M_SMTP_SERVER
                    (
                        SMTP_ID,
                        SMTP_HOST,
                        SMTP_PORT,
                        SEND_FROM,
                        SEND_NAME,
                        REPLY_TO,
                        REPLY_NAME,
                        ENVELOPE_FROM,
                        SSL_ENABLE,
                        START_TLS_ENABLE,
                        AUTHENTICATION_ENABLE,
                        AUTHENTICATION_USER,
                        AUTHENTICATION_PASSWORD,
                        CREATE_USER
                    ) VALUES (
                        %(SMTP_ID)s,
                        %(SMTP_HOST)s,
                        %(SMTP_PORT)s,
                        %(SEND_FROM)s,
                        %(SEND_NAME)s,
                        %(REPLY_TO)s,
                        %(REPLY_NAME)s,
                        %(ENVELOPE_FROM)s,
                        %(SSL_ENABLE)s,
                        %(START_TLS_ENABLE)s,
                        %(AUTHENTICATION_ENABLE)s,
                        %(AUTHENTICATION_USER)s,
                        %(AUTHENTICATION_PASSWORD)s,
                        %(CREATE_USER)s
                    )
            """, ret)
        conn.commit()

    return ret


def make_notification_mail(organization_id: str, workspace_id: str, mails_to: list, mails_cc: list, mails_bcc: list, title: str, message: str):
    process_id = ulid.new().str
    notification_id = ulid.new().str

    data = {
        "NOTIFICATION_ID": notification_id,
        "DESTINATION_KIND": const.DESTINATION_KIND_MAIL,
        "DESTINATION_INFORMATIONS": encrypt.encrypt_str(json.dumps(
            [{"address_header": const.MAIL_HEADER_TO, "email": mail} for mail in mails_to] +
            [{"address_header": const.MAIL_HEADER_CC, "email": mail} for mail in mails_cc] +
            [{"address_header": const.MAIL_HEADER_BCC, "email": mail} for mail in mails_bcc])),
        "MESSAGE_INFORMATIONS": json.dumps(
            {
                "title": title,
                "message": message
            }),
        "NOTIFICATION_STATUS": const.NOTIFICATION_STATUS_UNSENT,
        "CREATE_USER": job_manager_const.SYSTEM_USER_ID,
        "LAST_UPDATE_USER": job_manager_const.SYSTEM_USER_ID,
    }

    with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn, \
            conn.cursor() as cursor:
        conn.begin()
        cursor.execute("""
                INSERT INTO T_NOTIFICATION_MESSAGE
                    (
                        NOTIFICATION_ID,
                        DESTINATION_KIND,
                        DESTINATION_INFORMATIONS,
                        MESSAGE_INFORMATIONS,
                        NOTIFICATION_STATUS,
                        CREATE_USER,
                        LAST_UPDATE_USER
                    ) VALUES (
                        %(NOTIFICATION_ID)s,
                        %(DESTINATION_KIND)s,
                        %(DESTINATION_INFORMATIONS)s,
                        %(MESSAGE_INFORMATIONS)s,
                        %(NOTIFICATION_STATUS)s,
                        %(CREATE_USER)s,
                        %(LAST_UPDATE_USER)s
                    )
            """, data)
        conn.commit()

    queue = {
        "PROCESS_ID": process_id,
        "PROCESS_KIND": const.PROCESS_KIND_NOTIFICATION,
        "PROCESS_EXEC_ID": notification_id,
        "ORGANIZATION_ID": organization_id,
        "WORKSPACE_ID": workspace_id,
        "LAST_UPDATE_USER": job_manager_const.SYSTEM_USER_ID,
        "LAST_UPDATE_TIMESTAMP": str(datetime.datetime.now()),
    }
    # test_common.insert_queue([queue])
    return queue


def make_notification_servicenow_one(organization_id: str, workspace_id: str, sn_api_uri: str, sn_user: str, sn_pw: str, body: dict):
    process_id = ulid.new().str
    notification_id = ulid.new().str

    data = {
        "NOTIFICATION_ID": notification_id,
        "DESTINATION_KIND": const.DESTINATION_KIND_SERVICENOW,
        "DESTINATION_INFORMATIONS": encrypt.encrypt_str(json.dumps(
            [{
                "servicenow_user": sn_user,
                "servicenow_password": sn_pw,
                "table_api_url": sn_api_uri
            }])),
        "MESSAGE_INFORMATIONS": json.dumps(body),
        "NOTIFICATION_STATUS": const.NOTIFICATION_STATUS_UNSENT,
        "CREATE_USER": job_manager_const.SYSTEM_USER_ID,
        "LAST_UPDATE_USER": job_manager_const.SYSTEM_USER_ID,
    }

    with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn, \
            conn.cursor() as cursor:

        conn.begin()
        cursor.execute("""
                INSERT INTO T_NOTIFICATION_MESSAGE
                    (
                        NOTIFICATION_ID,
                        DESTINATION_KIND,
                        DESTINATION_INFORMATIONS,
                        MESSAGE_INFORMATIONS,
                        NOTIFICATION_STATUS,
                        CREATE_USER,
                        LAST_UPDATE_USER
                    ) VALUES (
                        %(NOTIFICATION_ID)s,
                        %(DESTINATION_KIND)s,
                        %(DESTINATION_INFORMATIONS)s,
                        %(MESSAGE_INFORMATIONS)s,
                        %(NOTIFICATION_STATUS)s,
                        %(CREATE_USER)s,
                        %(LAST_UPDATE_USER)s
                    )
            """, data)
        conn.commit()

    queue = {
        "PROCESS_ID": process_id,
        "PROCESS_KIND": const.PROCESS_KIND_NOTIFICATION,
        "PROCESS_EXEC_ID": notification_id,
        "ORGANIZATION_ID": organization_id,
        "WORKSPACE_ID": workspace_id,
        "LAST_UPDATE_USER": job_manager_const.SYSTEM_USER_ID,
        "LAST_UPDATE_TIMESTAMP": str(datetime.datetime.now()),
    }
    # test_common.insert_queue([queue])
    return queue


def make_notification_servicenow_batch(organization_id, workspace_id, sn_batch_url, sn_api_url, sn_user, sn_pw, sn_bodys):
    queues = []
    
    with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn, \
            conn.cursor() as cursor:

        conn.begin()

        for sn_body in sn_bodys:
            notification_id = ulid.new().str
            process_id = ulid.new().str

            data = {
                "NOTIFICATION_ID": notification_id,
                "DESTINATION_KIND": const.DESTINATION_KIND_SERVICENOW,
                "DESTINATION_INFORMATIONS": encrypt.encrypt_str(json.dumps(
                    [{
                        "servicenow_user": sn_user,
                        "servicenow_password": sn_pw,
                        "batch_api_url": sn_batch_url,
                        "table_api_url": sn_api_url
                    }])),
                "MESSAGE_INFORMATIONS": json.dumps(sn_body),
                "NOTIFICATION_STATUS": const.NOTIFICATION_STATUS_UNSENT,
                "CREATE_USER": job_manager_const.SYSTEM_USER_ID,
                "LAST_UPDATE_USER": job_manager_const.SYSTEM_USER_ID,
            }
            
            cursor.execute("""
                    INSERT INTO T_NOTIFICATION_MESSAGE
                        (
                            NOTIFICATION_ID,
                            DESTINATION_KIND,
                            DESTINATION_INFORMATIONS,
                            MESSAGE_INFORMATIONS,
                            NOTIFICATION_STATUS,
                            CREATE_USER,
                            LAST_UPDATE_USER
                        ) VALUES (
                            %(NOTIFICATION_ID)s,
                            %(DESTINATION_KIND)s,
                            %(DESTINATION_INFORMATIONS)s,
                            %(MESSAGE_INFORMATIONS)s,
                            %(NOTIFICATION_STATUS)s,
                            %(CREATE_USER)s,
                            %(LAST_UPDATE_USER)s
                        )
                """, data)
            
            queues.append({
                "PROCESS_ID": process_id,
                "PROCESS_KIND": const.PROCESS_KIND_NOTIFICATION,
                "PROCESS_EXEC_ID": notification_id,
                "ORGANIZATION_ID": organization_id,
                "WORKSPACE_ID": workspace_id,
                "LAST_UPDATE_USER": job_manager_const.SYSTEM_USER_ID,
                "LAST_UPDATE_TIMESTAMP": str(datetime.datetime.now()),
            })

        conn.commit()

    # test_common.insert_queue([queue])
    return queues


def get_notification_status(organization_id, workspace_id, notification_id):
    with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn, \
            conn.cursor() as cursor:
        cursor.execute("""
                SELECT NOTIFICATION_STATUS  FROM    T_NOTIFICATION_MESSAGE
                    WHERE   NOTIFICATION_ID     =   %(NOTIFICATION_ID)s
            """, {"NOTIFICATION_ID": notification_id})
        row = cursor.fetchone()
        if row is not None:
            return row["NOTIFICATION_STATUS"]
        else:
            return None


def assert_notification_response(organization_id, workspace_id, notification_id, response_code, response_body):
    with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn, \
            conn.cursor() as cursor:
        cursor.execute("""
                SELECT * FROM    T_NOTIFICATION_MESSAGE
                    WHERE   NOTIFICATION_ID     =   %(NOTIFICATION_ID)s
            """, {"NOTIFICATION_ID": notification_id})

        row = cursor.fetchone()

        assert row is not None
        assert row['HTTP_RESPONSE_CODE'] == response_code
        assert row['HTTP_RESPONSE_BODY'] == response_body


class mocked_smtp_base():
    instances = []

    def __init__(self, kind, host, port, timeout, context=None):
        self.kind = kind
        self.host = host
        self.port = port
        self.tls = False
        self.timeout = timeout
        self.context = context
        self.auth_user = None
        self.auth_password = None
        self.message = None
        self.from_addr = None
        self.to_addrs = None
        mocked_smtp_base.add_instances(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def starttls(self):
        self.tls = True

    def login(self, user, password):
        self.auth_user = user
        self.auth_password = password

    def send_message(self, msg: EmailMessage, from_addr, to_addrs):
        self.message = msg
        self.from_addr = from_addr
        self.to_addrs = to_addrs

    def set_debuglevel(self, debuglevel):
        pass

    @classmethod
    def init_instances(cls):
        cls.instances = []

    @classmethod
    def add_instances(cls, instance):
        cls.instances.append(instance)

    @classmethod
    def get_instances(cls):
        return cls.instances


class mocked_smtp(mocked_smtp_base):
    def __init__(self, host, port, timeout):
        super().__init__('smtp', host, port, timeout)


class mocked_smtps(mocked_smtp_base):
    def __init__(self, host, port, timeout, context):
        super().__init__('smtps', host, port, timeout, context)
