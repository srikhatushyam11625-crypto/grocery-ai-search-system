import streamlit as st
import pandas as pd

from parser import parse_query
from search import compare_grocery_prices

st.title("AI Grocery Price Comparison Engine")

query = st.text_input(
    "Enter grocery query"
)

if st.button("Compare Prices"):

    parsed_query = parse_query(query)

    st.subheader("Parsed Query")

    st.json(parsed_query)

    with st.spinner("Searching grocery platforms..."):

        results = compare_grocery_prices(parsed_query)

    if len(results) == 0:

        st.error(
            "No valid grocery prices found."
        )

    else:

        st.subheader("Platform Comparison")

        df = pd.DataFrame(results)

        st.dataframe(

            df[[
                "platform",
                "price",
                "title",
                "url"
            ]]
        )

        cheapest = results[0]

        st.success(

            f"""
            Cheapest Option Found:

            Platform: {cheapest['platform']}

            Price: ₹{cheapest['price']}
            """
        )