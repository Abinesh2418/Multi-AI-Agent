from crewai import Task
from .agent import google_search_agent


def create_google_search_task(query: str) -> Task:
    return Task(
        description=f"Perform a Google search for: {query}. Analyze the top results and provide a comprehensive answer.",
        expected_output="A well-structured summary of the top Google search results, including links, key facts, and relevant context.",
        agent=google_search_agent,
    )
