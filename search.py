import os
import re

from dotenv import load_dotenv
from tavily import TavilyClient

# -----------------------------------
# Load environment variables
# -----------------------------------

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
# Smart contextual price extraction
# -----------------------------------

def extract_price(text):

    text = text.lower()

    text = text.replace(",", "")

    # Ignore misleading contexts
    invalid_keywords = [

        "off",
        "discount",
        "save",
        "delivery",
        "minutes",
        "mins",
        "%",
        "cashback"
    ]

    # Price regex
    pattern = r'₹\s?\d+|rs\.?\s?\d+'

    matches = re.finditer(pattern, text)

    candidate_prices = []

    for match in matches:

        matched_text = match.group()

        numbers = re.findall(r'\d+', matched_text)

        if not numbers:
            continue

        value = int(numbers[0])

        # Realistic 1kg sugar price range
        if value < 35 or value > 80:
            continue

        # Context window
        start = max(0, match.start() - 50)

        end = min(len(text), match.end() + 50)

        context = text[start:end]

        # Reject misleading contexts
        invalid = False

        for word in invalid_keywords:

            if word in context:
                invalid = True
                break

        if invalid:
            continue

        # Strong relevance check
        if "sugar" in context:

            candidate_prices.append(value)

    if candidate_prices:

        return min(candidate_prices)

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
    "{quantity} {product}"
    "{location}"
    price
    """

    # -------------------------------
    # SAFE API CALL WITH ERROR HANDLING
    # -------------------------------

    try:

        response = client.search(

            query=query,

            search_depth="advanced",

            max_results=5
        )

    except Exception as e:

        print(f"Error searching {platform_name}: {e}")

        return None

    # -------------------------------
    # Process results
    # -------------------------------

    best_result = None

    best_price = None

    for result in response["results"]:

        title = result.get("title", "")

        content = result.get("content", "")

        combined_text = f"{title} {content}"

        # Relevance filtering
        if not is_relevant_result(combined_text):
            continue

        # Extract contextual price
        price = extract_price(combined_text)

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