from crewai import Task
from .agent import serper_search_agent


def create_serper_search_task(query: str) -> Task:
    return Task(
        description=f"Search the web using Serper.dev for: {query}. Provide a detailed summary of the most relevant results.",
        expected_output="A comprehensive summary of search results with key findings, relevant links, and synthesized insights.",
        agent=serper_search_agent,
    )
