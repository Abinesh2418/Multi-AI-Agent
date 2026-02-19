from crewai import Task
from .agent import file_reader_agent


def create_file_reader_task(query: str) -> Task:
    return Task(
        description=f"Read the specified file and answer the following: {query}. Provide a clear summary of the relevant content.",
        expected_output="A structured summary of the file contents relevant to the query, including key data points and observations.",
        agent=file_reader_agent,
    )
