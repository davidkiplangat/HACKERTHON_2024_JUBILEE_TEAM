# HACKERTHON_2024_JUBILEE_TEAM
Holds The Repository for the Hackerthon 


https://jubileeinsurance.com/ug/wp-content/uploads/2024/09/JubiAI-logo.png



# HTML and CSS for the clickable card
card_html = """
    <div style="border-radius: 10px; padding: 20px; 
                margin: 20px; background-color: #f9f9f9; width: 300px;
                 cursor: pointer;
                text-align: center; transition: box-shadow 0.3s ease;">
        <a href="https://www.example.com" target="_blank" style="text-decoration: none; color: black;">
            <h3 style="font-size: 24px;">Click Me!</h3>
            <p>Open a new tab with this clickable card.</p>
        </a>
    </div>
"""

# Use st.markdown to render the clickable card in Streamlit
st.markdown(card_html, unsafe_allow_html=True)
