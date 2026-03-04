from crewai import Agent
from backend.config.settings import GROQ_LLM
from .tool import scrape_tool

scrape_agent = Agent(
    role="Website Scraping Specialist",
    goal="Scrape website content and extract structured, useful information based on user requirements.",
    backstory=(
        "You are a web scraping expert who can extract content from any website. "
        "You understand HTML structure, can navigate complex pages, and return "
        "clean, well-organized data from scraped content."
    ),
    tools=[scrape_tool],
    llm=GROQ_LLM,
    verbose=True,
)
