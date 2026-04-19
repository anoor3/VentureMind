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

### 0) Prerequisites

- Python 3.9+
- An OpenAI API key (`OPENAI_API_KEY`) for full planner/analyst/writer quality
- A Tavily API key (`TAVILY_API_KEY`) for live web search

### 1) Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3) Add API keys (safe local dev)

This repo supports a local secrets file that is gitignored.

1) Create `.secrets/.env`:

```bash
mkdir -p .secrets
cat > .secrets/.env <<'EOF'
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...

# Optional overrides
CHROMA_PATH=./data/chroma
OPENAI_MODEL=gpt-4o-mini
MAX_TASKS=5
EOF
```

2) Run the app normally — it auto-loads `.secrets/.env` on startup.

If API keys are missing (or OpenAI quota is unavailable), VentureMind falls back to deterministic heuristics for some steps.

## Usage

### Quickstart (copy/paste)

```bash
cd /Users/abdullahnoor/Documents/VentureMind/VentureMind
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn venturemind.api.fastapi_app:app --reload
```

Open `http://127.0.0.1:8000/`.

### Option A: Web UI (recommended)

Start the server:

```bash
source .venv/bin/activate
uvicorn venturemind.api.fastapi_app:app --reload
```

Open:

- Web UI: `http://127.0.0.1:8000/`
- API docs (Swagger): `http://127.0.0.1:8000/docs`
- API docs (ReDoc): `http://127.0.0.1:8000/redoc`

### Option B: CLI

```bash
source .venv/bin/activate
python3 main.py "Find promising AI healthcare startups"
```

This executes the LangGraph pipeline, persists research snippets to Chroma, saves the resulting report to `data/exports/cli_report.csv`, and prints the memo to stdout.

### Option C: API (programmatic)

```bash
source .venv/bin/activate
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

## Troubleshooting

### `ModuleNotFoundError` (e.g. `tavily`)

You’re not running inside the virtualenv.

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python3 main.py "test"
```

### OpenAI `429 insufficient_quota`

Your API key is valid, but billing/quota isn’t enabled for that API project/org. Enable API billing in the OpenAI dashboard, then retry.

## Extending VentureMind

- Add additional agents (e.g., financial modelers or diligence bots).
- Introduce new tools (Crunchbase, PitchBook, etc.).
- Build scheduling and background workers around the FastAPI service for continuous monitoring.
