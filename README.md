# CrewAI Multi-Agent Platform

A production-ready, scalable multi-agent AI system built with **CrewAI**, **FastAPI**, and **React + TypeScript**.

## Architecture

The platform provides 7 specialized AI agents, each equipped with a dedicated tool:

| Agent | Tool | Purpose |
|---|---|---|
| `file-reader-agent` | FileReadTool | Read and analyze files |
| `file-writer-agent` | FileWriterTool | Generate and write files |
| `csv-rag-agent` | CSVSearchTool (LanceDB) | RAG search over CSV data |
| `scrape-agent` | ScrapeWebsiteTool | Scrape website content |
| `google-search-agent` | SerpApiGoogleSearchTool | Google search via SerpAPI |
| `shopping-agent` | SerpApiGoogleShoppingTool | Google Shopping via SerpAPI |
| `serper-search-agent` | SerperDevTool | Web search via Serper.dev |

## Project Structure

```
crew-ai-platform/
├── backend/
│   ├── main.py              # FastAPI entrypoint
│   ├── crew.py              # Crew orchestrator
│   ├── config/
│   │   └── settings.py      # Environment & config
│   └── agents/
│       ├── file-reader-agent/
│       │   ├── tool.py
│       │   ├── agent.py
│       │   └── task.py
│       ├── file-writer-agent/
│       ├── csv-rag-agent/
│       ├── scrape-agent/
│       ├── google-search-agent/
│       ├── shopping-agent/
│       └── serper-search-agent/
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── requirements.txt
├── .env.template
└── README.md
```

## Setup

### 1. Clone and Configure Environment

```bash
cp .env.template .env
```

Edit `.env` and fill in your API keys:

```
GROQ_API_KEY=gsk_...
SERPAPI_API_KEY=...
SERPER_API_KEY=...
```

### 2. Backend Setup

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Start the Backend

Run from the project root (`crew-ai-platform/`):

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at `http://localhost:5173` and proxies API calls to the backend.

## API

### `POST /execute`

Execute a query with a specific agent.

**Request:**

```json
{
  "agent_type": "scrape-agent",
  "query": "latest AI trends"
}
```

**Response:**

```json
{
  "result": "..."
}
```

### `GET /agents`

List all available agents.

### `GET /health`

Health check endpoint.

## Adding a New Agent

1. Create a new directory under `backend/agents/<agent-name>/`
2. Add `__init__.py`, `tool.py`, `agent.py`, and `task.py`
3. Register the agent in `backend/crew.py` → `AGENT_CONFIGS`

No changes to `main.py` or the frontend are needed — the system dynamically discovers agents.

## Tech Stack

- **Backend:** Python, FastAPI, CrewAI, crewai-tools, LanceDB
- **Frontend:** React, TypeScript, Vite
- **LLM:** Groq Llama 3.3 70B Versatile
- **Embeddings:** sentence-transformers/all-MiniLM-L6-v2 (local)
- **Vector DB:** LanceDB
