import streamlit as st
from parser import parse_query

st.title("AI Grocery Price Search System")

query = st.text_input("Enter your grocery search query")

if st.button("Search"):

    result = parse_query(query)

    st.write("Parsed Query:")
    st.json(result)