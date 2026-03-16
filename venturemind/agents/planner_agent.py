"""Planner agent responsible for decomposing user goals."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

try:  # Optional dependency for environments without OpenAI credentials.
    from openai import OpenAI
except ImportError:  # pragma: no cover - import guard
    OpenAI = None  # type: ignore


@dataclass
class PlannerAgent:
    """Use an LLM to break down a research problem into tasks."""

    client: OpenAI | None
    model: str
    max_tasks: int = 5

    def plan(self, query: str) -> List[str]:
        """Return an ordered list of actionable research tasks."""

        if not query:
            return []

        if not self.client:
            return self._fallback_plan(query)

        response = self.client.chat.completions.create(  # type: ignore[union-attr]
            model=self.model,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a meticulous research project planner. "
                        "Return a concise numbered list of tasks."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Plan research to answer: {query}",
                },
            ],
        )

        content = response.choices[0].message.content or ""  # type: ignore[index]
        tasks = self._parse_tasks(content)
        return tasks[: self.max_tasks]

    def _fallback_plan(self, query: str) -> List[str]:
        """Simple deterministic planner used when the LLM is unavailable."""

        blueprint = [
            "Clarify success metrics and investor expectations",
            "Map leading startups and competitors",
            "Summarize market size, tailwinds, and risks",
            "Highlight notable funding rounds and investors",
            "Synthesize key takeaways for the thesis",
        ]
        return blueprint[: self.max_tasks]

    def _parse_tasks(self, content: str) -> List[str]:
        lines = [line.strip(" -\t") for line in content.splitlines() if line.strip()]
        tasks: List[str] = []
        for line in lines:
            if "." in line[:4]:
                _, remainder = line.split(".", 1)
                tasks.append(remainder.strip())
            else:
                tasks.append(line)
        return [task for task in tasks if task]
