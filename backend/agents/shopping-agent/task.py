from crewai import Task
from .agent import shopping_agent


def create_shopping_task(query: str) -> Task:
    return Task(
        description=f"Search Google Shopping for: {query}. Compare products, prices, and ratings to provide the best recommendations.",
        expected_output="A curated list of products with prices, ratings, links, and a recommendation on the best option.",
        agent=shopping_agent,
    )
