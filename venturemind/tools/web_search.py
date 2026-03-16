"""Tavily-powered web search tool."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any

from tavily import TavilyClient


@dataclass
class WebSearchTool:
    """Lightweight wrapper around the Tavily API."""

    api_key: str | None = None
    max_results: int = 5

    def __post_init__(self) -> None:
        self._client = TavilyClient(api_key=self.api_key) if self.api_key else None

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search the web and return structured Tavily results."""

        if not query:
            return []

        if not self._client:
            return [
                {
                    "title": "Tavily key missing",
                    "url": "",
                    "content": "Set TAVILY_API_KEY to enable live search.",
                }
            ]

        response = self._client.search(query=query, max_results=self.max_results)
        return response.get("results", [])
