import streamlit as st
import openai
import mysql.connector
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve environment variables
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DEFAULT_DATABASE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FINE_TUNED_MODEL = os.getenv("FINE_TUNED_MODEL")

# Streamlit Page Configuration
st.set_page_config(page_title="AI-Powered SQL Chatbot", layout="wide")

# Title
st.title("🔍 AI-Powered SQL Chatbot")
st.write("Enter a natural language query, and the chatbot will search across all tables in the MySQL database.")

# Connect to MySQL Database
def connect_db():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

# Get all tables dynamically
def get_all_tables():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES;")
    tables = [table[0] for table in cursor.fetchall()]
    connection.close()
    return tables

# Extract keywords using fine-tuned OpenAI model
def extract_keywords(user_query):
    openai.api_key = OPENAI_API_KEY

    response = openai.ChatCompletion.create(
        model=FINE_TUNED_MODEL,
        messages=[
            {"role": "system", "content": "Extract the most relevant keywords for search from the given user query."},
            {"role": "user", "content": user_query}
        ]
    )
    
    keywords = response["choices"][0]["message"]["content"]
    return re.findall(r'\b\w+\b', keywords)  # Extract words from response

# Generate SQL query dynamically
def generate_sql_query(user_query):
    tables = get_all_tables()
    keywords = extract_keywords(user_query)

    if not tables:
        return "No tables found in the database."

    if not keywords:
        return "No relevant keywords found in the query."

    search_conditions = []
    for keyword in keywords:
        search_conditions.append(
            f"title LIKE '%{keyword}%' OR summary LIKE '%{keyword}%' OR content LIKE '%{keyword}%'"
        )

    search_condition = " OR ".join(search_conditions)

    # Construct a UNION ALL query to search in all tables
    union_queries = []
    for table in tables:
        union_queries.append(f"SELECT *, '{table}' AS source_table FROM {table} WHERE {search_condition}")

    final_query = " UNION ALL ".join(union_queries) + " ORDER BY date_of_published DESC LIMIT 100;"
    return final_query

# Execute SQL Query and fetch results
def execute_query(user_query):
    sql_query = generate_sql_query(user_query)

    if "No tables found" in sql_query or "No relevant keywords" in sql_query:
        return sql_query

    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute(sql_query)
        columns = [desc[0] for desc in cursor.description]  # Fetch column names
        results = cursor.fetchall()
        connection.close()

        return results, columns if results else ("No results found.", [])
    
    except Exception as e:
        return f"Error executing query: {str(e)}", []

# Streamlit UI
user_input = st.text_input("Enter your query:", "")

if st.button("Search"):
    if user_input.strip() == "":
        st.warning("Please enter a query before searching.")
    else:
        st.write("🔎 **Processing your query...**")

        # Generate and show the SQL query
        sql_query = generate_sql_query(user_input)
        st.write("### Generated SQL Query:")
        st.code(sql_query, language='sql')  # Display the generated SQL query in code block

        # Fetch and display results
        results, columns = execute_query(user_input)

        if isinstance(results, str):  # Error message or no results
            st.error(results)
        else:
            st.success("✅ Query executed successfully!")
            if results:
                st.write(f"Displaying {len(results)} results:")
                import pandas as pd
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)  # Display results in a table format
            else:
                st.warning("No matching results found.")
