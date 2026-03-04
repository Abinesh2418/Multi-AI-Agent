from crewai import Agent
from backend.config.settings import GROQ_LLM
from .tool import file_read_tool

file_reader_agent = Agent(
    role="File Reader Specialist",
    goal="Read and analyze file contents to extract meaningful information based on user queries.",
    backstory=(
        "You are a meticulous file analyst capable of reading various file formats "
        "and extracting precisely the information the user needs. You provide clear, "
        "well-organized summaries of file contents."
    ),
    tools=[file_read_tool],
    llm=GROQ_LLM,
    verbose=True,
)
