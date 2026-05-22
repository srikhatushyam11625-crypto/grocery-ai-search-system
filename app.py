import streamlit as st
import pandas as pd

from parser import parse_query
from search import compare_grocery_prices

# -----------------------------------
# Streamlit page settings
# -----------------------------------

st.set_page_config(

    page_title="AI Grocery Price Comparison",

    layout="centered"
)

# -----------------------------------
# Title
# -----------------------------------

st.title("AI Grocery Price Comparison Engine")

st.write(
    """
    Compare grocery prices across:
    BigBasket, Blinkit, Instamart and Zepto
    """
)

# -----------------------------------
# User input
# -----------------------------------

query = st.text_input(

    "Enter your grocery query",

    placeholder="Example: 1 kg sugar near my location-dwarka sec 13,delhi at lowest price"
)

# -----------------------------------
# Search button
# -----------------------------------

if st.button("Compare Prices"):

    # Parse query
    parsed_query = parse_query(query)

    st.subheader("Parsed Query")

    st.json(parsed_query)

    # Loading spinner
    with st.spinner("Searching grocery platforms..."):

        results = compare_grocery_prices(parsed_query)

    # No results case
    if len(results) == 0:

        st.error(
            "No valid grocery prices found."
        )

    else:

        # Convert to dataframe
        df = pd.DataFrame(results)

        # Rename columns
        comparison_df = df[[
            "platform",
            "price"
        ]]

        comparison_df.columns = [

            "Platform",

            "Price (₹)"
        ]

        # Show table
        st.subheader("Platform Comparison")

        st.dataframe(

            comparison_df,

            use_container_width=True
        )

        # Cheapest option
        cheapest = results[0]

        st.success(

            f"""
            Cheapest Option Found

            Platform: {cheapest['platform']}

            Price: ₹{cheapest['price']}
            """
        )