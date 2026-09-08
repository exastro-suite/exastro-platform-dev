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
System Prompt Loader

service_id と user_language に基づいてシステムプロンプトを読み込む
"""

import os
from pathlib import Path
from typing import Optional

import globals


class SystemPromptLoader:
    """
    システムプロンプトローダー

    ファイル命名規則:
    - {service_id}_base.txt: 基本プロンプト
    - {service_id}_jp.txt: 日本語用プロンプト
    - {service_id}_en.txt: 英語用プロンプト
    """

    def __init__(self, prompts_dir: Optional[str] = None):
        """
        初期化

        Args:
            prompts_dir: プロンプトファイルのディレクトリパス
                        （Noneの場合はデフォルトパスを使用）
        """
        if prompts_dir is None:
            # デフォルト: platform_api/prompts/system/
            api_root = Path(__file__).parent.parent.parent
            self.prompts_dir = api_root / "prompts" / "system"
            self.menu_prompts_dir = api_root / "prompts" / "menu"
        else:
            self.prompts_dir = Path(prompts_dir)
            self.menu_prompts_dir = Path(prompts_dir).parent / "menu"

        globals.logger.debug(
            f"SystemPromptLoader initialized: system={self.prompts_dir}, "
            f"menu={self.menu_prompts_dir}"
        )

    def load_prompt(
        self, service_id: str, user_language: Optional[str] = None
    ) -> str:
        """
        システムプロンプトを読み込む

        Args:
            service_id: サービスID (LLMEditor, AgenticAI)
            user_language: ユーザー言語 (jp, en, None)

        Returns:
            システムプロンプト文字列

        Raises:
            FileNotFoundError: プロンプトファイルが見つからない場合
        """
        # service_id を小文字に正規化
        service_id_lower = service_id.lower()

        # 言語別プロンプトを優先的に読み込み
        if user_language:
            lang_file = self.prompts_dir / f"{service_id_lower}_{user_language}.txt"
            if lang_file.exists():
                globals.logger.debug(
                    f"Loading language-specific prompt: {lang_file}"
                )
                return self._read_file(lang_file)

        # 言語別プロンプトがない場合はベースプロンプトを使用
        base_file = self.prompts_dir / f"{service_id_lower}_base.txt"
        if base_file.exists():
            globals.logger.debug(f"Loading base prompt: {base_file}")
            return self._read_file(base_file)

        # どちらも見つからない場合はエラー
        raise FileNotFoundError(
            f"System prompt not found for service_id={service_id}, "
            f"user_language={user_language}. "
            f"Expected files: {base_file} or {lang_file if user_language else 'N/A'}"
        )

    def _read_file(self, file_path: Path) -> str:
        """
        ファイルを読み込む

        Args:
            file_path: ファイルパス

        Returns:
            ファイル内容
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                globals.logger.debug(
                    f"Loaded prompt from {file_path}: {len(content)} characters"
                )
                return content
        except Exception as e:
            globals.logger.error(f"Failed to read prompt file {file_path}: {e}")
            raise

    def load_menu_prompt(
        self, menu_id: str, user_language: Optional[str] = None
    ) -> Optional[str]:
        """
        メニュー固有の追加システムプロンプトを読み込む

        Args:
            menu_id: メニューID (ITA画面ID)
            user_language: ユーザー言語 (jp, en, None)

        Returns:
            追加プロンプト文字列（ファイルがない場合はNone）
        """
        # menu_id を小文字に正規化
        menu_id_lower = menu_id.lower()

        # 言語別プロンプトを優先的に読み込み
        if user_language:
            lang_file = self.menu_prompts_dir / f"{menu_id_lower}_{user_language}.txt"
            if lang_file.exists():
                globals.logger.debug(
                    f"Loading menu-specific prompt (language): {lang_file}"
                )
                return self._read_file(lang_file)

        # 言語別プロンプトがない場合はベースプロンプトを使用
        base_file = self.menu_prompts_dir / f"{menu_id_lower}_base.txt"
        if base_file.exists():
            globals.logger.debug(f"Loading menu-specific prompt (base): {base_file}")
            return self._read_file(base_file)

        # どちらも見つからない場合はNone（エラーにしない）
        globals.logger.debug(
            f"No menu-specific prompt found for menu_id={menu_id}, "
            f"user_language={user_language}"
        )
        return None

    def get_available_services(self) -> list[str]:
        """
        利用可能なサービスIDのリストを取得

        Returns:
            サービスIDのリスト
        """
        services = set()
        if self.prompts_dir.exists():
            for file_path in self.prompts_dir.glob("*_base.txt"):
                service_id = file_path.stem.replace("_base", "")
                services.add(service_id)

        return sorted(services)


# シングルトンインスタンス
_loader_instance = None


def get_system_prompt_loader() -> SystemPromptLoader:
    """
    SystemPromptLoaderのシングルトンインスタンスを取得

    Returns:
        SystemPromptLoader
    """
    global _loader_instance
    if _loader_instance is None:
        _loader_instance = SystemPromptLoader()
    return _loader_instance


def load_system_prompt(
    service_id: str, user_language: Optional[str] = None
) -> str:
    """
    システムプロンプトを読み込む（ショートカット関数）

    Args:
        service_id: サービスID
        user_language: ユーザー言語

    Returns:
        システムプロンプト文字列
    """
    loader = get_system_prompt_loader()
    return loader.load_prompt(service_id, user_language)


def load_menu_prompt(
    menu_id: str, user_language: Optional[str] = None
) -> Optional[str]:
    """
    メニュー固有の追加プロンプトを読み込む（ショートカット関数）

    Args:
        menu_id: メニューID
        user_language: ユーザー言語

    Returns:
        追加プロンプト文字列（なければNone）
    """
    loader = get_system_prompt_loader()
    return loader.load_menu_prompt(menu_id, user_language)
