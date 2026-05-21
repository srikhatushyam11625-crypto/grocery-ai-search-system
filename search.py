import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

client = TavilyClient(api_key=api_key)


def search_grocery(parsed_query):

    product = parsed_query["product"]
    quantity = parsed_query["quantity"]
    location = parsed_query["location"]

    # Build live search query
    search_query = f"""
    buy {quantity} {product} online in {location}
    lowest price grocery delivery
    """

    response = client.search(
        query=search_query,
        search_depth="advanced",
        max_results=5
    )

    return response