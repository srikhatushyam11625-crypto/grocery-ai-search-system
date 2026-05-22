import streamlit as st
import pandas as pd

from parser import parse_query
from search import search_grocery

st.title("AI Grocery Price Comparison System")

query = st.text_input(
    "Enter grocery search query"
)

if st.button("Search"):

    parsed_query = parse_query(query)

    st.subheader("Parsed Query")

    st.json(parsed_query)

    results = search_grocery(parsed_query)

    if len(results) == 0:

        st.warning(
            "No grocery price results found."
        )

    else:

        st.subheader("Price Comparison Results")

        df = pd.DataFrame(results)

        st.dataframe(df)

        cheapest = results[0]

        st.success(

            f"""
            Cheapest Option:

            {cheapest['title']}

            Price: ₹{cheapest['price']}
            """
        )