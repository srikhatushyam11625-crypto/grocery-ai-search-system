# search.py

# search.py

# -----------------------------------
# Main Search Function
# -----------------------------------
# search.py

import re
from tavily import TavilyClient

# -----------------------------------
# Tavily API Client
# -----------------------------------
client = TavilyClient(
    api_key="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"
)

# -----------------------------------
# Extract Price
# -----------------------------------
def extract_price(text):

    if not text:
        return None

    text = text.replace(",", "")

    patterns = [
        r'₹\s?(\d+(?:\.\d{1,2})?)',
        r'rs\.?\s?(\d+(?:\.\d{1,2})?)',
        r'inr\s?(\d+(?:\.\d{1,2})?)'
    ]

    prices = []

    for pattern in patterns:

        matches = re.findall(pattern, text, re.IGNORECASE)

        for match in matches:

            try:

                price = float(match)

                # realistic grocery price range
                if 5 <= price <= 5000:
                    prices.append(price)

            except:
                pass

    if not prices:
        return None

    return min(prices)


# -----------------------------------
# Detect Platform
# -----------------------------------
def detect_platform(url):

    url = url.lower()

    if "blinkit" in url:
        return "Blinkit"

    elif "zepto" in url:
        return "Zepto"

    elif "bigbasket" in url:
        return "BigBasket"

    elif "swiggy" in url or "instamart" in url:
        return "Instamart"

    elif "jiomart" in url:
        return "JioMart"

    return "Other"


# -----------------------------------
# Clean Product Title
# -----------------------------------
def clean_title(title):

    if not title:
        return ""

    title = re.sub(r'\s+', ' ', title)

    return title.strip()


# -----------------------------------
# Main Grocery Search Function
# -----------------------------------
def search_grocery_prices(product, quantity="1 kg", location="Delhi"):

    # -----------------------------------
    # Build Search Query
    # -----------------------------------
    query = (
        f"buy {quantity} {product} online in {location} "
        f"price Blinkit Zepto BigBasket Instamart JioMart"
    )

    print("\n===================================")
    print("SEARCH QUERY:", query)
    print("===================================")

    try:

        # -----------------------------------
        # Tavily Search
        # -----------------------------------
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=20
        )

        results = response.get("results", [])

        print("\nRAW RESULTS COUNT:", len(results))

        products = []

        # -----------------------------------
        # Allowed Grocery Domains
        # -----------------------------------
        allowed_domains = [
            "blinkit",
            "zepto",
            "bigbasket",
            "swiggy",
            "instamart",
            "jiomart"
        ]

        # -----------------------------------
        # Bad / Noisy Domains
        # -----------------------------------
        bad_domains = [
            "linkedin",
            "telegram",
            "youtube",
            "facebook",
            "instagram",
            "play.google"
        ]

        # -----------------------------------
        # Process Results
        # -----------------------------------
        for result in results:

            title = result.get("title", "")
            content = result.get("content", "")
            url = result.get("url", "")

            full_text = f"{title} {content}".lower()

            print("\n----------------------------")
            print("TITLE:", title)
            print("URL:", url)

            # -----------------------------------
            # Skip bad domains
            # -----------------------------------
            if any(bad in url.lower() for bad in bad_domains):

                print("SKIPPED -> Bad Domain")
                continue

            # -----------------------------------
            # Keep only grocery domains
            # -----------------------------------
            if not any(domain in url.lower() for domain in allowed_domains):

                print("SKIPPED -> Not Grocery Domain")
                continue

            # -----------------------------------
            # Product relevance check
            # -----------------------------------
            if product.lower() not in full_text:

                print("SKIPPED -> Product Mismatch")
                continue

            # -----------------------------------
            # Extract Price
            # -----------------------------------
            price = extract_price(full_text)

            print("PRICE:", price)

            if price is None:

                print("SKIPPED -> No Price Found")
                continue

            # -----------------------------------
            # Detect Platform
            # -----------------------------------
            platform = detect_platform(url)

            # -----------------------------------
            # Save Product
            # -----------------------------------
            products.append({
                "platform": platform,
                "price": price,
                "title": clean_title(title),
                "url": url
            })

        # -----------------------------------
        # Remove Duplicates
        # -----------------------------------
        unique_products = []

        seen = set()

        for item in products:

            key = (item["platform"], item["price"])

            if key not in seen:

                seen.add(key)
                unique_products.append(item)

        # -----------------------------------
        # Sort by Lowest Price
        # -----------------------------------
        unique_products.sort(key=lambda x: x["price"])

        print("\n===================================")
        print("FINAL PRODUCTS:")
        print(unique_products)
        print("===================================")

        # -----------------------------------
        # No Results Handling
        # -----------------------------------
        if not unique_products:

            return [{
                "platform": "No Results",
                "price": "Unavailable",
                "title": "No accurate grocery prices found. Try broader search keywords.",
                "url": ""
            }]

        return unique_products

    except Exception as e:

        print("\nERROR:", str(e))

        return [{
            "platform": "Error",
            "price": "Unavailable",
            "title": str(e),
            "url": ""
        }]