import os
from pathlib import Path
from dotenv import load_dotenv
from crewai import LLM

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=str(env_path), override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")

os.environ["GROQ_API_KEY"] = GROQ_API_KEY
os.environ["SERPAPI_API_KEY"] = SERPAPI_API_KEY
os.environ["SERPER_API_KEY"] = SERPER_API_KEY

GROQ_LLM = LLM(
    model="llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LANCEDB_DIR = ".lancedb"
