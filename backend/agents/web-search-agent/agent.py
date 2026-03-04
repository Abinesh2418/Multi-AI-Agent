from crewai import Agent
from backend.config.settings import GROQ_MODEL
from .tool import web_search_tool

web_search_agent = Agent(
    role="Web Search Specialist",
    goal="Search websites thoroughly and extract relevant information based on user queries.",
    backstory=(
        "You are an expert web researcher with deep experience in finding "
        "accurate and relevant information from websites. You excel at "
        "understanding search queries and returning concise, useful results."
    ),
    tools=[web_search_tool],
    llm=GROQ_MODEL,
    verbose=True,
)
