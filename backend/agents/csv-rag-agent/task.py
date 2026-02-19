from crewai import Task
from .agent import csv_rag_agent


def create_csv_rag_task(query: str) -> Task:
    return Task(
        description=f"Search the CSV dataset using RAG to answer: {query}. Provide data-backed insights and specific values where possible.",
        expected_output="A data-driven answer with specific values, statistics, or records from the CSV that address the query.",
        agent=csv_rag_agent,
    )
