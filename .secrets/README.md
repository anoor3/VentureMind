Put your API keys in `.secrets/.env` (this file is gitignored).

Example:

```bash
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
CHROMA_PATH=./data/chroma
OPENAI_MODEL=gpt-4o-mini
MAX_TASKS=5
```

To load it into your current shell session:

```bash
set -a
source .secrets/.env
set +a
```

