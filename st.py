import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
import pandas as pd

# Sample product details and descriptions
products = pd.DataFrame(
    {
        "product_name": [
            "Life Insurance",
            "Health Insurance",
            "Car Insurance",
            "Home Insurance",
            "Investment Plan",
        ],
        "description": [
            "Life cover with death benefit and tax savings",
            "Comprehensive health coverage for individuals and families",
            "Covers damage to vehicles, accidents, and theft",
            "Protection for home and property, including fire and natural disasters",
            "Grow your money with safe and high returns in investment funds",
        ],
    }
)


def process_input(user_input, product_descriptions):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(product_descriptions)

    # Simulate relevance by matching keywords
    relevance_scores = []
    for description in product_descriptions:
        common_words = set(user_input.lower().split()) & set(
            description.lower().split()
        )
        relevance = len(common_words) / len(description.split())
        relevance_scores.append(relevance)

    # Create a dataframe of product descriptions with relevance scores
    product_df = pd.DataFrame(
        {
            "Product": products["product_name"],
            "Description": product_descriptions,
            "Relevance": relevance_scores,
        }
    )
    product_df = product_df.sort_values(by="Relevance", ascending=False)
    return product_df


def main():
    st.title("Smart Product Recommendation")
    st.write(
        "Describe what you're looking for, and we'll match you with the most relevant product."
    )

    # Input area for user request
    user_input = st.text_area(
        "Enter your needs",
        value="",
        placeholder="E.g., I need insurance for my car in case of accidents and theft.",
    )
    # Process the input and recommend products
    if st.button("Get Recommendation"):
        if user_input:
            # Process the input and get relevant products
            recommendations = process_input(user_input, products["description"])

            # Display the top recommended product
            top_product = recommendations.iloc[0]
            st.write(f"**Top Recommended Product: {top_product['Product']}**")
            st.write(f"Description: {top_product['Description']}")
            st.progress(top_product["Relevance"])

            # Display all other products sorted by relevance
            st.write("### Other relevant products:")
            for i, row in recommendations.iloc[1:].iterrows():
                st.write(
                    f"**{row['Product']}** - Relevance: {round(row['Relevance']*100, 2)}%"
                )
                st.write(f"Description: {row['Description']}")
        else:
            st.error("Please enter a product description to get recommendations.")


# Run the app
if __name__ == "__main__":
    main()
