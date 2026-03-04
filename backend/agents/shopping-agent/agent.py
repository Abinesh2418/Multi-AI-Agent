from crewai import Agent
from backend.config.settings import GROQ_LLM
from .tool import google_shopping_tool

shopping_agent = Agent(
    role="Shopping Research Specialist",
    goal="Search Google Shopping to find products, compare prices, and provide shopping recommendations.",
    backstory=(
        "You are a savvy shopping analyst who uses Google Shopping data to find "
        "the best products and deals. You compare prices, read reviews, and provide "
        "well-informed purchasing recommendations to users."
    ),
    tools=[google_shopping_tool],
    llm=GROQ_LLM,
    verbose=True,
)
