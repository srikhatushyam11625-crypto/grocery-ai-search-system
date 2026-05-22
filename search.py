import os
import re

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

client = TavilyClient(api_key=api_key)


# -----------------------------
# Extract price from text
# -----------------------------
def extract_price(text):

    price_patterns = [

        r'₹\s?\d+',

        r'rs\.?\s?\d+',

        r'\d+\s?rupees'
    ]

    for pattern in price_patterns:

        match = re.search(
            pattern,
            text.lower()
        )

        if match:

            price_text = match.group()

            number = re.findall(r'\d+', price_text)

            if number:
                return int(number[0])

    return None


# -----------------------------
# Check grocery relevance
# -----------------------------
def is_grocery_result(title, content):

    grocery_keywords = [

        "bigbasket",
        "blinkit",
        "instamart",
        "zepto",
        "dmart",
        "grofers",
        "grocery",
        "sugar"
    ]

    combined = f"{title} {content}".lower()

    for keyword in grocery_keywords:

        if keyword in combined:
            return True

    return False


# -----------------------------
# Main grocery search
# -----------------------------
def search_grocery(parsed_query):

    product = parsed_query["product"]

    quantity = parsed_query["quantity"]

    location = parsed_query["location"]

    search_query = f"""
    buy {quantity} {product} online in {location}
    grocery lowest price
    """

    response = client.search(

        query=search_query,

        search_depth="advanced",

        max_results=10
    )

    cleaned_results = []

    for result in response["results"]:

        title = result.get("title", "")

        content = result.get("content", "")

        url = result.get("url", "")

        # Filter grocery results
        if not is_grocery_result(title, content):
            continue

        # Extract price
        price = extract_price(content)

        cleaned_results.append({

            "title": title,

            "price": price,

            "url": url,

            "content": content
        })

    # Sort by lowest price
    cleaned_results = sorted(

        cleaned_results,

        key=lambda x: x["price"]
        if x["price"] is not None
        else 99999
    )

    return cleaned_results