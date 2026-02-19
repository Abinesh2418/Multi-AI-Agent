from crewai import Task
from .agent import pdf_search_agent


def create_pdf_search_task(query: str) -> Task:
    return Task(
        description=f"Search through the provided PDF document(s) for: {query}. Extract and summarize the relevant information found.",
        expected_output="A detailed extraction of relevant information from the PDF, including page references and key findings.",
        agent=pdf_search_agent,
    )
