from crewai import Agent
from backend.config.settings import GROQ_LLM
from .tool import file_writer_tool

file_writer_agent = Agent(
    role="File Writer Specialist",
    goal="Generate and write well-structured content to files based on user instructions.",
    backstory=(
        "You are a skilled content writer and file management expert. You create "
        "high-quality, well-formatted content and save it to files efficiently. "
        "You understand various file formats and write accordingly."
    ),
    tools=[file_writer_tool],
    llm=GROQ_LLM,
    verbose=True,
)
