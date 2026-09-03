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

"""
History Service

会話履歴（UI用）の管理
"""

import json
from contextlib import closing
from typing import Dict, List, Optional

import ulid
from common_library.common.db import DBconnector
from libs import queries_ai_assistant

import globals


class HistoryService:
    """
    会話履歴サービス
    """

    def create_history(
        self,
        organization_id: str,
        workspace_id: str,
        user_id: str,
        conversation_id: str,
        contents: List[Dict],
    ) -> Dict:
        """
        履歴レコードを作成

        Args:
            organization_id: Organization ID
            workspace_id: Workspace ID
            user_id: User ID
            conversation_id: Conversation ID
            contents: コンテンツ（JSON配列全体 - role, content, _timestamp等を含む配列）

        Returns:
            作成した履歴レコード
        """
        with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn:
            with closing(conn.cursor()) as cursor:
                # 次のSEQを取得
                cursor.execute(
                    queries_ai_assistant.SQL_GET_NEXT_HISTORY_SEQ,
                    {"conversation_id": conversation_id},
                )
                result = cursor.fetchone()
                next_seq = result["next_seq"]

                # 履歴レコードを作成
                history_id = ulid.new().str
                contents_json = json.dumps(contents, ensure_ascii=False)

                cursor.execute(
                    queries_ai_assistant.SQL_INSERT_HISTORY,
                    {
                        "history_id": history_id,
                        "conversation_id": conversation_id,
                        "history_seq": next_seq,
                        "contents": contents_json,
                        "user_id": user_id,
                    },
                )

                conn.commit()

                globals.logger.debug(
                    f"Created history: id={history_id}, conv={conversation_id}, "
                    f"seq={next_seq}"
                )

                return {
                    "history_id": history_id,
                    "conversation_id": conversation_id,
                    "history_seq": next_seq,
                    "contents": contents,
                }

    def get_latest_history(
        self,
        organization_id: str,
        workspace_id: str,
        conversation_id: str,
    ) -> Optional[List[Dict]]:
        """
        会話の最新の履歴スナップショット（JSON配列全体）を取得

        /completionsエンドポイントが会話のやり取りを継続する際、
        直前までの全ターン（role, content, _timestamp等）を取得するために使う。

        Args:
            organization_id: Organization ID
            workspace_id: Workspace ID
            conversation_id: Conversation ID

        Returns:
            直近のcontents（JSON配列）。履歴が存在しない場合はNone。
        """
        with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    queries_ai_assistant.SQL_SELECT_LATEST_HISTORY,
                    {"conversation_id": conversation_id},
                )
                row = cursor.fetchone()

        if not row:
            return None

        try:
            return json.loads(row["CONTENTS"])
        except (json.JSONDecodeError, TypeError):
            return None

    def list_histories(
        self,
        organization_id: str,
        workspace_id: str,
        user_id: str,
        conversation_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict]:
        """
        会話の履歴一覧を取得

        Args:
            organization_id: Organization ID
            workspace_id: Workspace ID
            user_id: User ID
            conversation_id: Conversation ID
            limit: 取得件数
            offset: オフセット（HISTORY_SEQ基準）

        Returns:
            履歴レコードのリスト（各レコードにJSON配列全体を含む）
        """
        with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn:
            with closing(conn.cursor()) as cursor:
                # 会話の存在確認とオーナーシップ確認
                cursor.execute(
                    queries_ai_assistant.SQL_SELECT_CONVERSATION_FOR_HISTORY,
                    {"conversation_id": conversation_id, "user_id": user_id},
                )
                if not cursor.fetchone():
                    raise ValueError(
                        f"Conversation not found or access denied: {conversation_id}"
                    )

                # 履歴を取得
                cursor.execute(
                    queries_ai_assistant.SQL_LIST_HISTORIES,
                    {
                        "conversation_id": conversation_id,
                        "limit": limit,
                        "offset": offset,
                    },
                )

                histories = []
                for row in cursor.fetchall():
                    # CONTENTSをJSONとしてパース
                    try:
                        contents = json.loads(row["CONTENTS"])
                    except (json.JSONDecodeError, TypeError):
                        contents = []

                    history_dict = {
                        "history_id": row["HISTORY_ID"],
                        "conversation_id": row["CONVERSATION_ID"],
                        "history_seq": row["HISTORY_SEQ"],
                        "contents": contents,
                        "created_at": row["CREATE_TIMESTAMP"].isoformat() if row["CREATE_TIMESTAMP"] else None,
                        "updated_at": row["LAST_UPDATE_TIMESTAMP"].isoformat() if row["LAST_UPDATE_TIMESTAMP"] else None,
                    }

                    histories.append(history_dict)

                globals.logger.debug(
                    f"Listed {len(histories)} histories: conv={conversation_id}"
                )

                return histories

    def replace_histories(
        self,
        organization_id: str,
        workspace_id: str,
        user_id: str,
        conversation_id: str,
        histories: List[List[Dict]],
    ) -> List[Dict]:
        """
        会話履歴を全置き換え

        既存のT_CHAT_HISTORYレコードを全て削除し、指定されたcontents配列群を
        新しい履歴レコードとして登録し直す（GETで取得できる内容をそのまま置き換えるイメージ）。

        Args:
            organization_id: Organization ID
            workspace_id: Workspace ID
            user_id: User ID
            conversation_id: Conversation ID
            histories: 置き換え後の履歴レコード一覧（各要素はcontents配列）

        Returns:
            置き換え後の履歴レコードのリスト

        Raises:
            ValueError: 会話が見つからない
        """
        with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn:
            with closing(conn.cursor()) as cursor:
                # 会話の存在確認とオーナーシップ確認
                cursor.execute(
                    queries_ai_assistant.SQL_SELECT_CONVERSATION_FOR_HISTORY,
                    {"conversation_id": conversation_id, "user_id": user_id},
                )
                if not cursor.fetchone():
                    raise ValueError(
                        f"Conversation not found or access denied: {conversation_id}"
                    )

                # 既存の履歴を全削除してから置き換え後の内容を登録し直す
                cursor.execute(
                    queries_ai_assistant.SQL_DELETE_HISTORIES,
                    {"conversation_id": conversation_id},
                )

                results = []
                for index, contents in enumerate(histories, start=1):
                    history_id = ulid.new().str
                    contents_json = json.dumps(contents, ensure_ascii=False)

                    cursor.execute(
                        queries_ai_assistant.SQL_INSERT_HISTORY,
                        {
                            "history_id": history_id,
                            "conversation_id": conversation_id,
                            "history_seq": index,
                            "contents": contents_json,
                            "user_id": user_id,
                        },
                    )

                    results.append({
                        "history_id": history_id,
                        "conversation_id": conversation_id,
                        "history_seq": index,
                        "contents": contents,
                    })

                conn.commit()

                globals.logger.debug(
                    f"Replaced histories: conv={conversation_id}, count={len(results)}"
                )

                return results

    def delete_histories(
        self,
        organization_id: str,
        workspace_id: str,
        user_id: str,
        conversation_id: str,
    ) -> int:
        """
        会話履歴を全削除

        Args:
            organization_id: Organization ID
            workspace_id: Workspace ID
            user_id: User ID
            conversation_id: Conversation ID

        Returns:
            削除件数

        Raises:
            ValueError: 会話が見つからない
        """
        with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn:
            with closing(conn.cursor()) as cursor:
                # 会話の存在確認とオーナーシップ確認
                cursor.execute(
                    queries_ai_assistant.SQL_SELECT_CONVERSATION_FOR_HISTORY,
                    {"conversation_id": conversation_id, "user_id": user_id},
                )
                if not cursor.fetchone():
                    raise ValueError(
                        f"Conversation not found or access denied: {conversation_id}"
                    )

                cursor.execute(
                    queries_ai_assistant.SQL_DELETE_HISTORIES,
                    {"conversation_id": conversation_id},
                )
                deleted_count = cursor.rowcount

                conn.commit()

                globals.logger.debug(
                    f"Deleted histories: conv={conversation_id}, count={deleted_count}"
                )

                return deleted_count


# シングルトンインスタンス
_service_instance = None


def get_history_service() -> HistoryService:
    """
    HistoryServiceのシングルトンインスタンスを取得

    Returns:
        HistoryService
    """
    global _service_instance
    if _service_instance is None:
        _service_instance = HistoryService()
    return _service_instance
