"""Entry-point for running the VentureMind pipeline from the CLI."""
from __future__ import annotations

import argparse

from venturemind.runtime import build_runtime


def main() -> None:
    """Execute the multi-agent workflow for a user supplied query."""

    parser = argparse.ArgumentParser(description="Run the VentureMind research pipeline")
    parser.add_argument(
        "query",
        nargs="?",
        default="Find promising AI healthcare startups",
        help="Research prompt for the agents",
    )
    args = parser.parse_args()

    runtime = build_runtime()
    result = runtime.graph.invoke({"query": args.query})
    report = result.get("report", "No report generated")
    runtime.csv_export.export(
        "cli_report.csv",
        [
            {
                "query": args.query,
                "report": report,
            }
        ],
    )
    print(report)


if __name__ == "__main__":
    main()
