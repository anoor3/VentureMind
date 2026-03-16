"""Application configuration helpers."""
from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


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
