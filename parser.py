import re
import spacy

nlp = spacy.load("en_core_web_sm")


def parse_query(user_query):

    query = user_query.lower()

    # Quantity extraction
    quantity_pattern = r'(\d+\s?(kg|g|gm|litre|liter|ml|pack))'

    quantity_match = re.search(quantity_pattern, query)

    quantity = quantity_match.group(1) if quantity_match else None

    # Location extraction
    location = None

    if "near my location" in query:

        parts = query.split("near my location")

        if len(parts) > 1:

            location = parts[1]

            location = location.replace("-", " ")
            location = location.replace("at lowest price", "")
            location = location.strip()

    # Intent extraction
    intent = None

    if "lowest price" in query:
        intent = "lowest price"

    # NLP tokenization
    doc = nlp(query)

    stop_words = {
        "near", "my", "location",
        "lowest", "price", "at"
    }

    product_tokens = []

    for token in doc:

        if (
            token.text not in stop_words
            and not token.is_stop
            and not token.is_punct
            and not token.like_num
        ):

            if token.text not in ["kg", "g", "gm", "ml"]:
                product_tokens.append(token.text)

    product = product_tokens[0] if product_tokens else None

    return {
        "product": product,
        "quantity": quantity,
        "location": location,
        "intent": intent
    }