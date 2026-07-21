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
import json

from common_library.common import multi_lang
from common_library.common import api_keycloak_tokens

import globals


MSG_FUNCTION_ID = "100044"


class update_keycloak_realm_sso():

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
        globals.logger.info(f"Keycloak realm SSO settings update start")
        globals.logger.info("#" * 50)

        try:
            # Get admin credentials from environment
            keycloak_user = os.environ.get("KEYCLOAK_USER", "admin")
            keycloak_password = os.environ.get("KEYCLOAK_PASSWORD", "password")

            # Get admin token
            token_response = api_keycloak_tokens.get_user_token(keycloak_user, keycloak_password, "master")
            token = token_response.json()['access_token']

            # Update SSO settings for master realm
            globals.logger.info("Updating SSO settings for master realm")
            self.__update_realm_sso("master", token)

            # Update SSO settings for all organization realms
            globals.logger.info("Updating SSO settings for organization realms")
            self.__update_sso_for_all_organizations(token)

        except Exception as e:
            globals.logger.error(f"Exception: {e}")
            import traceback
            globals.logger.error(traceback.format_exc())
            return 1

        globals.logger.info(f"Keycloak realm SSO settings update successful !!")
        return 0

    def __update_sso_for_all_organizations(self, token):
        """Update SSO settings for all organization realms

        Args:
            token (str): keycloak access token
        """
        globals.logger.info(f"### Start func:{inspect.currentframe().f_code.co_name}")

        # Get all realms
        api_url = "http://keycloak:8080/auth/admin/realms"
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(api_url, headers=headers)

        if response.status_code != 200:
            message_id = f"500-{MSG_FUNCTION_ID}001"
            message = multi_lang.get_text(
                message_id,
                "Failed to get realms"
            )
            globals.logger.error(f"{message} status:{response.status_code} response:{response.text}")
            raise Exception(message)

        realms = response.json()
        organization_realms = [r['realm'] for r in realms if r['realm'] != 'master']

        globals.logger.info(f"Found {len(organization_realms)} organization realms: {organization_realms}")

        # For each organization realm, update SSO settings
        for realm_name in organization_realms:
            globals.logger.info(f"Processing realm: {realm_name}")
            self.__update_realm_sso(realm_name, token)

        globals.logger.info(f"### End func:{inspect.currentframe().f_code.co_name}")

    def __update_realm_sso(self, realm_name, token):
        """Update SSO session timeout settings for a realm

        Args:
            realm_name (str): realm name
            token (str): keycloak access token
        """
        globals.logger.info(f"### Start func:{inspect.currentframe().f_code.co_name} realm={realm_name}")

        api_url = "http://keycloak:8080/auth/admin/realms"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        # Get current realm settings
        response = requests.get(f"{api_url}/{realm_name}", headers=headers)
        if response.status_code != 200:
            globals.logger.warning(f"Failed to get realm {realm_name}: {response.status_code}")
            return

        realm_config = response.json()

        # Check if SSO settings are already configured
        if 'ssoSessionIdleTimeout' in realm_config and 'ssoSessionMaxLifespan' in realm_config:
            globals.logger.info(f"SSO settings already exist for realm {realm_name}, skipping")
            return

        # Update SSO settings
        update_config = {
            "ssoSessionIdleTimeout": 86400,
            "ssoSessionMaxLifespan": 86400
        }

        response = requests.put(
            f"{api_url}/{realm_name}",
            headers=headers,
            data=json.dumps(update_config)
        )

        if response.status_code in [200, 204]:
            globals.logger.info(f"Successfully updated SSO settings for realm {realm_name}")
        else:
            globals.logger.error(f"Failed to update SSO settings for realm {realm_name}: {response.status_code} {response.text}")

        globals.logger.info(f"### End func:{inspect.currentframe().f_code.co_name}")


if __name__ == '__main__':
    ret = update_keycloak_realm_sso().start()
    exit(ret)
