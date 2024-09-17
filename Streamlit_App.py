import streamlit as st


# Define a function to render the chat interface
def chat_interface():
    st.title("Chat Interface")

    # Sidebar for user settings
    with st.sidebar:
        st.header("Products and Services")
        option = st.selectbox(
            "Select a product or service:",
            ["Select an option", "HEALTH", "LIFE", "JAML", "CONSULTING", "AOBS"],
        )
        st.header("App Info")

        # Provide specific descriptions based on the selected product or service
        if option == "Select an option":
            description = """
            **Chat Interface App**

            This application provides an interactive platform where users can engage in real-time conversations with a sophisticated assistant. Whether you have questions about our products and services or need assistance with other inquiries, this app is designed to offer immediate, insightful responses. The user-friendly chat interface ensures a seamless experience, allowing you to easily navigate through different service options and receive tailored information. You can also explore our various products and services through the dropdown menu, making it easy to find relevant details.

            Key functionalities include:
            - **Chat Interface**: Engage in a conversational interface where you can ask questions and receive responses.
            - **Products and Services Dropdown**: Select from various products and services to get tailored information.
            - **Real-time Interaction**: Type your message and receive an immediate response from the assistant.
            - **Customizable Experience**: Customize the chat experience according to your preferences.

            Explore and learn more about our offerings to get the most out of your interaction with our assistant.
            """
        else:
            descriptions = {
                "HEALTH": """
                **HEALTH**

                Our HEALTH service offers comprehensive solutions for individuals and organizations looking to improve their wellness and healthcare management. We provide access to a range of health resources, including personalized health assessments, expert medical consultations, and wellness programs. Our goal is to help you make informed health decisions and manage your health proactively. With the latest advancements in health technology and data analytics, our service ensures you receive the best care and support tailored to your specific needs.
                """,
                "LIFE": """
                **LIFE**

                The LIFE service is designed to support individuals in achieving their personal and professional goals. Whether you're looking for career development, financial planning, or personal growth, our LIFE service offers a variety of resources and tools to help you succeed. We provide expert guidance, strategic planning, and actionable insights to help you navigate life's challenges and opportunities. Our commitment is to empower you with the knowledge and support needed to thrive in all aspects of your life.
                """,
                "JAML": """
                **JAML**

                JAML (Just Another Machine Learning) is our cutting-edge machine learning service designed for data-driven decision-making and advanced analytics. This service leverages state-of-the-art algorithms and models to analyze complex data, uncover insights, and drive strategic outcomes. Whether you're working on predictive analytics, data visualization, or model development, JAML provides the tools and expertise needed to harness the power of machine learning effectively. Our service is tailored to meet the needs of both beginners and advanced users in the field of data science.
                """,
                "CONSULTING": """
                **CONSULTING**

                Our CONSULTING service offers expert advice and strategic solutions to help businesses and organizations achieve their objectives. We provide customized consulting services across various domains, including management, technology, and operations. Our team of experienced consultants works closely with clients to identify challenges, develop actionable strategies, and implement effective solutions. Whether you need assistance with project management, process optimization, or technology integration, our CONSULTING service is here to guide you through every step of the process.
                """,
                "AOBS": """
                **AOBS**

                AOBS (Advanced Operations and Business Solutions) is our specialized service focusing on optimizing business operations and enhancing operational efficiency. We offer a range of solutions to streamline processes, improve productivity, and drive business growth. Our AOBS service includes operational audits, process reengineering, and technology implementation to help organizations achieve their operational goals. With a focus on innovation and best practices, AOBS provides the expertise needed to elevate your business operations to the next level.
                """,
            }
            description = descriptions.get(option, "Description not available.")

        st.write(description)

    # Display chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f"<div style='text-align: right;'><b>User:</b> {msg['content']}</div>",
                unsafe_allow_html=True,
            )
        elif msg["role"] == "assistant":
            st.markdown(
                f"<div style='text-align: left;'><b>Assistant:</b> {msg['content']}</div>",
                unsafe_allow_html=True,
            )

    # Input box for the user to type a message
    user_input = st.text_input("Type your message:")

    # Send message
    if st.button("Send"):
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            # Here you would add code to get a response from the assistant
            # For demonstration purposes, we'll just echo the user's message
            assistant_response = f"Echo: {user_input}"
            st.session_state.messages.append(
                {"role": "assistant", "content": assistant_response}
            )
            st.experimental_rerun()


# Run the chat interface
if __name__ == "__main__":
    chat_interface()
