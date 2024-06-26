
#   Copyright 2023 NEC Corporation
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
import migration_common
from contextlib import closing

import globals
from . import update_organization_db
from . import create_update_workspace_db
from .libs import queries_db_migration


def main():
    
    # オーガナイゼーションデータベースの更新
    # Update organization database
    api = update_organization_db.update_organization_db()
    result = api.start()

    # エラーがあっても処理を継続する
    # continue processing even if there is an error
    
    # ワークスペースデータベースの作成・更新
    # Create and update workspace database
    api = create_update_workspace_db.create_update_workspace_db()
    result = api.start()

    # エラーがあっても処理を継続する
    # continue processing even if there is an error

    # 共通認証基盤DBのテーブル作成
    # PlatformDB table creation
    with closing(migration_common.connect_platform_db()) as conn:
        with conn.cursor() as cursor:
            for query in queries_db_migration.CREATE_TABLES:
                globals.logger.info(f'EXECUTE SQL:{query}')
                cursor.execute(query)

            for query in queries_db_migration.UPDATE_TABLES:
                globals.logger.info(f'EXECUTE SQL:{query}')
                cursor.execute(query)

            conn.commit()

    if result != 0:
        return result

    return 0


if __name__ == '__main__':
    ret = main()
    exit(ret)
