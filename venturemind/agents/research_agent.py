"""Research agent that orchestrates tool usage."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any

from venturemind.tools.web_search import WebSearchTool
from venturemind.tools.scraper import ScraperTool
from venturemind.tools.python_executor import PythonExecutor
from venturemind.memory.vector_store import VectorStore
from venturemind.memory.retriever import Retriever


@dataclass
class ResearchAgent:
    """Gather data using search, scraping, and calculations."""

    search_tool: WebSearchTool
    scraper_tool: ScraperTool
    python_executor: PythonExecutor
    vector_store: VectorStore
    retriever: Retriever

    def gather(self, query: str, tasks: List[str]) -> List[Dict[str, Any]]:
        """Collect structured findings for the downstream agents."""

        findings: List[Dict[str, Any]] = []
        for doc in self.retriever.retrieve(query):
            metadata = doc.get("metadata", {})
            findings.append(
                {
                    "source": metadata.get("source", "memory"),
                    "summary": doc.get("content", ""),
                    "score": doc.get("score"),
                }
            )

        for task in tasks:
            search_results = self.search_tool.search(f"{query}: {task}")
            for result in search_results:
                url = result.get("url")
                content = result.get("content") or self.scraper_tool.scrape(url)
                summary = content[:1000] if content else ""
                finding = {
                    "task": task,
                    "title": result.get("title") or url,
                    "url": url,
                    "summary": summary,
                }
                findings.append(finding)
                self.vector_store.add_documents(
                    [summary],
                    [
                        {
                            "task": task,
                            "source": url or result.get("title", "search"),
                        }
                    ],
                )

        metrics = self.python_executor.run(
            "result = {'total_findings': len(data)}",
            {"data": findings},
        )
        findings.append(
            {
                "source": "python_executor",
                "summary": f"Total findings gathered: {metrics.get('result')}",
            }
        )

        return findings
