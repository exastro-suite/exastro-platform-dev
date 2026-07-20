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

import inspect
import os
import requests

from common_library.common import multi_lang
from common_library.common import api_keycloak_tokens
from common_library.common import api_keycloak_clients

import globals


MSG_FUNCTION_ID = "100041"


class update_keycloak():

    def __init__(self):
        """init
        """
        self.step_count = 1
        self.step_max = 1

    def start(self):
        """start

        Returns:
            bool: result
        """
        globals.logger.info("#" * 50)
        globals.logger.info(f"Keycloak client update start")
        globals.logger.info("#" * 50)

        try:
            # Get admin credentials from environment
            keycloak_user = os.environ.get("KEYCLOAK_USER", "admin")
            keycloak_password = os.environ.get("KEYCLOAK_PASSWORD", "password")

            # Get admin token
            token_response = api_keycloak_tokens.get_user_token(keycloak_user, keycloak_password, "master")
            token = token_response.json()['access_token']

            # Add sub mapper to master realm clients
            globals.logger.info("Adding sub mapper to master realm clients")
            stats = api_keycloak_clients.add_sub_mapper_to_realm_clients("master", token)
            globals.logger.info(f"Master realm: {stats}")

            # Add sub mapper to all organization realm clients
            globals.logger.info("Adding sub mapper to organization realm clients")
            self.__add_sub_mapper_to_all_organizations(token)

        except Exception as e:
            globals.logger.error(f"Exception: {e}")
            import traceback
            globals.logger.error(traceback.format_exc())
            return 1

        globals.logger.info(f"Keycloak client update successful !!")
        return 0

    def __add_sub_mapper_to_all_organizations(self, token):
        """Add sub mapper to all organization realm clients

        Args:
            token (str): keycloak access token
        """
        globals.logger.info(f"### Start func:{inspect.currentframe().f_code.co_name}")

        # Get all realms
        api_url = "http://keycloak:8080/auth/admin/realms"
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(api_url, headers=headers)

        if response.status_code != 200:
            message_id = f"500-{MSG_FUNCTION_ID}004"
            message = multi_lang.get_text(
                message_id,
                "Failed to get realms"
            )
            globals.logger.error(f"{message} status:{response.status_code} response:{response.text}")
            raise Exception(message)

        realms = response.json()
        organization_realms = [r['realm'] for r in realms if r['realm'] != 'master']

        globals.logger.info(f"Found {len(organization_realms)} organization realms: {organization_realms}")

        # For each organization realm, add sub mapper to all openid-connect clients
        for realm_name in organization_realms:
            globals.logger.info(f"Processing realm: {realm_name}")
            stats = api_keycloak_clients.add_sub_mapper_to_realm_clients(realm_name, token)
            globals.logger.info(f"Realm {realm_name}: {stats}")

        globals.logger.info(f"### Succeed func:{inspect.currentframe().f_code.co_name}")
