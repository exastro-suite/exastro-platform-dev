#   Copyright 2025 NEC Corporation
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

CREATE_TABLES_PLATFORM_DB = [
    """
    -- 生成AI情報 / generative ai information
    CREATE TABLE IF NOT EXISTS T_GENERATIVE_AI_SERVICES
    (
        AI_ID		                    VARCHAR(255) NOT NULL,                      -- 生成AI情報ID
        AI_SERVICE		                VARCHAR(255),                               -- 生成AIサービス
        AI_MODEL		                VARCHAR(255),                               -- 生成AIモデル
        AI_DISPLAY_NAME	                VARCHAR(255),                               -- 生成AI表示名
        ENDPOINT_URL	                VARCHAR(4000),	                            -- エンドポイントURL
        HTTP_HEADERS	                JSON,       	                            -- HTTP-HEADERS
        EXTERNAL_ACCOUNT_DEFINITION     JSON,	                                    -- 外部アカウント項目定義
        ENABLED                         BOOLEAN,	                                -- 有効無効
        DISPLAY_ORDER	                INT,	                                    -- 表示順
        CREATE_TIMESTAMP		        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,    -- 作成日時
        CREATE_USER		                VARCHAR(40),                                -- 作成者
        LAST_UPDATE_TIMESTAMP		    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,    -- 最終更新日時
        LAST_UPDATE_USER		        VARCHAR(40),                                -- 最終更新者
        PRIMARY KEY (AI_ID)
    )ENGINE = InnoDB, CHARSET = utf8mb4, COLLATE = utf8mb4_bin, ROW_FORMAT=COMPRESSED ,KEY_BLOCK_SIZE=8;
    """
]

CREATE_TABLES_ORGANIZATION_DB = [
    """
    -- 生成AI利用 / generative ai usage
    CREATE TABLE IF NOT EXISTS T_GENERATIVE_AI_USAGE
    (
        WORKSPACE_ID                    VARCHAR(36) NOT NULL,                       -- Workspace ID
        AI_ID		                    VARCHAR(255) NOT NULL,                      -- 生成AI情報ID
        PRIMARY KEY (WORKSPACE_ID, AI_ID)
    )ENGINE = InnoDB, CHARSET = utf8mb4, COLLATE = utf8mb4_bin, ROW_FORMAT=COMPRESSED ,KEY_BLOCK_SIZE=8;
    """,
    """
    -- 外部アカウント情報 / external account information
    CREATE TABLE IF NOT EXISTS T_EXTERNAL_ACCOUNTS
    (
        USER_ID 		                VARCHAR(40) NOT NULL,                       -- 該当のユーザーID
        EXTERNAL_ID                     VARCHAR(26) NOT NULL,                       -- 外部アカウント情報キー
        CATEGORY                        VARCHAR(255),                               -- 外部アカウントカテゴリー
        TYPE                            VARCHAR(255),                               -- 外部アカウント種類
        DISPLAY_NAME                    VARCHAR(255),                               -- 表示名
        DETAILS                         LONGTEXT,	                                -- 詳細情報
        CREATE_TIMESTAMP		        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,    -- 作成日時
        CREATE_USER		                VARCHAR(40),                                -- 作成者
        LAST_UPDATE_TIMESTAMP		    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,    -- 最終更新日時
        LAST_UPDATE_USER		        VARCHAR(40),                                -- 最終更新者
        PRIMARY KEY (USER_ID, EXTERNAL_ID)
    )ENGINE = InnoDB, CHARSET = utf8mb4, COLLATE = utf8mb4_bin, ROW_FORMAT=COMPRESSED ,KEY_BLOCK_SIZE=8;
    """,
    """
    -- 外部アカウント情報 利用Workspace / external account information usage workspace
    CREATE TABLE IF NOT EXISTS T_EXTERNAL_ACCOUNTS_WORKSPACE
    (
        USER_ID 		                VARCHAR(40) NOT NULL,                       -- 該当のユーザーID
        EXTERNAL_ID                     VARCHAR(26) NOT NULL,                       -- 外部アカウント情報キー
        WORKSPACE_ID                    VARCHAR(36) NOT NULL,                       -- Workspace ID
        PRIMARY KEY (USER_ID, EXTERNAL_ID, WORKSPACE_ID)
    )ENGINE = InnoDB, CHARSET = utf8mb4, COLLATE = utf8mb4_bin, ROW_FORMAT=COMPRESSED ,KEY_BLOCK_SIZE=8;
    """
]
