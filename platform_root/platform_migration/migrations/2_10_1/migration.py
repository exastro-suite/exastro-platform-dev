
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

from . import update_platform_db


def main():

    # エラーがあっても処理を継続する
    # continue processing even if there is an error
    result = []

    # プラットフォームデータベースの更新
    # Update platform database
    api = update_platform_db.update_platform_db()
    result.append(api.start())

    for i in result:
        if i != 0:
            return i

    return 0


if __name__ == '__main__':
    ret = main()
    exit(ret)
