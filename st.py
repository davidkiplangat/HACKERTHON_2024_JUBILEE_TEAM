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
    # Sidebar
    with st.sidebar:
        st.image("logo.webp", width=150)  # Replace with your logo path

        st.image("advert4.png", use_column_width=True)  # Replace with your advert image
        st.image("advert3.png", use_column_width=True)  # Uncomment if you have a second advert

        st.markdown("---")
      
        st.markdown(
            """
            <div style="display: flex; justify-content: space-between;">
                <div class="footer-links" style="width: 45%;">
                    <a class="sidebar-link" href="#">Terms & Conditions</a><br>
                    <a class="sidebar-link" href="#">Privacy Policy</a>
                </div>
                <div style="width: 45%;">
                    <div class="sidebar-contact">
                        <div class="contact-item"><strong><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pin-map-fill" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M3.1 11.2a.5.5 0 0 1 .4-.2H6a.5.5 0 0 1 0 1H3.75L1.5 15h13l-2.25-3H10a.5.5 0 0 1 0-1h2.5a.5.5 0 0 1 .4.2l3 4a.5.5 0 0 1-.4.8H.5a.5.5 0 0 1-.4-.8z"/>
                            <path fill-rule="evenodd" d="M4 4a4 4 0 1 1 4.5 3.969V13.5a.5.5 0 0 1-1 0V7.97A4 4 0 0 1 4 3.999z"/>
                            </svg> Jubilee Insurance - Nairobi</strong></div>
                                <div class="contact-item"><strong><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-telephone-fill" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M1.885.511a1.745 1.745 0 0 1 2.61.163L6.29 2.98c.329.423.445.974.315 1.494l-.547 2.19a.68.68 0 0 0 .178.643l2.457 2.457a.68.68 0 0 0 .644.178l2.189-.547a1.75 1.75 0 0 1 1.494.315l2.306 1.794c.829.645.905 1.87.163 2.611l-1.034 1.034c-.74.74-1.846 1.065-2.877.702a18.6 18.6 0 0 1-7.01-4.42 18.6 18.6 0 0 1-4.42-7.009c-.362-1.03-.037-2.137.703-2.877z"/>
                            </svg> 0709949000</strong></div>
                                <div class="contact-item"><strong><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-envelope-open-fill" viewBox="0 0 16 16">
                            <path d="M8.941.435a2 2 0 0 0-1.882 0l-6 3.2A2 2 0 0 0 0 5.4v.314l6.709 3.932L8 8.928l1.291.718L16 5.714V5.4a2 2 0 0 0-1.059-1.765zM16 6.873l-5.693 3.337L16 13.372v-6.5Zm-.059 7.611L8 10.072.059 14.484A2 2 0 0 0 2 16h12a2 2 0 0 0 1.941-1.516M0 13.373l5.693-3.163L0 6.873z"/>
                            </svg> Talk2Us@jubileekenya.com</strong></div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Main content
    st.markdown(
        """
        <style>
        .main-logo {
            display: flex;
            justify-content: center;
        }
        .main-header {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 0px;
        }
        .header-text {
            margin: 0 10px;
            font-size: 24px;
        }
        .live-free {
            text-align: center;
            color: #BA0C2F;
            font-size: 32px;
           # margin: 20px 0;
        }
        .question-cards {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin: 20px 0;
        }
        .footer-links a{
        color: #BA0C2F;
        text-decoration: none;
        }
        .footer-links a{
          text-decoration: underline;
        }
        .card {
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            background-color: #f9f9f9;
            width: 45%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # st.image("icon-top.png", width=150) 

    # Center the image using HTML and CSS
    # st.markdown(
    #     """
    #     <div style="text-align: center;">
    #         <img src="icon-top.png" width="150">
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )


    st.markdown(
        """
        <div class="main-header">
            <div style="text-align:center; font-weight: bold; font-size: 34px;" class="header-text">Jisort, Jielimishe With Jub-GPT</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="live-free">#LiveFree</div>', unsafe_allow_html=True)

    # Inline block cards for random questions
    st.markdown(
        """
        <div class="question-cards">
            <div class="card">
                <strong>What insurance products can I get to cover my health needs? <svg class="inline" width="0.5rem" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1 9L9 1M9 1H2.5M9 1V7.22222" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"></path></svg></strong>
            </div>
            <div class="card">
                <strong>How can I find the best investment plan for my future? <svg class="inline" width="0.5rem" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1 9L9 1M9 1H2.5M9 1V7.22222" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"></path></svg></strong>
            </div>
            <div class="card">
                <strong>How can I find the best investment plan for my future? <svg class="inline" width="0.5rem" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1 9L9 1M9 1H2.5M9 1V7.22222" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"></path></svg></strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Chat search bar
   # st.text_input("Type your question here:")

    # Input area for user request
    user_input = st.text_area(
        "Describe what you're looking for",
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
