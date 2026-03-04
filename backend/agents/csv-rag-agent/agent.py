from crewai import Agent
from backend.config.settings import GROQ_LLM
from .tool import csv_search_tool

csv_rag_agent = Agent(
    role="CSV Data Analyst (RAG)",
    goal="Perform RAG-based search over CSV data to answer user queries with precise, data-driven insights.",
    backstory=(
        "You are a data analyst who specializes in CSV datasets. Using advanced "
        "retrieval-augmented generation techniques with LanceDB, you can search "
        "through large CSV files and return accurate, contextual answers based "
        "on the underlying data."
    ),
    tools=[csv_search_tool],
    llm=GROQ_LLM,
    verbose=True,
)
