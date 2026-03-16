"""LangGraph workflow orchestrating the VentureMind agents."""
from __future__ import annotations

from typing import TypedDict, List, Dict, Any

from langgraph.graph import StateGraph, END

from venturemind.agents.planner_agent import PlannerAgent
from venturemind.agents.research_agent import ResearchAgent
from venturemind.agents.analyst_agent import AnalystAgent
from venturemind.agents.writer_agent import WriterAgent


class ResearchState(TypedDict, total=False):
    """Shared graph state passed between nodes."""

    query: str
    tasks: List[str]
    findings: List[Dict[str, Any]]
    insights: str
    report: str


def build_research_graph(
    planner: PlannerAgent,
    researcher: ResearchAgent,
    analyst: AnalystAgent,
    writer: WriterAgent,
):
    """Create a LangGraph pipeline for the VentureMind workflow."""

    graph = StateGraph(ResearchState)

    def plan_node(state: ResearchState) -> ResearchState:
        tasks = planner.plan(state["query"])
        return {"tasks": tasks}

    def research_node(state: ResearchState) -> ResearchState:
        findings = researcher.gather(state["query"], state.get("tasks", []))
        return {"findings": findings}

    def analyze_node(state: ResearchState) -> ResearchState:
        insights = analyst.analyze(state["query"], state.get("findings", []))
        return {"insights": insights}

    def write_node(state: ResearchState) -> ResearchState:
        tasks = state.get("tasks", [])
        insights = state.get("insights", "")
        findings_count = len(state.get("findings", []))
        report = writer.write(state["query"], tasks, insights, findings_count)
        return {"report": report}

    graph.add_node("plan", plan_node)
    graph.add_node("research", research_node)
    graph.add_node("analyze", analyze_node)
    graph.add_node("write", write_node)

    graph.set_entry_point("plan")
    graph.add_edge("plan", "research")
    graph.add_edge("research", "analyze")
    graph.add_edge("analyze", "write")
    graph.add_edge("write", END)

    return graph.compile()
