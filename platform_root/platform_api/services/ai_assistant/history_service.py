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
from datetime import datetime
from typing import Dict, List, Optional

import ulid
from common_library.common.db import DBconnector

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
        role: str,
        content: List[Dict],
        timestamp: str,
        thinking_ms: Optional[int] = None,
        model: Optional[str] = None,
    ) -> Dict:
        """
        履歴レコードを作成

        Args:
            organization_id: Organization ID
            workspace_id: Workspace ID
            user_id: User ID
            conversation_id: Conversation ID
            role: ロール (user/assistant)
            content: コンテンツ（JSON配列）
            timestamp: タイムスタンプ (ISO 8601)
            thinking_ms: 思考時間（ミリ秒、optional）
            model: モデル名（optional）

        Returns:
            作成した履歴レコード
        """
        with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn:
            with closing(conn.cursor()) as cursor:
                # 次のSEQを取得
                cursor.execute(
                    """
                    SELECT COALESCE(MAX(HISTORY_SEQ), 0) + 1 AS next_seq
                    FROM T_CHAT_HISTORY
                    WHERE CONVERSATION_ID = %s
                    """,
                    (conversation_id,),
                )
                result = cursor.fetchone()
                next_seq = result["next_seq"]

                # 履歴レコードを作成
                history_id = ulid.new().str
                content_json = json.dumps(content, ensure_ascii=False)

                # timestampをdatetimeに変換
                if isinstance(timestamp, str):
                    timestamp_dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                else:
                    timestamp_dt = timestamp

                cursor.execute(
                    """
                    INSERT INTO T_CHAT_HISTORY
                    (
                        HISTORY_ID, CONVERSATION_ID, HISTORY_SEQ, ROLE,
                        CONTENT, TIMESTAMP, THINKING_MS, MODEL,
                        CREATE_TIMESTAMP, CREATE_USER
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s)
                    """,
                    (
                        history_id,
                        conversation_id,
                        next_seq,
                        role,
                        content_json,
                        timestamp_dt,
                        thinking_ms,
                        model,
                        user_id,
                    ),
                )

                conn.commit()

                globals.logger.debug(
                    f"Created history: id={history_id}, conv={conversation_id}, "
                    f"seq={next_seq}, role={role}"
                )

                return {
                    "history_id": history_id,
                    "conversation_id": conversation_id,
                    "history_seq": next_seq,
                    "role": role,
                    "content": content,
                    "timestamp": timestamp,
                    "thinking_ms": thinking_ms,
                    "model": model,
                }

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
            履歴レコードのリスト
        """
        with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn:
            with closing(conn.cursor()) as cursor:
                # 会話の存在確認とオーナーシップ確認
                cursor.execute(
                    """
                    SELECT CONVERSATION_ID
                    FROM T_CHAT_CONVERSATION
                    WHERE CONVERSATION_ID = %s AND USER_ID = %s
                    """,
                    (conversation_id, user_id),
                )
                if not cursor.fetchone():
                    raise ValueError(
                        f"Conversation not found or access denied: {conversation_id}"
                    )

                # 履歴を取得
                cursor.execute(
                    """
                    SELECT
                        HISTORY_ID, CONVERSATION_ID, HISTORY_SEQ, ROLE,
                        CONTENT, TIMESTAMP, THINKING_MS, MODEL,
                        CREATE_TIMESTAMP
                    FROM T_CHAT_HISTORY
                    WHERE CONVERSATION_ID = %s
                    ORDER BY HISTORY_SEQ ASC
                    LIMIT %s OFFSET %s
                    """,
                    (conversation_id, limit, offset),
                )

                histories = []
                for row in cursor.fetchall():
                    # CONTENTをJSONとしてパース
                    try:
                        content = json.loads(row["CONTENT"])
                    except (json.JSONDecodeError, TypeError):
                        content = []

                    history_dict = {
                        "history_id": row["HISTORY_ID"],
                        "conversation_id": row["CONVERSATION_ID"],
                        "history_seq": row["HISTORY_SEQ"],
                        "role": row["ROLE"],
                        "content": content,
                        "_timestamp": row["TIMESTAMP"].isoformat() + 'Z' if row["TIMESTAMP"] else None,
                    }

                    # オプションフィールドを追加
                    if row["THINKING_MS"] is not None:
                        history_dict["_thinkingMs"] = row["THINKING_MS"]
                    if row["MODEL"]:
                        history_dict["_model"] = row["MODEL"]

                    histories.append(history_dict)

                globals.logger.debug(
                    f"Listed {len(histories)} histories: conv={conversation_id}"
                )

                return histories


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
