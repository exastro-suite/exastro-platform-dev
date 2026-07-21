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
from . import update_keycloak
from . import update_keycloak_audience
from . import update_keycloak_realm_sso


def main():

    # Keycloak 26.5 compatibility: Add SSO session timeout settings to realms
    api = update_keycloak_realm_sso.update_keycloak_realm_sso()
    result = api.start()
    if result != 0:
        return result

    # Keycloak 25 compatibility: Add sub claim mapper to _platform-console client
    api = update_keycloak.update_keycloak()
    result = api.start()
    if result != 0:
        return result

    # Keycloak 26.6 compatibility: Add audience mapper to _platform-console client
    api = update_keycloak_audience.update_keycloak_audience()
    result = api.start()

    return result


if __name__ == '__main__':
    ret = main()
    exit(ret)
