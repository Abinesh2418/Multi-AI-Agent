from crewai import Task
from .agent import web_search_agent


def create_web_search_task(query: str) -> Task:
    return Task(
        description=f"Search the web for: {query}. Provide a comprehensive and well-structured summary of the findings.",
        expected_output="A detailed summary of the search results with key facts, sources, and relevant insights.",
        agent=web_search_agent,
    )
