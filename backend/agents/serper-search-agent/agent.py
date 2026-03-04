from crewai import Agent
from backend.config.settings import GROQ_LLM
from .tool import serper_search_tool

serper_search_agent = Agent(
    role="Serper Search Specialist",
    goal="Perform fast, real-time web searches using Serper.dev and provide accurate, current results.",
    backstory=(
        "You are an internet research specialist who uses the Serper.dev API for "
        "lightning-fast web searches. You excel at finding the latest information "
        "and presenting it in a clear, organized manner."
    ),
    tools=[serper_search_tool],
    llm=GROQ_LLM,
    verbose=True,
)
