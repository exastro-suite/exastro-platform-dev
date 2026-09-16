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
Lesson Service

ユーザーごと(ワークスペース横断)の学習事項（過去の会話から得られた失敗・教訓・注意点）の管理。
AIアシスタントのシステムプロンプトへの注入に使用する。
"""

from datetime import datetime
from typing import Optional, List, Tuple
from dataclasses import dataclass
from contextlib import closing
import ulid

from common_library.common.db import DBconnector
from libs import queries_ai_assistant

import globals


@dataclass
class Lesson:
    """User Lesson（学習事項）"""
    lesson_id: str
    lesson: str
    category: Optional[str]
    priority: int
    enabled: bool
    conversation_id: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]


class LessonService:
    """
    Lesson Service

    ユーザーごとの学習事項を管理
    """

    def create_lesson(
        self,
        organization_id: str,
        workspace_id: str,
        user_id: str,
        lesson: str,
        category: Optional[str] = None,
        priority: int = 5,
        enabled: bool = True,
        conversation_id: Optional[str] = None,
    ) -> Lesson:
        """
        学習事項を作成

        Args:
            organization_id: Organization ID (DB接続用、テーブルには保存しない)
            workspace_id: Workspace ID (DB接続用、テーブルには保存しない)
            user_id: User ID
            lesson: 学習事項の内容
            category: 分類 (任意)
            priority: 重要度 (1〜10。デフォルト5)
            enabled: 有効/無効フラグ (デフォルトTrue)
            conversation_id: 学習元の会話ID (任意。ワークスペースDB側のIDのため外部キーではない)

        Returns:
            Lesson: 作成した学習事項
        """
        lesson_id = ulid.new().str
        now = datetime.now()

        with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    queries_ai_assistant.SQL_INSERT_LESSON,
                    {
                        "lesson_id": lesson_id,
                        "user_id": user_id,
                        "lesson": lesson,
                        "category": category,
                        "priority": priority,
                        "enabled": enabled,
                        "conversation_id": conversation_id,
                    },
                )
                conn.commit()

        globals.logger.debug(
            f"Lesson created: id={lesson_id}, user={user_id}, category={category}, priority={priority}"
        )

        return Lesson(
            lesson_id=lesson_id,
            lesson=lesson,
            category=category,
            priority=priority,
            enabled=enabled,
            conversation_id=conversation_id,
            created_at=now.isoformat(),
            updated_at=now.isoformat(),
        )

    def get_lesson(
        self,
        organization_id: str,
        workspace_id: str,
        user_id: str,
        lesson_id: str,
    ) -> Optional[Lesson]:
        """
        学習事項を取得

        Args:
            organization_id: Organization ID (DB接続用、テーブルには保存しない)
            workspace_id: Workspace ID (DB接続用、テーブルには保存しない)
            user_id: User ID
            lesson_id: Lesson ID

        Returns:
            Lesson。見つからない場合はNone
        """
        with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    queries_ai_assistant.SQL_SELECT_LESSON,
                    {"lesson_id": lesson_id, "user_id": user_id},
                )
                row = cursor.fetchone()

        if not row:
            return None

        return self.__row_to_lesson(row)

    def list_lessons(
        self,
        organization_id: str,
        workspace_id: str,
        user_id: str,
        enabled: Optional[bool] = None,
        category: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[List[Lesson], int]:
        """
        学習事項一覧を取得

        Args:
            organization_id: Organization ID (DB接続用、テーブルには保存しない)
            workspace_id: Workspace ID (DB接続用、テーブルには保存しない)
            user_id: User ID
            enabled: 有効/無効フィルター (任意)
            category: 分類フィルター (任意)
            limit: 取得件数
            offset: オフセット

        Returns:
            Tuple[List[Lesson], int]: (学習事項一覧, LIMIT/OFFSET適用前の総件数)
        """
        params = {"user_id": user_id}

        # ENABLED/CATEGORYの絞り込みは任意なので、指定された場合のみAND句を連結する
        # Filtering by ENABLED/CATEGORY is optional, so append the AND clause only when specified
        extra_where = ""
        if enabled is not None:
            extra_where += " AND ENABLED = %(enabled)s"
            params["enabled"] = enabled
        if category is not None:
            extra_where += " AND CATEGORY = %(category)s"
            params["category"] = category

        list_query = queries_ai_assistant.SQL_LIST_LESSONS + extra_where + queries_ai_assistant.SQL_LIST_LESSONS_ORDER_LIMIT
        count_query = queries_ai_assistant.SQL_COUNT_LESSONS + extra_where

        with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    list_query,
                    {**params, "limit": limit, "offset": offset},
                )
                rows = cursor.fetchall()

                cursor.execute(count_query, params)
                total_count = cursor.fetchone()["total_count"]

        lessons = [self.__row_to_lesson(row) for row in rows]

        globals.logger.debug(
            f"Listed {len(lessons)} lessons (total_count={total_count}): "
            f"org={organization_id}, user={user_id}, enabled={enabled}, category={category}"
        )

        return lessons, total_count

    def update_lesson(
        self,
        organization_id: str,
        workspace_id: str,
        user_id: str,
        lesson_id: str,
        lesson: Optional[str] = None,
        category: Optional[str] = None,
        priority: Optional[int] = None,
        enabled: Optional[bool] = None,
    ) -> Optional[Lesson]:
        """
        学習事項を部分更新（PATCH。指定された項目のみ更新する）

        Args:
            organization_id: Organization ID (DB接続用、テーブルには保存しない)
            workspace_id: Workspace ID (DB接続用、テーブルには保存しない)
            user_id: User ID
            lesson_id: Lesson ID
            lesson: 変更後の学習事項の内容 (省略時は変更しない)
            category: 変更後の分類 (省略時は変更しない)
            priority: 変更後の重要度 (省略時は変更しない)
            enabled: 変更後の有効/無効フラグ (省略時は変更しない)

        Returns:
            Lesson。見つからない場合はNone
        """
        with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    queries_ai_assistant.SQL_SELECT_LESSON,
                    {"lesson_id": lesson_id, "user_id": user_id},
                )
                existing = cursor.fetchone()

                if not existing:
                    return None

                cursor.execute(
                    queries_ai_assistant.SQL_UPDATE_LESSON,
                    {
                        "lesson_id": lesson_id,
                        "user_id": user_id,
                        "lesson": lesson,
                        "category": category,
                        "priority": priority,
                        "enabled": enabled,
                    },
                )
                conn.commit()

        globals.logger.debug(
            f"Lesson updated: id={lesson_id}, user={user_id}"
        )

        # COALESCEで更新した内容をDBへ再度問い合わせずに反映する（未指定の項目は更新前の値を維持）
        # Reflect the COALESCE-based update without re-querying the DB (fields not specified keep their prior value)
        return Lesson(
            lesson_id=lesson_id,
            lesson=lesson if lesson is not None else existing["LESSON"],
            category=category if category is not None else existing["CATEGORY"],
            priority=priority if priority is not None else existing["PRIORITY"],
            enabled=enabled if enabled is not None else bool(existing["ENABLED"]),
            conversation_id=existing["CONVERSATION_ID"],
            created_at=existing["CREATE_TIMESTAMP"].isoformat() if existing["CREATE_TIMESTAMP"] else None,
            updated_at=datetime.now().isoformat(),
        )

    def bulk_update_enabled(
        self,
        organization_id: str,
        workspace_id: str,
        user_id: str,
        lesson_ids: List[str],
        enabled: bool,
    ) -> int:
        """
        複数の学習事項の有効/無効フラグを一括更新

        Args:
            organization_id: Organization ID (DB接続用、テーブルには保存しない)
            workspace_id: Workspace ID (DB接続用、テーブルには保存しない)
            user_id: User ID
            lesson_ids: 更新対象のLesson IDリスト
            enabled: 変更後の有効/無効フラグ

        Returns:
            int: 実際に更新された件数（他ユーザーの所有物や存在しないIDが含まれる場合、len(lesson_ids)より少なくなることがある）
        """
        # IN句のプレースホルダをID数に応じて動的に生成する（生の値を直接SQL文へ埋め込まない）
        # Dynamically build the IN clause placeholders based on the number of ids (never interpolate raw values into the SQL text)
        id_params = {f"id_{i}": lesson_id for i, lesson_id in enumerate(lesson_ids)}
        in_clause = ", ".join(f"%({key})s" for key in id_params)

        query = f"""
            UPDATE T_USER_LESSON
            SET ENABLED = %(enabled)s,
                LAST_UPDATE_TIMESTAMP = NOW(),
                LAST_UPDATE_USER = %(user_id)s
            WHERE USER_ID = %(user_id)s AND LESSON_ID IN ({in_clause})
        """

        with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    query,
                    {"enabled": enabled, "user_id": user_id, **id_params},
                )
                updated_count = cursor.rowcount
                conn.commit()

        globals.logger.debug(
            f"Bulk lesson update: user={user_id}, requested={len(lesson_ids)}, updated={updated_count}, enabled={enabled}"
        )

        return updated_count

    def delete_lesson(
        self,
        organization_id: str,
        workspace_id: str,
        user_id: str,
        lesson_id: str,
    ) -> bool:
        """
        学習事項を削除

        Args:
            organization_id: Organization ID (DB接続用、テーブルには保存しない)
            workspace_id: Workspace ID (DB接続用、テーブルには保存しない)
            user_id: User ID
            lesson_id: Lesson ID

        Returns:
            削除した学習事項があったかどうか（存在しない場合はFalse）
        """
        with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    queries_ai_assistant.SQL_DELETE_LESSON,
                    {"lesson_id": lesson_id, "user_id": user_id},
                )
                deleted = cursor.rowcount > 0
                conn.commit()

        if deleted:
            globals.logger.debug(f"Lesson deleted: id={lesson_id}, user={user_id}")

        return deleted

    def get_enabled_lessons_for_prompt(
        self,
        organization_id: str,
        workspace_id: str,
        user_id: str,
        limit: int = 20,
    ) -> List[Lesson]:
        """
        有効な学習事項を優先度・更新日時の降順で取得する（AIアシスタントのシステムプロンプトへの注入用）

        Args:
            organization_id: Organization ID (DB接続用、テーブルには保存しない)
            workspace_id: Workspace ID (DB接続用、テーブルには保存しない)
            user_id: User ID
            limit: 取得件数

        Returns:
            List[Lesson]: 有効な学習事項一覧（lesson/category/priorityのみ設定済み）
        """
        with closing(DBconnector().connect_workspacedb(organization_id, workspace_id)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    queries_ai_assistant.SQL_SELECT_ENABLED_LESSONS_FOR_PROMPT,
                    {"user_id": user_id, "limit": limit},
                )
                rows = cursor.fetchall()

        return [
            Lesson(
                lesson_id=None,
                lesson=row["LESSON"],
                category=row["CATEGORY"],
                priority=row["PRIORITY"],
                enabled=True,
                conversation_id=None,
                created_at=None,
                updated_at=None,
            )
            for row in rows
        ]

    @staticmethod
    def __row_to_lesson(row) -> Lesson:
        """DBの行データからLessonを構築する"""
        return Lesson(
            lesson_id=row["LESSON_ID"],
            lesson=row["LESSON"],
            category=row["CATEGORY"],
            priority=row["PRIORITY"],
            enabled=bool(row["ENABLED"]),
            conversation_id=row["CONVERSATION_ID"],
            created_at=row["CREATE_TIMESTAMP"].isoformat() if row["CREATE_TIMESTAMP"] else None,
            updated_at=row["LAST_UPDATE_TIMESTAMP"].isoformat() if row["LAST_UPDATE_TIMESTAMP"] else None,
        )


# シングルトンインスタンス
_lesson_service_instance: Optional[LessonService] = None


def get_lesson_service() -> LessonService:
    """
    Lesson Serviceのシングルトンインスタンスを取得

    Returns:
        LessonService
    """
    global _lesson_service_instance
    if _lesson_service_instance is None:
        _lesson_service_instance = LessonService()
    return _lesson_service_instance
