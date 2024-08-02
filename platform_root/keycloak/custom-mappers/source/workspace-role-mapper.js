/*
#   Copyright 2024 NEC Corporation
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
*/

// Arrayを使うための宣言 / Declaration for using Array
var ArrayList = Java.type("java.util.ArrayList");
var forEach = Array.prototype.forEach;

// ロールの格納変数 / Role storage variables
var roles = new ArrayList();

// Workspcaeのロールが含まれるclient-id名(realm-idと同じID名)
// client-id name that includes the Workspcae role (same ID name as realm-id)
var workspaceRoleClientId = realm.getId();

// Workspcaeのロールが含まれるclientModelを特定する
// Identify the clientModel that contains the Workspcae role
var role_client = null;
keycloakSession.clients().getClientsStream(realm).forEach(function (clientModel) {
    if(clientModel.getClientId() == realm.getId()) {
        role_client = clientModel;
    }
});


if (role_client !== null) {
    // ユーザーにマッピングされているWorkspcaeのロールを取得する
    // Get the Workspcae role mapped to a user
    user.getClientRoleMappingsStream(role_client).forEach(function (roleModel) {
        // ロールの属性情報の中のkindを取得する
        // Get kind in role attribute information
        kind = roleModel.getFirstAttribute("kind");
        if (kind === "workspace") {
            // kindがWorkspaceのもののみを対象とする
            // Targets only those whose kind is Workspace
            roleModel.getCompositesStream().forEach(function (compositeRoleModel) {
                // 先頭の1文字目が"_"のロールはワークスペースIDではないので除外する
                // Exclude roles whose first character is "_" as they are not workspace IDs.
                if(compositeRoleModel.getName().substr(0,1) !== "_") {
                    // レルムID.ロール名.ワークスペースIDをSAMLのロール名とする
                    // Set realm ID.role name.workspace ID as SAML role name
                    roles.add(realm.getId() + '.' + roleModel.getName() + '.' + compositeRoleModel.getName());
                }
            });
        }
    });
}

exports = roles;
