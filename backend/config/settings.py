import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["SERPAPI_API_KEY"] = SERPAPI_API_KEY
os.environ["SERPER_API_KEY"] = SERPER_API_KEY

OPENAI_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
LANCEDB_DIR = ".lancedb"
