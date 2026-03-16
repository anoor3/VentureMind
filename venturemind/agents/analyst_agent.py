"""Analyst agent that converts raw findings into insights."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - optional dependency
    OpenAI = None  # type: ignore


@dataclass
class AnalystAgent:
    """Summarize data and extract opportunities, risks, and trends."""

    client: OpenAI | None
    model: str

    def analyze(self, query: str, findings: List[Dict[str, Any]]) -> str:
        """Return a concise analysis of the gathered findings."""

        if not findings:
            return "No evidence collected."

        bullet_points = []
        for finding in findings:
            summary = finding.get("summary") or ""
            if summary:
                bullet_points.append(summary)
            if len(bullet_points) >= 10:
                break
        context = "\n".join(bullet_points)

        if not self.client:
            return self._fallback_analysis(query, context)

        response = self.client.chat.completions.create(  # type: ignore[union-attr]
            model=self.model,
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": "You are an investment analyst who explains insights clearly.",
                },
                {
                    "role": "user",
                    "content": (
                        "Analyze the following findings and synthesize insights for "
                        f"the research query '{query}'.\n\nFindings:\n{context}"
                    ),
                },
            ],
        )
        return response.choices[0].message.content or ""  # type: ignore[index]

    def _fallback_analysis(self, query: str, context: str) -> str:
        """Provide a deterministic summary without an LLM."""

        highlighted = context[:500]
        return (
            f"Insights for '{query}':\n- Evidence excerpts: {highlighted}\n"
            "- Further validation required before investing."
        )
