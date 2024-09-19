import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
import pandas as pd
import requests
import os
import datetime
import sqlite3
import streamlit.components.v1 as components
import time

# Variables
top_cards = """
            <div style="display: flex; justify-content: space-between;">
                <div class="footer-links" style="width: 45%;">
                    <a class="sidebar-link" target="_blank" href="https://jubileeinsurance.com/ke/blog/">Blog</a><br>
                    <a class="sidebar-link" target="_blank" href="https://jubileeinsurance.com/ke/privacy/">Privacy Policy</a>
                    <a class="sidebar-link" target="_blank" href="https://jubileeinsurance.com/ke">www.jubileeinsurance.com</a>
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
            """
# style css
styles = """
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
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            background-color: #f9f9f9;
            width: 45%;
        }
                .conversation {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 10px;
        }
        .user-input {
            text-align: right;
            width: 45%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background-color: #e0f7fa;
        }
        .response {
            text-align: left;
            width: 45%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background-color: #f1f8e9;
        }
        .timestamp {
            text-align: center;
            color: #888;
            font-size: 12px;
            margin-top: 10px;
        }
        .conversation-log {
            margin-bottom: 20px;
        }
        </style>
        """
defaults_questions = """
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
        """


# Render the question cards section
def render_defaults_questions():
    defaults_questions = """
    <div class="question-cards">
        <div class="card">
            <strong>What insurance products can I get to cover my health needs? 
            <svg class="inline" width="0.5rem" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M1 9L9 1M9 1H2.5M9 1V7.22222" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"></path></svg>
            </strong>
        </div>
        <div class="card">
            <strong>How can I find the best investment plan for my future? 
            <svg class="inline" width="0.5rem" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M1 9L9 1M9 1H2.5M9 1V7.22222" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"></path></svg>
            </strong>
        </div>
        <div class="card">
            <strong>What are the steps in the insurance claim process? 
            <svg class="inline" width="0.5rem" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M1 9L9 1M9 1H2.5M9 1V7.22222" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"></path></svg>
            </strong>
        </div>
    </div>
    """
    st.markdown(defaults_questions, unsafe_allow_html=True)


# Custom CSS for styling the cards and buttons
def add_custom_css():
    st.markdown(
        """
        <style>
        .question-cards {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .question-cards .card {
            background-color: #f0f4f8;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .question-cards .card:hover {
            background-color: #e0e7ff;
        }
        .question-cards .card svg {
            margin-left: 8px;
            vertical-align: middle;
        }
        .quick-response {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
            transition: background-color 0.3s ease;
        }
        .quick-response:hover {
            background-color: #0056b3;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# a . Log Conversations Logs && # Ensure log file exists
LOG_FILE = "conversation_log.txt"
if not os.path.exists(LOG_FILE):
    open(LOG_FILE, "w").close()


# Initialize database
def init_db():
    conn = sqlite3.connect("conversation_history_.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS conversation_history (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user_input TEXT,
            response TEXT
        )
    """
    )
    # Create conversation_snapshot table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS conversation_snapshot (
            snapshot_id INTEGER,
            user_id INTEGER,
            timestamp TEXT,
            user_input TEXT,
            response TEXT
        )
        """
    )

    # Create users table to store registered users
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            useremail TEXT UNIQUE,
            fullname TEXT,
            userphoneno TEXT,
            password TEXT
        )
        """
    )
    conn.commit()
    return conn


# Store conversation into the database
def store_conversation(timestamp, user_input, response):
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO conversation_history (timestamp, user_input, response)
        VALUES (?, ?, ?)
        """,
        (timestamp, user_input, response),
    )
    conn.commit()
    conn.close()


# Read conversation history from the database
def read_conversation_history():
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conversation_history ORDER BY timestamp ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def read_top_conversation_history():
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conversation_history ORDER BY timestamp ASC limit 1")
    rows = cursor.fetchall()
    conn.close()
    return rows


def clear_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as log:
            log.write("")  # Clear the file content
    conn = sqlite3.connect("conversation_history_.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM conversation_history")  # Clear database entries
    conn.commit()
    conn.close()
    st.success("Chat logs cleared!")


def load_charts_from_api(message):
    api_url = "https://jubgpt-f5g4ceeahbh9ephy.westeurope-01.azurewebsites.net/api/jubchat/inquire"
    headers = {"Content-Type": "application/json"}  # No API key needed
    response = requests.post(api_url, headers=headers, json=message)
    # Check for 400 response content
    if response.status_code == 400:
        response.raise_for_status()
    responce_feedback = response.text
    return response


def get_responce_from_llm_new_user(userid, message, chatid=0):
    api_url = f"https://jubgpt-f5g4ceeahbh9ephy.westeurope-01.azurewebsites.net/api/jubchat/inquire/{userid}/chats/{chatid}"
    headers = {"Content-Type": "application/json"}  # No API key needed
    response = requests.post(api_url, headers=headers, json=message)
    # Check for 400 response content
    if response.status_code == 400:
        response.raise_for_status()
    response_json = response.json()
    # Parse the response as JSON
    chat_id = response_json.get("chatId", None)
    answer = response_json.get("answer", "No answer provided")
    return userid, chatid, message, answer


# Initialize session state for button clicks
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = None


def display_jcare_options():
    # Create a container for buttons and text input
    col1 = st.columns(1)
    with col1[0]:
        card_html = """  
            <div style="border-radius: 10px; padding: 20px;   
                        margin: 20px; background-color: #f9f9f9;   
                        cursor: pointer; text-align: left;   
                        transition: box-shadow 0.3s ease;   
                        width: calc(100% - 60px); max-width: 100%; display: inline-block;">  
                <a href="https://jubileeinsurance.com/ke/product/j-care-medical-cover/'" target="_blank" style="text-decoration: none; color: black;">  
                    <p>Proceed to buy a J Care policy and get a policy in 5 mins!?</p>  
                </a>  
            </div>  
        """
        st.markdown(card_html, unsafe_allow_html=True)


def display_top_chat():
    from datetime import datetime

    conversation_history = read_top_conversation_history()
    for conversation in conversation_history:
        user_id, timestamp, user_input, response = conversation
        timestamp = datetime.fromisoformat(timestamp).strftime("%d/%m/%Y, %H:%M:%S")
        # Display the user input message (if available)
        if user_input:
            col1, col2 = st.columns([3, 1])  # User message aligned to the right
            with col1:
                st.markdown(
                    f"<div style='background-color: #e1ffc7; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>"
                    f"<b>Me:</b> {user_input} <br><small style='color: grey;'>{timestamp}</small></div>",
                    unsafe_allow_html=True,
                )

        # Display the response message (if available)
        if response:
            col1, col2 = st.columns([1, 3])  # Response message aligned to the left
            with col2:
                st.markdown(
                    f"<div style='background-color: #f1f1f1; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>"
                    f"<b>Ans:</b> {response} <br><small style='color: grey;'>{timestamp}</small></div>",
                    unsafe_allow_html=True,
                )


# Function to display messages with timestamps
def display_chat():
    from datetime import datetime

    conversation_history = read_conversation_history()
    for conversation in conversation_history:
        user_id, timestamp, user_input, response = conversation
        timestamp = datetime.fromisoformat(timestamp).strftime("%d/%m/%Y, %H:%M:%S")
        # Display the user input message (if available)
        if user_input:
            col1, col2 = st.columns([3, 1])  # User message aligned to the right
            with col1:
                st.markdown(
                    f"<div style='background-color: #e1ffc7; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>"
                    f"<b>Me:</b> {user_input} <br><small style='color: grey;'>{timestamp}</small></div>",
                    unsafe_allow_html=True,
                )

        # Display the response message (if available)
        if response:
            col1, col2 = st.columns([1, 3])  # Response message aligned to the left
            with col2:
                st.markdown(
                    f"<div style='background-color: #f1f1f1; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>"
                    f"<b>Ans:</b> {response} <br><small style='color: grey;'>{timestamp}</small></div>",
                    unsafe_allow_html=True,
                )


def login_component():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "user" and password == "password":  # Simple hardcoded check
            st.session_state["logged_in"] = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password.")


# Register component
def register_component():
    st.subheader("Register")
    useremail = st.text_input("Email")
    fullname = st.text_input("FullName")
    userphoneno = st.text_input("Phone")
    password = st.text_input("Passwords", type="password")
    passwords = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if (
            useremail == "user@gmail.com"
            and password == "password"
            and passwords == password
            and fullname > 4
            and len(userphoneno) == 10
        ):  # Simple hardcoded check
            st.session_state["Registered"] = True
            st.success("Registered successfully!")
        elif password == "password" and passwords != password:
            st.session_state["Registered"] = False
            st.error("wrong password retyped.")
        else:
            st.session_state["Registered"] = False
            st.error("member already logged in or wrong password retyped.")


# Functions Tab
# 1 . Call api and get responce
def send_prompt_request(message):
    api_url = "https://jubgpt-f5g4ceeahbh9ephy.westeurope-01.azurewebsites.net/api/jubchat/inquire"
    headers = {"Content-Type": "application/json"}  # No API key needed
    response = requests.post(api_url, headers=headers, json=message)
    # Check for 400 response content
    if response.status_code == 400:
        response.raise_for_status()
    responce_feedback = response.text
    return responce_feedback


# 2. Get User Inputs
def get_user_inputs():
    user_input = st.text_area(
        "Describe what you're looking for",
        value="" if not st.session_state.clear_input else "",
        placeholder="E.g., I need insurance for my car in case of accidents and theft.",
        key="user_input_area",
    )
    return user_input


# 3. Get prompt response from Jubilee GPT
def process_user_request(conn):
    user_input = get_user_inputs()
    response = get_responce_from_llm_new_user(1, message=user_input, chatid=0)
    # response = send_prompt_request(user_input)
    return response


# 4 . Logging function
def log_conversation(user_input, responce_feedback):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"Timestamp: {datetime.datetime.now()}\n")
        log_file.write(f"User Input: {user_input}\n")
        log_file.write(f"Response: {responce_feedback}\n")
        log_file.write("-" * 50 + "\n")


# 5 . Read The conversations from the logs
def read_conversation_log():
    with open(LOG_FILE, "r") as log_file:
        return log_file.read()


def main(top_cards, styles, defaults_questions):
    # Sidebar
    with st.sidebar:
        #  st.image("logo.webp", width=150)  # Replace with your logo path
        st.image(
            "https://microproducts.jubileeinsurance.com/images/abc/main-logo.svg",
            width=150,
        )
        st.markdown(
            '<div class="live-free" style="padding-top: 70px"></div>',
            unsafe_allow_html=True,
        )
        signup_options = ["Login", "Sign Up", "Try Me !!"]
        # if st.radio("Please Login to proceed", signup_options, key="nav_list"):
        selected_option = st.radio(
            "Please Login to proceed", signup_options, key="nav_list"
        )
        # Check which option was selected
        if selected_option == "Login":
            st.write("Please Login to proceed")
            login_component()
        elif selected_option == "Sign Up":
            st.write("Please Sign Up")
            register_component()
        st.divider()
        st.image("advert4.png", use_column_width=True)  # Replace with your advert image
        st.image(
            "advert3.png", use_column_width=True
        )  # Uncomment if you have a second advert
        st.markdown("---")
        st.markdown(
            # Load Top Sections for the app
            top_cards,
            unsafe_allow_html=True,
        )
    # Main content
    st.markdown(
        # Load the styles for this section
        styles,
        unsafe_allow_html=True,
    )
    # Display the image with HTML and CSS, pointing to the static directory
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://jubileeinsurance.com/ug/wp-content/uploads/2024/09/JubiAI-logo.png" width="250">
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="main-header">
            <div style="text-align:center; font-weight: bold; font-size: 34px;" class="header-text">Jisort, Jielimishe With Jubi-AI</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="live-free">#LiveFree</div>', unsafe_allow_html=True)
    st.markdown("### Quick Responses")
    render_defaults_questions()

    # Manage session state
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    if "clear_input" not in st.session_state:
        st.session_state.clear_input = False
    # Process the input and recommend products
    display_chat()
    user_input = get_user_inputs()
    response = get_responce_from_llm_new_user(1, message=user_input, chatid=0)[3]
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit"):
            if user_input:
                user_input += "  In Jubilee Insurance"
                # Process the input and get relevant products
                if "j-care" in response.lower():
                    display_jcare_options()
                # st.markdown(card_html, unsafe_allow_html=True)
                log_conversation(user_input, response)
                timestamp = datetime.datetime.now().isoformat()
                store_conversation(timestamp, user_input, response)
                st.session_state.conversation_history.append((user_input, response))
                st.session_state.clear_input = True
                # display_chat()
    with col2:
        if st.button("Clear Chats"):
            # store_conversation_snapshot()
            clear_logs()
    st.write(response)


if __name__ == "__main__":
    main(top_cards, styles, defaults_questions)
