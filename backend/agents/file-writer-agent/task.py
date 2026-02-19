from crewai import Task
from .agent import file_writer_agent


def create_file_writer_task(query: str) -> Task:
    return Task(
        description=f"Generate content and write it to a file as instructed: {query}. Ensure proper formatting and structure.",
        expected_output="Confirmation of file creation with a summary of the content written and the file path.",
        agent=file_writer_agent,
    )
