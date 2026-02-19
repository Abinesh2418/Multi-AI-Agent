import os
import csv
from pathlib import Path
from typing import Type

import lancedb
import openai
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

LANCEDB_DIR = str(Path(__file__).resolve().parents[2] / ".lancedb")
TABLE_NAME = "csv_rows"
EMBEDDING_MODEL = "text-embedding-3-small"


def _get_embedding(text: str) -> list[float]:
    client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    resp = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return resp.data[0].embedding


def _ingest_csv(csv_path: str) -> lancedb.table.Table:
    """Read a CSV, embed every row, and upsert into a LanceDB table."""
    db = lancedb.connect(LANCEDB_DIR)

    rows: list[dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = " | ".join(f"{k}: {v}" for k, v in row.items())
            rows.append({"text": text, "vector": _get_embedding(text)})

    if TABLE_NAME in db.table_names():
        db.drop_table(TABLE_NAME)

    return db.create_table(TABLE_NAME, rows)


def _search(table: lancedb.table.Table, query: str, top_k: int = 10) -> str:
    query_vec = _get_embedding(query)
    results = table.search(query_vec).limit(top_k).to_pandas()
    if results.empty:
        return "No matching rows found."
    return "\n\n".join(results["text"].tolist())


class CSVSearchInput(BaseModel):
    query: str = Field(..., description="The search query to find relevant rows in the CSV.")
    csv_path: str = Field(
        default="data/employees.csv",
        description="Path to the CSV file relative to the project root.",
    )


class CSVSearchToolLanceDB(BaseTool):
    name: str = "csv_search_tool"
    description: str = (
        "Searches a CSV file using RAG with LanceDB vector search. "
        "Provide a natural-language query and an optional csv_path. "
        "Returns the most relevant rows from the CSV."
    )
    args_schema: Type[BaseModel] = CSVSearchInput

    def _run(self, query: str, csv_path: str = "data/employees.csv") -> str:
        project_root = Path(__file__).resolve().parents[3]
        full_path = project_root / csv_path

        if not full_path.exists():
            return f"CSV file not found at {full_path}"

        table = _ingest_csv(str(full_path))
        return _search(table, query)


csv_search_tool = CSVSearchToolLanceDB()
