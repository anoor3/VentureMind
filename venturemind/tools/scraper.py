"""HTML scraping helpers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import requests
from bs4 import BeautifulSoup


@dataclass
class ScraperTool:
    """Fetch and extract readable text from URLs."""

    user_agent: str = "VentureMindBot/1.0"
    timeout: int = 15

    def scrape(self, url: str) -> Optional[str]:
        """Return plain text content for a URL."""

        if not url:
            return None

        headers = {"User-Agent": self.user_agent}
        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as exc:  # pragma: no cover - network
            return f"Failed to fetch {url}: {exc}"

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
        return "\n".join(paragraphs)
