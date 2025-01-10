import streamlit as st
import requests
import json

# Set page config
st.set_page_config(page_title="EDU.AI - Interactive Learning Platform", layout="wide")

# Title and sidebar
st.title("EDU.AI - Interactive Learning Platform")

# Sidebar Navigation
menu = ["Home", "Quiz", "Ranks", "AI Chat", "Assignments", "Rewards", "Profile", "Settings"]
choice = st.sidebar.radio("Navigation", menu)

# OpenAI API Setup
API_KEY = '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'
API_URL = 'https://api.openai.com/v1/chat/completions'

# Function to fetch AI Chat Response
def get_ai_response(prompt):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-4',
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 150
    }
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    return response.json()['choices'][0]['message']['content']

# Home Page
if choice == "Home":
    st.subheader("Reels-Like Flashcards")
    st.write("Swipe through current affairs topics interactively!")

    # Flashcard Example
    with st.container():
        st.info("Question: What is the capital of France?")
        if st.button("Show Answer"):
            st.success("Answer: Paris")

    st.write("More flashcards coming soon!")

# Quiz Page
elif choice == "Quiz":
    st.subheader("Quiz Section")
    st.write("Test your knowledge with quizzes.")

    # Sample Quiz Question
    st.write("Question: Which is the largest planet in our solar system?")
    options = ["Mars", "Jupiter", "Saturn", "Neptune"]
    answer = st.radio("Choose your answer:", options)

    if st.button("Submit Answer"):
        if answer == "Jupiter":
            st.success("Correct Answer!")
        else:
            st.error("Wrong Answer. Try Again!")

# Ranks Page
elif choice == "Ranks":
    st.subheader("Leaderboard")
    st.write("Check out the top performers.")

    # Example Leaderboard
    ranks = [
        {"name": "John D.", "score": 2450},
        {"name": "Jane S.", "score": 2300},
        {"name": "Mike T.", "score": 2150}
    ]

    for rank, user in enumerate(ranks, 1):
        st.write(f"{rank}. {user['name']} - {user['score']} pts")

# AI Chat Page
elif choice == "AI Chat":
    st.subheader("AI Chatbot")
    st.write("Ask questions and get AI-powered answers!")

    # Chat Interface with modern UI
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    user_input = st.chat_input("Type your message...")
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                ai_response = get_ai_response(user_input)
                st.markdown(ai_response)
        
        # Add AI message to chat history
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

# Assignments Page
elif choice == "Assignments":
    st.subheader("Assignments")
    st.write("View and manage your assignments.")

    assignments = [
        {"title": "Math Quiz 1", "due": "2025-01-10", "status": "Pending"},
        {"title": "Science Project", "due": "2025-01-15", "status": "Completed"}
    ]

    for assignment in assignments:
        st.write(f"{assignment['title']} - Due: {assignment['due']} - Status: {assignment['status']}")

# Rewards Page
elif choice == "Rewards":
    st.subheader("Rewards")
    st.write("Track your rewards and achievements.")

    rewards = [
        {"title": "Top Scorer Badge", "points": 500},
        {"title": "Quiz Master", "points": 300}
    ]

    for reward in rewards:
        st.write(f"{reward['title']} - {reward['points']} points")

# Profile Page
elif choice == "Profile":
    st.subheader("Profile")
    st.write("View and edit your profile information.")

    st.text_input("Name", "John Doe")
    st.text_input("Email", "johndoe@example.com")
    st.text_input("Phone", "+1234567890")
    if st.button("Save Changes"):
        st.success("Profile updated successfully!")

# Settings Page
elif choice == "Settings":
    st.subheader("Settings")
    st.write("Adjust your preferences.")

    dark_mode = st.checkbox("Enable Dark Mode")
    notifications = st.checkbox("Enable Notifications")
    language = st.selectbox("Language", ["English", "Spanish", "French"])

    if st.button("Save Settings"):
        st.success("Settings saved successfully!")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Contact us at: support@edu.ai")
