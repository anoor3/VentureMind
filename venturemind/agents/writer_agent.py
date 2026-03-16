"""Writer agent responsible for producing the final report."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - optional dependency
    OpenAI = None  # type: ignore


@dataclass
class WriterAgent:
    """Craft a narrative investment memo summarizing outcomes."""

    client: OpenAI | None
    model: str

    def write(
        self,
        query: str,
        tasks: List[str],
        insights: str,
        findings_count: int,
    ) -> str:
        """Return a polished investor-style report."""

        if not self.client:
            return self._fallback_report(query, tasks, insights, findings_count)

        response = self.client.chat.completions.create(  # type: ignore[union-attr]
            model=self.model,
            temperature=0.4,
            messages=[
                {
                    "role": "system",
                    "content": "You are an elite investment memo writer.",
                },
                {
                    "role": "user",
                    "content": (
                        "Compose a report for the research query \"{query}\"\n"
                        f"Tasks: {tasks}\nInsights: {insights}\n"
                        f"Total findings: {findings_count}"
                    ),
                },
            ],
        )
        return response.choices[0].message.content or ""  # type: ignore[index]

    def _fallback_report(
        self, query: str, tasks: List[str], insights: str, findings_count: int
    ) -> str:
        tasks_bullets = "\n".join(f"- {task}" for task in tasks)
        return (
            f"VentureMind Report\n===================\nQuery: {query}\n\n"
            f"Tasks executed:\n{tasks_bullets}\n\nInsights:\n{insights}\n\n"
            f"Evidence references: {findings_count} items"
        )
