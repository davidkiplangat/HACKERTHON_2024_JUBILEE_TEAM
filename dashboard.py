import streamlit as st
from datetime import datetime

# Sample data for demonstration purposes
old_chats = [
    {"id": 1, "question": "What is AI?", "answer": "AI stands for Artificial Intelligence."},
    {"id": 2, "question": "What is Streamlit?", "answer": "Streamlit is a Python library for creating web apps."},
    
]

# Function to delete selected chats
def delete_selected_chats(selected_ids):
    global old_chats
    old_chats = [chat for chat in old_chats if chat['id'] not in selected_ids]

# Sidebar for old chats
st.sidebar.header("Previous Chats")
chat_titles = [f"{chat['id']}: {chat['question']}" for chat in old_chats]
selected_ids = []

# Create checkboxes for each chat
for chat in old_chats:
    if st.sidebar.checkbox(f"{chat['question']}"):
        selected_ids.append(chat['id'])

if st.sidebar.button("Delete Selected"):
    delete_selected_chats(selected_ids)
    st.sidebar.success("Selected chats deleted successfully.")

# Main chat area
st.title("Jubilee GPT")

# st.subheader("Chat with AI")

# Display old chats
st.subheader("Chat History")
for chat in old_chats:
    st.markdown(f"**You:** {chat['question']}")
    st.markdown(f"**AI:** {chat['answer']}")


st.markdown("---")

# Chat input
user_input = st.text_input("You: ", placeholder="Type your question here...")

if st.button("Send"):
    # Simulate AI response (for demonstration)
    response = f"Response to: {user_input}"  # Here you would integrate your AI model
    old_chats.append({"id": len(old_chats) + 1, "question": user_input, "answer": response})


st.markdown("---")
    # Login component
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
 
def main():
    # Check if user is logged in
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        login_component()
        return

login_component()

st.markdown("---")

# Register component
def register_component():
    st.subheader("Register")
    useremail = st.text_input("Email")
    fullname = st.text_input("FullName")
    userphoneno = st.text_input("Phone")
    password = st.text_input("Passwords", type="password")
    passwords = st.text_input("Confirm Password", type="password")
   
    if st.button("Register"):
        if useremail == "user@gmail.com" and password == "password" and passwords==password and fullname > 4 and len(userphoneno) == 10:  # Simple hardcoded check
            st.session_state["Registered"] = True
            st.success("Registered successfully!")
        elif password == "password" and passwords != password:
            st.session_state["Registered"] = False
            st.error("wrong password retyped.")
        else:
            st.session_state["Registered"] = False
            st.error("member already logged in or wrong password retyped.")
 
def main():
    # Check if user is logged in
    if "Registered" not in st.session_state or not st.session_state["Registered"]:
        register_component()
        return


register_component()

st.markdown("---")



# Function to display messages with timestamps
def display_message(message, is_user):
    timestamp = datetime.now().strftime("%H:%M:%S")  # Format the timestamp
    if is_user:
        col1, col2 = st.columns([3, 1])  # User message on the right
        with col1:
            st.markdown(
                f"<div style='background-color: #e1ffc7; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>"
                f"<b>Me:</b> {message} <br><small style='color: grey;'>{timestamp}</small></div>",
                unsafe_allow_html=True
            )
    else:
        col1, col2 = st.columns([1, 3])  # Response on the left
        with col2:
            st.markdown(
                f"<div style='background-color: #f1f1f1; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>"
                f"<b>Ans:</b> {message} <br><small style='color: grey;'>{timestamp}</small></div>",
                unsafe_allow_html=True
            )

# Main app
st.title("Chat Widget")

# Static messages for demonstration
static_messages = [
    
    ("I need assistance with my tax return.", True),
    ("Sure! What specific help do you need?", False),
    ("Can you explain the filing process?", True),
    ("Hello! How can I help you today?", False),
]

# Display static messages
for message, is_user in static_messages:
    display_message(message, is_user)





# User icon and profile options
st.sidebar.image("https://icons.veryicon.com/png/o/miscellaneous/standard/avatar-15.png", width=50)  # User icon
st.sidebar.subheader("User Profile")
if st.sidebar.button("Profile"):
    st.sidebar.write("User Profile Page (To be implemented)")
if st.sidebar.button("Logout"):
    st.sidebar.write("Logout functionality (To be implemented)")
