"""Application configuration helpers."""
from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Optional


def _load_env_file(path: str) -> None:
    """Load KEY=VALUE lines into the process environment.

    Values from the file do not override existing environment variables.
    """

    env_path = Path(path)
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key:
            continue
        os.environ.setdefault(key, value)


def _load_local_secrets() -> None:
    """Load optional local env files (useful for development).

    Priority:
    1) .secrets/.env
    2) .env
    """

    _load_env_file(".secrets/.env")
    _load_env_file(".env")


@dataclass
class Settings:
    """Runtime configuration loaded from environment variables."""

    openai_api_key: str = ""
    tavily_api_key: str = ""
    chroma_path: str = "./data/chroma"
    openai_model: str = "gpt-4o-mini"
    max_tasks: int = 5

    @classmethod
    def from_environment(cls) -> "Settings":
        """Load and sanitize settings from the current environment."""

        _load_local_secrets()

        chroma_path = os.getenv("CHROMA_PATH", "./data/chroma")
        Path(chroma_path).mkdir(parents=True, exist_ok=True)

        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            tavily_api_key=os.getenv("TAVILY_API_KEY", ""),
            chroma_path=chroma_path,
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            max_tasks=int(os.getenv("MAX_TASKS", "5")),
        )


settings = Settings.from_environment()
