# app.py

import streamlit as st
import pandas as pd

from search import search_grocery_prices

# -----------------------------------
# Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="AI Grocery Price Comparison",
    page_icon="🛒",
    layout="wide"
)

# -----------------------------------
# Main Title
# -----------------------------------
st.title("🛒 AI Grocery Price Comparison Search Engine")

st.markdown("""
Compare grocery prices across Blinkit, Zepto, BigBasket, Instamart, and JioMart using AI-powered search.
""")

# -----------------------------------
# Sidebar Settings
# -----------------------------------
st.sidebar.header("Search Settings")

location = st.sidebar.text_input(
    "Enter Location",
    value="Delhi"
)

quantity = st.sidebar.selectbox(
    "Select Quantity",
    [
        "500 g",
        "1 kg",
        "2 kg",
        "5 kg"
    ]
)

# -----------------------------------
# User Input
# -----------------------------------
product = st.text_input(
    "Enter Grocery Product",
    placeholder="Example: sugar, rajma, poha, daliya"
)

# -----------------------------------
# Search Button
# -----------------------------------
search_button = st.button("🔍 Search Prices")

# -----------------------------------
# Search Logic
# -----------------------------------
if search_button:

    if not product.strip():

        st.warning("Please enter a grocery product.")

    else:

        with st.spinner("Searching grocery prices..."):

            results = search_grocery_prices(
                product=product,
                quantity=quantity,
                location=location
            )

        # -----------------------------------
        # Convert to DataFrame
        # -----------------------------------
        df = pd.DataFrame(results)

        # -----------------------------------
        # Handle Errors / Empty Results
        # -----------------------------------
        if df.iloc[0]["platform"] == "No Results":

            st.warning(df.iloc[0]["title"])

        elif df.iloc[0]["platform"] == "Error":

            st.error(df.iloc[0]["title"])

        else:

            # -----------------------------------
            # Cheapest Product
            # -----------------------------------
            cheapest = df.iloc[0]

            st.success(
                f"✅ Cheapest Price: ₹{cheapest['price']} on {cheapest['platform']}"
            )

            # -----------------------------------
            # Platform Comparison Table
            # -----------------------------------
            st.subheader("📊 Platform Price Comparison")

            comparison_df = df[["platform", "price"]]

            comparison_df.columns = [
                "Platform",
                "Price (₹)"
            ]

            st.dataframe(
                comparison_df,
                width='stretch'
            )

            # -----------------------------------
            # Detailed Results
            # -----------------------------------
            st.subheader("🧾 Detailed Search Results")

            for index, row in df.iterrows():

                with st.container():

                    st.markdown("---")

                    st.markdown(
                        f"### {row['platform']}"
                    )

                    st.write(
                        f"💰 Price: ₹{row['price']}"
                    )

                    st.write(
                        f"🛍️ Product: {row['title']}"
                    )

                    if row["url"]:

                        st.markdown(
                            f"[🔗 View Product]({row['url']})"
                        )

# -----------------------------------
# Footer
# -----------------------------------
st.markdown("---")

st.caption(
    "Built using Python, Streamlit, Tavily AI Search API, NLP, spaCy, GitHub, and AWS."
)