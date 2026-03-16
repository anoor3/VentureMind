"""Runtime factories for building VentureMind components."""
from __future__ import annotations

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None  # type: ignore

from venturemind.config.settings import settings
from venturemind.tools.web_search import WebSearchTool
from venturemind.tools.scraper import ScraperTool
from venturemind.tools.python_executor import PythonExecutor
from venturemind.tools.csv_export import CSVExportTool
from venturemind.memory.vector_store import VectorStore
from venturemind.memory.retriever import Retriever
from venturemind.agents.planner_agent import PlannerAgent
from venturemind.agents.research_agent import ResearchAgent
from venturemind.agents.analyst_agent import AnalystAgent
from venturemind.agents.writer_agent import WriterAgent
from venturemind.workflows.research_pipeline import build_research_graph


class Runtime:
    """Container for key VentureMind services."""

    def __init__(self) -> None:
        self.client = (
            OpenAI(api_key=settings.openai_api_key)
            if settings.openai_api_key and OpenAI
            else None
        )
        self.vector_store = VectorStore(settings.chroma_path)
        self.retriever = Retriever(self.vector_store)
        self.search_tool = WebSearchTool(api_key=settings.tavily_api_key)
        self.scraper_tool = ScraperTool()
        self.python_executor = PythonExecutor()
        self.csv_export = CSVExportTool()
        self.planner = PlannerAgent(
            client=self.client,
            model=settings.openai_model,
            max_tasks=settings.max_tasks,
        )
        self.researcher = ResearchAgent(
            search_tool=self.search_tool,
            scraper_tool=self.scraper_tool,
            python_executor=self.python_executor,
            vector_store=self.vector_store,
            retriever=self.retriever,
        )
        self.analyst = AnalystAgent(client=self.client, model=settings.openai_model)
        self.writer = WriterAgent(client=self.client, model=settings.openai_model)
        self.graph = build_research_graph(
            self.planner, self.researcher, self.analyst, self.writer
        )


def build_runtime() -> Runtime:
    """Instantiate and return the runtime container."""

    return Runtime()
