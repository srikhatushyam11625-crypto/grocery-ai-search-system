import os
import re

from dotenv import load_dotenv
from tavily import TavilyClient

# Load environment variables
load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

client = TavilyClient(api_key=api_key)

# -----------------------------------
# Supported grocery platforms
# -----------------------------------

platforms = {

    "BigBasket": "bigbasket.com",

    "Blinkit": "blinkit.com",

    "Instamart": "swiggy.com/instamart",

    "Zepto": "zepto.com"
}


# -----------------------------------
# Check whether result is relevant
# -----------------------------------

def is_relevant_result(content):

    content = content.lower()

    # Must contain sugar
    if "sugar" not in content:
        return False

    # Must contain 1kg reference
    if "1 kg" not in content and "1kg" not in content:
        return False

    return True


# -----------------------------------
# Smart price extraction
# -----------------------------------

def extract_price(text):

    patterns = [

        r'₹\s?\d+',

        r'rs\.?\s?\d+',

        r'\d+\s?rupees'
    ]

    text = text.lower()

    detected_prices = []

    for pattern in patterns:

        matches = re.findall(pattern, text)

        for match in matches:

            numbers = re.findall(r'\d+', match)

            if numbers:

                value = int(numbers[0])

                # Realistic 1kg sugar price range
                if 20 <= value <= 100:

                    detected_prices.append(value)

    if detected_prices:

        return min(detected_prices)

    return None


# -----------------------------------
# Search a single grocery platform
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

    best_result = None

    best_price = None

    for result in response["results"]:

        title = result.get("title", "")

        content = result.get("content", "")

        url = result.get("url", "")

        # Relevance filtering
        if not is_relevant_result(content):
            continue

        # Price extraction
        price = extract_price(content)

        if price is not None:

            if best_price is None or price < best_price:

                best_price = price

                best_result = {

                    "platform": platform_name,

                    "price": price
                }

    return best_result


# -----------------------------------
# Compare all grocery platforms
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

    # Sort by lowest price
    all_results = sorted(

        all_results,

        key=lambda x: x["price"]
    )

    return all_results