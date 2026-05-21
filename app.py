import streamlit as st

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

    st.subheader("Live Search Results")

    for result in results["results"]:

        st.write("Title:", result["title"])

        st.write("URL:", result["url"])

        st.write("Content:", result["content"])

        st.write("---")