from crewai import Task
from .agent import scrape_agent


def create_scrape_task(query: str) -> Task:
    return Task(
        description=f"Scrape the specified website and extract information related to: {query}. Organize the scraped data clearly.",
        expected_output="Structured, clean content extracted from the website with relevant information highlighted and organized.",
        agent=scrape_agent,
    )
