from crewai import Agent
from backend.config.settings import GROQ_MODEL
from .tool import pdf_search_tool

pdf_search_agent = Agent(
    role="PDF Search Specialist",
    goal="Search through PDF documents to find and extract relevant information for user queries.",
    backstory=(
        "You are an expert document analyst specializing in PDF files. You can "
        "quickly navigate through lengthy documents, locate relevant sections, "
        "and extract precise information the user needs."
    ),
    tools=[pdf_search_tool],
    llm=GROQ_MODEL,
    verbose=True,
)
