import json
import pandas as pd
import requests
import streamlit as st
import mysql.connector
import openai
import time

# Set page config
st.set_page_config(page_title="EDU.AI - Interactive Learning Platform", layout="wide")

# Sidebar with Logo
st.sidebar.image("logo.png", width=150)  # Logo with fixed width

# Sidebar Menu
menu = [
    {"icon": "🏠", "label": "Home"},
    {"icon": "📚", "label": "Quiz"},
    {"icon": "🤖", "label": "AI Chat"},
    {"icon": "👤", "label": "Profile"},
]

# Initialize session state for navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# Sidebar with custom buttons
for item in menu:
    if st.sidebar.button(f"{item['icon']} {item['label']}"):
        st.session_state.current_page = item['label']

######################################################### HOME PAGE  ##################################################################

def show_home():
    st.title("Welcome to EDU.AI!")
    col1, col2 = st.columns([1, 1])  # Adjust column widths as needed

    # Clickable Current Affairs Section
    with col1:
        if st.button("Go to Current Affairs"):
            st.session_state.current_page = "Current Affairs"
        st.image("cf.png", use_container_width=True)
        st.subheader("Current Affairs")
        st.write("Stay updated with the latest current affairs from around the world.")

    # Clickable General Knowledge Section
    with col2:
        if st.button("Go to General Knowledge"):
            st.session_state.current_page = "General Knowledge"
        st.image("gk3.png", use_container_width=True)
        st.subheader("General Knowledge")
        st.write("Enhance your general knowledge with a variety of interesting facts.")


######################################################### Function to display Quiz Page ######################################################
def show_quiz():
    st.subheader("Quiz Section")
    st.write("Test your knowledge with quizzes.")
    st.write("Question: Which is the largest planet in our solar system?")
    options = ["Mars", "Jupiter", "Saturn", "Neptune"]
    answer = st.radio("Choose your answer:", options)

    if st.button("Submit Answer"):
        if answer == "Jupiter":
            st.success("Correct Answer!")
        else:
            st.error("Wrong Answer. Try Again!")
            
######################################################### Function to display Chat Page ######################################################

API_KEY = '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'
API_URL = 'https://api.openai.com/v1/chat/completions'

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

import os
from datetime import datetime
import pandas as pd
import streamlit as st

def save_chat_history():
    # Add timestamps to the messages
    for message in st.session_state.messages:
        if "timestamp" not in message:
            message["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Convert messages to a DataFrame
    df = pd.DataFrame(st.session_state.messages)

    # File paths
    excel_file = "chat_history.xlsx"
    csv_file = "chat_history.csv"

    try:
        # Handle Excel file saving
        if os.path.exists(excel_file):
            # Read existing data
            existing_df = pd.read_excel(excel_file)
            combined_df = pd.concat([existing_df, df], ignore_index=True)
        else:
            combined_df = df

        # Save to a temporary file and then overwrite the original
        temp_excel_file = "temp_chat_history.xlsx"
        combined_df.to_excel(temp_excel_file, index=False)
        os.replace(temp_excel_file, excel_file)

        # Handle CSV file saving
        if os.path.exists(csv_file):
            # Read existing data
            existing_df = pd.read_csv(csv_file)
            combined_df = pd.concat([existing_df, df], ignore_index=True)
        else:
            combined_df = df
        combined_df.to_csv(csv_file, index=False)

        st.success("Chat history updated and saved to 'chat_history.xlsx' and 'chat_history.csv'.")
    
    except PermissionError:
        st.error("Permission denied: Ensure the file is not open or locked by another process.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")


def show_ai_chat():
    st.subheader("AI Chatbot")
    st.write("Ask questions and get AI-powered answers!")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

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

    if st.button("Save Chat History"):
        save_chat_history()

#########################################################Function to display Profile Page######################################################

def show_profile():
    st.subheader("Profile")
    st.text_input("Name", "John Doe")
    st.text_input("Email", "johndoe@example.com")
    st.text_input("Phone", "+1234567890")
    if st.button("Save Changes"):
        st.success("Profile updated successfully!")

######################################################### CURRENT AFFAIRS  ##################################################################

def fetch_current_affairs():
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="",  # Replace with your MySQL password
        database="temp"  # Replace with your database name
    )
    cursor = conn.cursor(dictionary=True)  # Use dictionary=True for dict-based results

    # SQL query to fetch data
    query = "SELECT title, summary, date_of_published, content FROM jagranjosh"
    cursor.execute(query)
    results = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    return results

import os
openai.api_key = "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"  

def generate_image(prompt):
    # Check if the image URL is already cached in the session state
    generated_image_url = st.session_state.get(prompt)
    if not generated_image_url:
        with st.spinner("Generating image..."):
            try:
                # OpenAI API call to generate an image
                response = openai.Image.create(
                    prompt=prompt,
                    n=1,
                    size="512x512"
                )
                generated_image_url = response["data"][0]["url"]
                st.session_state[prompt] = generated_image_url  # Cache the URL in session state
            except Exception as e:
                st.error("Failed to generate the image.")
                st.write(str(e))
                generated_image_url = "https://via.placeholder.com/300"  # Placeholder in case of error
    return generated_image_url

def show_current_affairs():
    st.title("Current Affairs")
    st.write("Stay updated with the latest current affairs happening around the world.")
    st.write("This page provides in-depth information on current topics.")

    # Fetch data from the database
    current_affairs_data = fetch_current_affairs()

    # Search Bar
    search_query = st.text_input("Search Current Affairs", placeholder="Type a topic or keyword...")

    # Filter Topics by Search Query
    filtered_topics = [
        topic for topic in current_affairs_data
        if search_query.lower() in topic["title"].lower()
    ] if search_query else current_affairs_data

    # Display Current Affairs
    st.subheader("Topics")
    for topic in filtered_topics:
        col1, col2 = st.columns([1, 3])  # Adjust column widths

        with col1:
            # Generate an image dynamically
            image_prompt = f"A stunning image representing {topic['title']} in general knowledge"
            image_url = generate_image(image_prompt)
            st.image(image_url, use_container_width=True)

        with col2:
            st.markdown(f"### {topic['title']}")
            st.write(f"**Published Date:** {topic['date_of_published']}")
            st.write(f"**Summary:** {topic['summary']}")

            # Expander for more details
            with st.expander("Read More"):
                st.write(topic["content"])

        # Add a buffer between each iteration
        time.sleep(1)  # Wait for 1 second before processing the next topic

    # No Results Found
    if not filtered_topics:
        st.info("No topics found matching your search.")

######################################################### GENERAL KNOWLEGDE ##################################################################

def fetch_general_knowledge():
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="",  # Replace with your MySQL password
        database="temp"  # Replace with your database name
    )
    cursor = conn.cursor(dictionary=True)  # Use dictionary=True for dict-based results

    # SQL query to fetch data sorted by id in descending order
    query = """
    SELECT id, title, date_of_published, summary, content, image_link 
    FROM gktoday 
    ORDER BY date_of_published DESC
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    return results
    

def format_content(content):
    """
    Function to format content into headings, subheadings, and paragraphs
    for improved readability.
    """
    import re

    # Split content into lines and analyze for headings, subheadings, and paragraphs
    lines = content.split("\n")
    formatted_content = []
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:  # Skip empty lines
            continue
        if re.match(r"^#{1,6}\s", stripped_line):  # Markdown headings (e.g., #, ##)
            formatted_content.append(stripped_line)
        elif stripped_line.endswith(":"):  # Treat lines ending with ":" as potential subheadings
            formatted_content.append(f"**{stripped_line}**")
        elif len(stripped_line.split()) > 15:  # Longer lines as paragraphs
            formatted_content.append(stripped_line)
        else:  # Shorter lines as potential subheadings
            formatted_content.append(f"**{stripped_line}**")

    return "\n\n".join(formatted_content)


def show_general_knowledge():
    st.title("General Knowledge")
    st.write("Enhance your general knowledge with engaging content and interesting facts.")
    st.write("Explore various topics to learn more every day.")

    # Fetch data from the database
    general_knowledge_data = fetch_general_knowledge()

    # Search Bar
    search_query = st.text_input("Search General Knowledge", placeholder="Type a topic, category, or keyword...")

    # Filter Topics by Search Query
    filtered_topics = [
        topic for topic in general_knowledge_data
        if search_query.lower() in topic["title"].lower()
    ] if search_query else general_knowledge_data

    # Display General Knowledge Topics
    st.subheader("Topics")
    for topic in filtered_topics:
        col1, col2 = st.columns([1, 3])  # Adjust column widths

        with col1:
            st.image(topic["image_link"], use_container_width=True)  # Use the image link from the database

        with col2:
            st.markdown(f"### {topic['title']}")
            st.write(f"**Published Date:** {topic['date_of_published']}")
            st.write(f"**Summary:** {topic['summary']}")

            # Expander for more details
            with st.expander("Read More"):
                try:
                    # Format the content for improved readability
                    formatted_content = format_content(topic["content"])
                    st.markdown(formatted_content, unsafe_allow_html=True)
                except Exception as e:
                    st.error("Error displaying content. Please ensure it is in the correct format.")
                    st.write(str(e))

    # No Results Found
    if not filtered_topics:
        st.info("No topics found matching your search.")




# Display the current page based on user selection
page_function_mapping = {
    "Home": show_home,
    "Quiz": show_quiz,
    "AI Chat": show_ai_chat,
    "Profile": show_profile,
    "Current Affairs": show_current_affairs,
    "General Knowledge": show_general_knowledge,
}

# Render the selected page
page_function_mapping[st.session_state.current_page]()

# Footer
st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: rgba(0, 0, 0, 0.1);
            text-align: center;
            padding: 10px;
            font-size: 14px;
            color: gray;
        }
    </style>
    <div class="footer">
        Contact us at: support@edu.ai
    </div>
    """,
    unsafe_allow_html=True,
)
