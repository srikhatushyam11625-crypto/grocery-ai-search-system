import os
import re

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

client = TavilyClient(api_key=api_key)


# -----------------------------------
# Grocery platforms
# -----------------------------------

platforms = {

    "BigBasket": "bigbasket.com",

    "Blinkit": "blinkit.com",

    "Instamart": "swiggy.com/instamart",

    "Zepto": "zepto.com"
}


# -----------------------------------
# Extract numeric price
# -----------------------------------

def extract_price(text):

    patterns = [

        r'₹\s?\d+',

        r'rs\.?\s?\d+',

        r'\d+\s?rupees'
    ]

    text = text.lower()

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:

            value = re.findall(r'\d+', match.group())

            if value:
                return int(value[0])

    return None


# -----------------------------------
# Search one grocery platform
# -----------------------------------

def search_platform(

    platform_name,

    domain,

    product,

    quantity,

    location
):

    query = f"""
    site:{domain}
    buy {quantity} {product}
    in {location}
    price
    """

    response = client.search(

        query=query,

        search_depth="advanced",

        max_results=3
    )

    best_price = None

    best_result = None

    for result in response["results"]:

        content = result.get("content", "")

        title = result.get("title", "")

        url = result.get("url", "")

        price = extract_price(content)

        if price is not None:

            if best_price is None or price < best_price:

                best_price = price

                best_result = {

                    "platform": platform_name,

                    "title": title,

                    "price": price,

                    "url": url,

                    "content": content
                }

    return best_result


# -----------------------------------
# Compare all platforms
# -----------------------------------

def compare_grocery_prices(parsed_query):

    product = parsed_query["product"]

    quantity = parsed_query["quantity"]

    location = parsed_query["location"]

    all_results = []

    for platform, domain in platforms.items():

        result = search_platform(

            platform,

            domain,

            product,

            quantity,

            location
        )

        if result:
            all_results.append(result)

    # Sort lowest price first
    all_results = sorted(

        all_results,

        key=lambda x: x["price"]
    )

    return all_results