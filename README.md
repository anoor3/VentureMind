# VentureMind

VentureMind is an autonomous multi-agent AI research system that plans, gathers, analyzes, and writes investment-style reports on startups and markets. It demonstrates modern agent-engineering practices such as LangGraph workflows, Retrieval Augmented Generation (RAG), tool use, and an API backend powered by FastAPI.

## Architecture

- **Agents** – Planner, Researcher, Analyst, and Writer agents collaborate in a LangGraph pipeline powered by OpenAI models.
- **Tools** – Tavily web search, BeautifulSoup scraping, a sandboxed Python executor, and CSV export utilities provide the agents with external capabilities.
- **Memory** – A Chroma vector database stores research snippets and enables retrieval for future sessions via a lightweight retriever wrapper.
- **Workflow** – `workflows/research_pipeline.py` wires the agents together so each stage updates a shared state.
- **API** – `api/fastapi_app.py` exposes a `/analyze` endpoint for programmatic access, returning a generated report for any query.
- **CLI** – `main.py` runs the full pipeline locally for experimentation or batch analyses.

## Project Structure

```
venturemind/
  agents/
  tools/
  memory/
  workflows/
  api/
  config/
main.py
requirements.txt
```

See the repository for the complete module layout.

## Setup

1. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set environment variables**
   ```bash
   export OPENAI_API_KEY="sk-..."
   export TAVILY_API_KEY="tvly-..."
   # Optional overrides
   export CHROMA_PATH="./data/chroma"
   export OPENAI_MODEL="gpt-4o-mini"
   export MAX_TASKS=5
   ```

Without API keys the system falls back to deterministic heuristics, which is useful for local testing but lacks live data.

## Usage

### Run the CLI

```bash
python main.py "Find promising AI healthcare startups"
```

This executes the LangGraph pipeline, persists research snippets to Chroma, saves the resulting report to `data/exports/cli_report.csv`, and prints the memo to stdout.

### Start the API

```bash
uvicorn venturemind.api.fastapi_app:app --reload
```

Send a request:

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "Find promising AI healthcare startups"}'
```

Response:

```json
{
  "report": "...generated analysis..."
}
```

## Testing

Run the unit tests with pytest:

```bash
pytest
```

## Extending VentureMind

- Add additional agents (e.g., financial modelers or diligence bots).
- Introduce new tools (Crunchbase, PitchBook, etc.).
- Build scheduling and background workers around the FastAPI service for continuous monitoring.
