"""FastAPI application exposing the VentureMind workflow."""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from venturemind.runtime import build_runtime


class AnalyzeRequest(BaseModel):
    """Incoming request payload."""

    query: str


class AnalyzeResponse(BaseModel):
    """API response payload."""

    report: str


def _build_app() -> FastAPI:
    runtime = build_runtime()

    app = FastAPI(title="VentureMind API", version="0.1.0")

    static_dir = Path(__file__).resolve().parent / "static"
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/", include_in_schema=False)
    async def home() -> FileResponse:
        return FileResponse(static_dir / "index.html")

    @app.post("/analyze", response_model=AnalyzeResponse)
    async def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
        if not payload.query:
            raise HTTPException(status_code=400, detail="Query is required")

        result = runtime.graph.invoke({"query": payload.query})
        report = result.get("report")
        if not report:
            raise HTTPException(status_code=500, detail="Failed to generate report")

        runtime.csv_export.export(
            "latest_report.csv",
            [
                {
                    "query": payload.query,
                    "report": report,
                }
            ],
        )
        return AnalyzeResponse(report=report)

    return app


app = _build_app()
