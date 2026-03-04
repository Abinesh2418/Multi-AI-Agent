# CrewAI Multi-Agent Platform — Project Report

---

## Table of Contents

1. [Overview](#overview)
2. [Project Description](#project-description)
3. [Features Implemented](#features-implemented)
4. [Output Screenshots](#output-screenshots)
5. [Conclusion](#conclusion)
6. [Future Plan](#future-plan)

---

## Overview

The **CrewAI Multi-Agent Platform** is a production-ready, full-stack web application that brings together multiple specialized AI agents under a single, unified interface. Built with **CrewAI** on the backend and **React + TypeScript** on the frontend, the platform allows users to interact with 7 distinct AI agents — each equipped with a dedicated tool — through a modern chat-style UI. The system is designed to be modular and extensible, enabling new agents to be added with zero changes to the core application code.

**Tech Stack:**

| Layer | Technology |
|---|---|
| Backend | Python 3, FastAPI, CrewAI, crewai-tools |
| Frontend | React 19, TypeScript, Vite 7 |
| LLM | Groq Llama 3.3 70B Versatile |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 (local) |
| Vector Database | LanceDB |
| Search APIs | SerpAPI, Serper.dev |

---

## Project Description

The platform solves the problem of interacting with multiple AI tool-agents through a single conversational interface. Instead of writing separate scripts or notebooks for each task (web search, PDF analysis, CSV querying, web scraping, etc.), users simply select an agent from the sidebar and type their query in natural language.

### Architecture

The system follows a clean **three-layer architecture**:

```
┌──────────────────────────────────────────────────────────┐
│                    React Frontend                        │
│           (Chat UI · Agent Selector · Vite)              │
└────────────────────────┬─────────────────────────────────┘
                         │  HTTP (REST API)
┌────────────────────────▼─────────────────────────────────┐
│                  FastAPI Backend                          │
│         POST /execute  ·  GET /agents  ·  GET /health    │
└────────────────────────┬─────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────┐
│               CrewAI Orchestrator (crew.py)               │
│     Dynamic agent loading  ·  Crew kickoff  ·  Process    │
└──┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┘
   │      │      │      │      │      │      │      │
 Agent  Agent  Agent  Agent  Agent  Agent  Agent  Agent ...
  +Tool  +Tool  +Tool  +Tool  +Tool  +Tool  +Tool  +Tool
```

**Key design decisions:**

- **Dynamic agent discovery** — agents are loaded at runtime via `importlib`, so adding a new agent only requires creating a new folder under `backend/agents/` and registering it in `crew.py`.
- **Separation of concerns** — each agent lives in its own directory with three files: `tool.py` (tool setup), `agent.py` (agent definition), and `task.py` (task factory).
- **RESTful API** — the frontend communicates with the backend through a clean REST API (`/execute`, `/agents`, `/health`), making it easy to integrate other clients in the future.

### Project Structure

```
crew-ai-platform/
├── backend/
│   ├── main.py                  # FastAPI app & endpoints
│   ├── crew.py                  # Crew orchestrator & dynamic loader
│   ├── config/
│   │   └── settings.py          # Environment variables & model config
│   └── agents/
│       ├── file-reader-agent/   # FileReadTool
│       ├── file-writer-agent/   # FileWriterTool
│       ├── csv-rag-agent/       # CSVSearchTool + LanceDB (RAG)
│       ├── scrape-agent/        # ScrapeWebsiteTool
│       ├── google-search-agent/ # SerpApiGoogleSearchTool
│       ├── shopping-agent/      # SerpApiGoogleShoppingTool
│       └── serper-search-agent/ # SerperDevTool
├── frontend/
│   ├── src/
│   │   ├── App.tsx              # Main chat component
│   │   ├── App.css              # Styles
│   │   └── main.tsx             # React entry point
│   ├── package.json
│   └── vite.config.ts
├── requirements.txt
├── .env.template
└── README.md
```

---

## Features Implemented

### 1. Seven Specialized AI Agents

Each agent is purpose-built with a dedicated CrewAI tool:

| # | Agent | Tool | Capability |
|---|---|---|---|
| 1 | **File Reader Agent** | FileReadTool | Reads and analyzes local files |
| 2 | **File Writer Agent** | FileWriterTool | Generates and writes content to files |
| 3 | **CSV RAG Agent** | CSVSearchTool + LanceDB | Performs RAG-based semantic search over CSV data |
| 4 | **Scrape Agent** | ScrapeWebsiteTool | Scrapes and extracts content from web pages |
| 5 | **Google Search Agent** | SerpApiGoogleSearchTool | Performs Google searches via SerpAPI |
| 6 | **Shopping Agent** | SerpApiGoogleShoppingTool | Searches Google Shopping for product listings |
| 7 | **Serper Search Agent** | SerperDevTool | Performs web searches via Serper.dev API |

### 2. Modern Chat-Based UI

- Responsive chat interface built with **React 19** and **TypeScript**
- Sidebar-based agent selector with color-coded agent indicators
- Real-time typing indicator ("Agent is thinking...")
- Quick-start suggestion chips for common queries
- Keyboard shortcuts: `Enter` to send, `Shift+Enter` for new line
- Mobile-friendly layout with hamburger menu and sidebar overlay
- New Chat button to clear conversation history

### 3. FastAPI REST Backend

- `POST /execute` — Accepts an agent type and query, runs the CrewAI crew, and returns the result
- `GET /agents` — Returns the list of all available agents
- `GET /health` — Health check endpoint for monitoring
- Full **CORS** support for cross-origin frontend requests
- Structured request/response models using **Pydantic**

### 4. Dynamic Agent Loading System

- Agents are dynamically imported at runtime using Python's `importlib`
- Adding a new agent requires only:
  1. Creating a new directory under `backend/agents/`
  2. Adding `__init__.py`, `tool.py`, `agent.py`, and `task.py`
  3. Registering the agent in `AGENT_CONFIGS` in `crew.py`
- No modifications to `main.py` or the frontend are needed

### 5. RAG Pipeline (CSV RAG Agent)

- Uses **LanceDB** as the vector database for embedding storage
- Leverages **sentence-transformers/all-MiniLM-L6-v2** for local embedding generation (no API key needed)
- Enables semantic search over CSV data for natural-language querying

### 6. Environment & Configuration Management

- Centralized settings in `backend/config/settings.py`
- API keys managed through `.env` file (template provided as `.env.template`)
- Configurable LLM model (`groq/llama-3.3-70b-versatile`) and embedding model

---

## Output Screenshots

### Screenshot 1 — Chat Interface (Home Screen)

<!-- Replace the path below with the actual screenshot -->

![Home Screen](screenshots/screenshot_1.png)

<br><br><br><br><br><br><br><br><br><br>

*Figure 1: The main chat interface showing the agent sidebar, suggestion chips, and the chat area.*

---

### Screenshot 2 — Agent Execution & Response

<!-- Replace the path below with the actual screenshot -->

![Agent Response](screenshots/screenshot_2.png)

<br><br><br><br><br><br><br><br><br><br>

*Figure 2: An agent processing a user query and returning the result in the chat window.*

---

### Screenshot 3 — Agent Sidebar Selection

<!-- Replace the path below with the actual screenshot -->

![Agent Sidebar](screenshots/screenshot_3.png)

<br><br><br><br><br><br><br><br><br><br>

*Figure 3: The sidebar showing all 7 available agents with their associated tools.*

---

## Conclusion

The **CrewAI Multi-Agent Platform** successfully demonstrates a scalable, modular approach to building multi-agent AI systems. By combining the orchestration capabilities of CrewAI with a clean FastAPI backend and a modern React frontend, the platform delivers a seamless conversational interface for interacting with specialized AI agents.

Key takeaways from the project:

- **Modular agent architecture** makes the system easy to extend — new agents can be added without touching the core codebase.
- **CrewAI's orchestration** simplifies the complexity of managing multiple LLM-powered agents, each with their own tools and tasks.
- **The chat-based UI** provides an intuitive, familiar experience for end users, lowering the barrier to interacting with advanced AI capabilities.
- **RAG integration** with LanceDB demonstrates how vector databases can be used alongside LLMs for semantic search over structured data like CSVs.
- **REST API design** ensures the backend can serve not only the web frontend but also future integrations such as mobile apps or CLI tools.

The project showcases the practical application of multi-agent systems, tool-augmented LLMs, and full-stack development in building intelligent, production-grade AI platforms.

---

## Future Plan

1. **Streaming Responses** — Implement Server-Sent Events (SSE) or WebSocket support so that agent responses stream to the UI in real-time instead of waiting for full completion.

2. **Multi-Agent Collaboration** — Enable users to chain multiple agents together in a single workflow (e.g., scrape a website → analyze with CSV RAG → generate a report with the file writer).

3. **Conversation Memory** — Add persistent chat history using a database (e.g., SQLite or PostgreSQL) so users can revisit and continue past conversations.

4. **User Authentication** — Integrate authentication (OAuth / JWT) to support multiple users with isolated sessions and API key management.

5. **File Upload Support** — Allow users to upload files (PDFs, CSVs, text files) directly through the UI for the file-based agents to process.

6. **Agent Performance Dashboard** — Build an analytics page showing agent usage statistics, average response times, and token consumption.

7. **Deployment & CI/CD** — Containerize the application with Docker, set up a CI/CD pipeline, and deploy to a cloud platform (AWS / GCP / Azure) for production use.

8. **Additional Agents** — Expand the agent library with new capabilities such as image analysis, code generation, database querying, and email automation.

---
