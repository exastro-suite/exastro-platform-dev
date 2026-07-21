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

# import inspect
import os
import requests

# User Imports
import globals  # 共通的なglobals Common globals


def client_create(realm_name, client_json, token):
    """クライアント作成 client create

    Args:
        realm_name (str): realm name
        client_json (disct): client create parameter
        toekn (str): token

    Returns:
        Response: HTTP Respose (success : .status_code=200)
    """
    globals.logger.info('Post keycloak clients. client_id={}'.format(client_json.get("clientId")))

    header_para = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
    }

    # 呼び出し先設定 requests setting
    api_url = "{}://{}:{}".format(os.environ['API_KEYCLOAK_PROTOCOL'], os.environ['API_KEYCLOAK_HOST'], os.environ['API_KEYCLOAK_PORT'])

    request_response = requests.post(f"{api_url}/auth/admin/realms/{realm_name}/clients",
                                     headers=header_para,
                                     json=client_json,
                                     timeout=(12, 600)
                                     )

    return request_response


def client_update(realm_name, client_uid, client_json, token):
    """クライアント作成 client create

    Args:
        realm_name (str): realm name
        client_uid (str): client id (uuid)
        client_json (disct): client update parameter
        toekn (str): token

    Returns:
        Response: HTTP Respose (success : .status_code=200)
    """
    globals.logger.info('Put keycloak clients. client_id={}'.format(client_uid))

    header_para = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
    }

    # 呼び出し先設定 requests setting
    api_url = "{}://{}:{}".format(os.environ['API_KEYCLOAK_PROTOCOL'], os.environ['API_KEYCLOAK_HOST'], os.environ['API_KEYCLOAK_PORT'])

    request_response = requests.put(
        f"{api_url}/auth/admin/realms/{realm_name}/clients/{client_uid}",
        headers=header_para,
        json=client_json,
        timeout=(12, 600)
    )

    return request_response


def clients_get(realm_name, client_id, token):
    """クライアント情報取得 client info get

    Args:
        realm_name (str): realm name
        client_id (str): client id
        toekn (str): token

    Returns:
        Response: HTTP Respose (success : .status_code=200)
    """
    globals.logger.debug('Get keycloak client role. client_id={}'.format(client_id))

    header_para = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
    }

    # client_idが指定されている場合は、querystringで条件を設定
    # If client_id is specified, set the condition with querystring
    if client_id:
        query_para = {
            "clientId": client_id,
        }
    else:
        query_para = None

    globals.logger.debug("client get send")
    # 呼び出し先設定 requests setting
    api_url = "{}://{}:{}".format(os.environ['API_KEYCLOAK_PROTOCOL'], os.environ['API_KEYCLOAK_HOST'], os.environ['API_KEYCLOAK_PORT'])

    request_response = requests.get(f"{api_url}/auth/admin/realms/{realm_name}/clients",
                                    headers=header_para,
                                    params=query_para,
                                    timeout=(12, 600)
                                    )

    # globals.logger.debug(request_response.text)

    return request_response


def client_secret_create(realm_name, client_id, token):
    """クライアントシークレット作成 client secret create

    Args:
        realm_name (str): realm name
        client_id (str): client id (not client-id)
        toekn (str): token

    Returns:
        Response: HTTP Respose (success : .status_code=200)
    """
    globals.logger.info('Post keycloak clients secret. client_id={}'.format(client_id))

    header_para = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
    }

    # 呼び出し先設定 requests setting
    api_url = "{}://{}:{}".format(os.environ['API_KEYCLOAK_PROTOCOL'], os.environ['API_KEYCLOAK_HOST'], os.environ['API_KEYCLOAK_PORT'])

    request_response = requests.post(
        f"{api_url}/auth/admin/realms/{realm_name}/clients/{client_id}/client-secret",
        headers=header_para,
        timeout=(12, 600)
    )

    return request_response


def client_secret_get(realm_name, client_id, token):
    """クライアントシークレット取得 client secret get

    Args:
        realm_name (str): realm name
        client_id (str): client id (not client-id)
        toekn (str): token

    Returns:
        Response: HTTP Respose (success : .status_code=200)
    """
    globals.logger.debug('Get keycloak clients secret. client_id={}'.format(client_id))

    header_para = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
    }

    # 呼び出し先設定 requests setting
    api_url = "{}://{}:{}".format(os.environ['API_KEYCLOAK_PROTOCOL'], os.environ['API_KEYCLOAK_HOST'], os.environ['API_KEYCLOAK_PORT'])

    request_response = requests.get(f"{api_url}/auth/admin/realms/{realm_name}/clients/{client_id}/client-secret",
                                    headers=header_para,
                                    timeout=(12, 600)
                                    )

    return request_response


def add_sub_mapper_to_client(realm_name, client_id, token):
    """Add sub claim protocol mapper to a specific client

    Keycloak 25+ no longer includes 'sub' claim by default in tokens.
    This function adds the 'sub' protocol mapper to a client.

    Args:
        realm_name (str): realm name
        client_id (str): client internal ID (not clientId)
        token (str): keycloak admin access token

    Returns:
        bool: True if added or already exists, False if failed
    """
    globals.logger.debug(f'Adding sub mapper to client {client_id} in realm {realm_name}')

    header_para = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
    }

    # 呼び出し先設定 requests setting
    api_url = "{}://{}:{}".format(os.environ['API_KEYCLOAK_PROTOCOL'], os.environ['API_KEYCLOAK_HOST'], os.environ['API_KEYCLOAK_PORT'])
    mappers_url = f"{api_url}/auth/admin/realms/{realm_name}/clients/{client_id}/protocol-mappers/models"

    # Check if sub mapper already exists
    response = requests.get(mappers_url, headers=header_para, timeout=(12, 600))
    
    if response.status_code == 200:
        existing_mappers = response.json()
        has_sub_mapper = any(
            mapper.get('name') == 'sub' or mapper.get('config', {}).get('claim.name') == 'sub'
            for mapper in existing_mappers
        )
        
        if has_sub_mapper:
            globals.logger.debug(f'sub mapper already exists in client {client_id}')
            return True

    # Add sub mapper
    mapper_config = {
        "name": "sub",
        "protocol": "openid-connect",
        "protocolMapper": "oidc-usermodel-property-mapper",
        "consentRequired": False,
        "config": {
            "userinfo.token.claim": "true",
            "user.attribute": "id",
            "id.token.claim": "true",
            "access.token.claim": "true",
            "claim.name": "sub",
            "jsonType.label": "String"
        }
    }

    response = requests.post(mappers_url, headers=header_para, json=mapper_config, timeout=(12, 600))

    if response.status_code == 201:
        globals.logger.info(f'Successfully added sub mapper to client {client_id}')
        return True
    else:
        globals.logger.warning(f'Failed to add sub mapper to client {client_id}: {response.status_code} - {response.text}')
        return False


def add_sub_mapper_to_realm_clients(realm_name, token, exclude_builtin=True):
    """Add sub claim protocol mapper to all openid-connect clients in a realm

    Keycloak 25+ no longer includes 'sub' claim by default in tokens.
    This function adds the 'sub' protocol mapper to all user-facing clients in a realm.

    Args:
        realm_name (str): realm name
        token (str): keycloak admin access token
        exclude_builtin (bool): exclude built-in system clients (default: True)

    Returns:
        dict: {"success": int, "failed": int, "skipped": int}
    """
    globals.logger.info(f'Adding sub mapper to all clients in realm {realm_name}')

    header_para = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
    }

    # 呼び出し先設定 requests setting
    api_url = "{}://{}:{}".format(os.environ['API_KEYCLOAK_PROTOCOL'], os.environ['API_KEYCLOAK_HOST'], os.environ['API_KEYCLOAK_PORT'])

    # Get all clients in the realm
    response = requests.get(f"{api_url}/auth/admin/realms/{realm_name}/clients", headers=header_para, timeout=(12, 600))

    if response.status_code != 200:
        globals.logger.warning(f'Failed to get clients for realm {realm_name}: {response.status_code}')
        return {"success": 0, "failed": 0, "skipped": 0}

    clients = response.json()

    # Filter openid-connect clients
    if exclude_builtin:
        target_clients = [
            c for c in clients
            if c.get('protocol') == 'openid-connect'
            and not c['clientId'].startswith('account')
            and not c['clientId'].startswith('admin')
            and not c['clientId'].startswith('broker')
            and not c['clientId'].startswith('realm-management')
            and not c['clientId'].startswith('security-admin-console')
        ]
    else:
        target_clients = [c for c in clients if c.get('protocol') == 'openid-connect']

    globals.logger.info(f'Found {len(target_clients)} target clients in realm {realm_name}')

    stats = {"success": 0, "failed": 0, "skipped": 0}

    for client in target_clients:
        client_id = client['clientId']
        internal_id = client['id']

        try:
            result = add_sub_mapper_to_client(realm_name, internal_id, token)
            if result:
                stats["success"] += 1
            else:
                stats["failed"] += 1
        except Exception as e:
            globals.logger.warning(f'Error adding sub mapper to {client_id}: {e}')
            stats["failed"] += 1

    globals.logger.info(f'Completed adding sub mappers to {realm_name}: {stats}')
    return stats


def add_audience_mapper_to_client(realm_name, client_id, token, audience_client_id="_platform"):
    """Add audience protocol mapper to a specific client

    Keycloak 26+ requires explicit audience configuration for token introspection.
    This function adds the audience mapper to a client.

    Args:
        realm_name (str): realm name
        client_id (str): client internal ID (not clientId)
        token (str): keycloak admin access token
        audience_client_id (str): the audience to add (default: "_platform")

    Returns:
        bool: True if added or already exists, False if failed
    """
    globals.logger.debug(f'Adding audience mapper to client {client_id} in realm {realm_name}')

    header_para = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
    }

    # 呼び出し先設定 requests setting
    api_url = "{}://{}:{}".format(os.environ['API_KEYCLOAK_PROTOCOL'], os.environ['API_KEYCLOAK_HOST'], os.environ['API_KEYCLOAK_PORT'])
    mappers_url = f"{api_url}/auth/admin/realms/{realm_name}/clients/{client_id}/protocol-mappers/models"

    # Check if audience mapper already exists
    response = requests.get(mappers_url, headers=header_para, timeout=(12, 600))
    
    if response.status_code == 200:
        existing_mappers = response.json()
        has_audience_mapper = any(
            mapper.get('name') == f'audience-{audience_client_id}'
            for mapper in existing_mappers
        )
        
        if has_audience_mapper:
            globals.logger.debug(f'audience mapper already exists in client {client_id}')
            return True

    # Add audience mapper
    mapper_config = {
        "name": f"audience-{audience_client_id}",
        "protocol": "openid-connect",
        "protocolMapper": "oidc-audience-mapper",
        "consentRequired": False,
        "config": {
            "included.client.audience": audience_client_id,
            "id.token.claim": "false",
            "access.token.claim": "true",
            "introspection.token.claim": "true"
        }
    }

    response = requests.post(mappers_url, headers=header_para, json=mapper_config, timeout=(12, 600))

    if response.status_code == 201:
        globals.logger.info(f'Successfully added audience mapper to client {client_id}')
        return True
    else:
        globals.logger.warning(f'Failed to add audience mapper to client {client_id}: {response.status_code} - {response.text}')
        return False


def add_audience_mapper_to_realm_clients(realm_name, token, audience_client_id="_platform", target_client_filter="_platform-console"):
    """Add audience protocol mapper to specific clients in a realm

    Keycloak 26+ requires explicit audience configuration for token introspection.
    This function adds the audience mapper to clients matching the filter.

    Args:
        realm_name (str): realm name
        token (str): keycloak admin access token
        audience_client_id (str): the audience to add (default: "_platform")
        target_client_filter (str): filter for client IDs (default: "_platform-console")

    Returns:
        dict: {"success": int, "failed": int, "skipped": int}
    """
    globals.logger.info(f'Adding audience mapper to clients matching "{target_client_filter}" in realm {realm_name}')

    header_para = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
    }

    # 呼び出し先設定 requests setting
    api_url = "{}://{}:{}".format(os.environ['API_KEYCLOAK_PROTOCOL'], os.environ['API_KEYCLOAK_HOST'], os.environ['API_KEYCLOAK_PORT'])

    # Get all clients in the realm
    response = requests.get(f"{api_url}/auth/admin/realms/{realm_name}/clients", headers=header_para, timeout=(12, 600))

    if response.status_code != 200:
        globals.logger.warning(f'Failed to get clients for realm {realm_name}: {response.status_code}')
        return {"success": 0, "failed": 0, "skipped": 0}

    clients = response.json()

    # Filter target clients (by default, only _platform-console)
    target_clients = [
        c for c in clients
        if c.get('protocol') == 'openid-connect'
        and c['clientId'] == target_client_filter
    ]

    globals.logger.info(f'Found {len(target_clients)} target clients in realm {realm_name}')

    stats = {"success": 0, "failed": 0, "skipped": 0}

    for client in target_clients:
        client_id = client['clientId']
        internal_id = client['id']

        try:
            result = add_audience_mapper_to_client(realm_name, internal_id, token, audience_client_id)
            if result:
                stats["success"] += 1
            else:
                stats["failed"] += 1
        except Exception as e:
            globals.logger.warning(f'Error adding audience mapper to {client_id}: {e}')
            stats["failed"] += 1

    globals.logger.info(f'Completed adding audience mappers to {realm_name}: {stats}')
    return stats
