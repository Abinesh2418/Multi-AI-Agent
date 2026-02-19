from crewai import Agent
from .tool import google_search_tool

google_search_agent = Agent(
    role="Google Search Specialist",
    goal="Perform Google searches via SerpAPI and deliver accurate, up-to-date search results for user queries.",
    backstory=(
        "You are a seasoned research analyst with expertise in leveraging Google "
        "search to find the most relevant and reliable information. You use SerpAPI "
        "to access real-time Google search results and synthesize them into actionable insights."
    ),
    tools=[google_search_tool],
    verbose=True,
)
