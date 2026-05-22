import streamlit as st
import pandas as pd

from parser import parse_query
from search import compare_grocery_prices

# -----------------------------------
# Page configuration
# -----------------------------------

st.set_page_config(

    page_title="AI Grocery Price Comparison",

    layout="centered"
)

# -----------------------------------
# App title
# -----------------------------------

st.title("AI Grocery Price Comparison Engine")

st.markdown(

    """
    Compare grocery prices across:

    - BigBasket
    - Blinkit
    - Instamart
    - Zepto
    """
)

# -----------------------------------
# User input
# -----------------------------------

query = st.text_input(

    "Enter grocery query",

    placeholder="Example: 1 kg sugar near my location-dwarka sec 13,delhi at lowest price"
)

# -----------------------------------
# Compare button
# -----------------------------------

if st.button("Compare Prices"):

    # Empty query validation
    if query.strip() == "":

        st.warning(
            "Please enter a valid grocery query."
        )

    else:

        # Parse user query
        parsed_query = parse_query(query)

        # Show parsed query
        st.subheader("Parsed Query")

        st.json(parsed_query)

        # Loading spinner
        with st.spinner("Searching grocery platforms..."):

            results = compare_grocery_prices(parsed_query)

        # No results found
        if len(results) == 0:

            st.error(
                "No accurate grocery prices found."
            )

        else:

            # Convert results to DataFrame
            df = pd.DataFrame(results)

            # Keep only required columns
            comparison_df = df[[
                "platform",
                "price"
            ]]

            # Rename columns
            comparison_df.columns = [

                "Platform",

                "Price (₹)"
            ]

            # Display comparison table
            st.subheader("Platform Comparison")

            st.dataframe(

                comparison_df,

                width="stretch"
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