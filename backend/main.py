from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.crew import run_crew, get_available_agents

app = FastAPI(
    title="CrewAI Multi-Agent Platform",
    description="A scalable multi-agent AI system powered by CrewAI",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ExecuteRequest(BaseModel):
    agent_type: str
    query: str


class ExecuteResponse(BaseModel):
    result: str


class AgentsResponse(BaseModel):
    agents: list[str]


@app.get("/agents", response_model=AgentsResponse)
async def list_agents():
    return AgentsResponse(agents=get_available_agents())


@app.post("/execute", response_model=ExecuteResponse)
async def execute(request: ExecuteRequest):
    try:
        result = run_crew(request.agent_type, request.query)
        return ExecuteResponse(result=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "healthy"}
