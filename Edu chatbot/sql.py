import openai
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve credentials from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DEFAULT_DATABASE")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
FINE_TUNED_MODEL = os.getenv("FINE_TUNED_MODEL")  # Load fine-tuned model ID

# Connect to MySQL Database
def connect_db():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

# Get all tables in the database dynamically
def get_all_tables():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES;")
    tables = [table[0] for table in cursor.fetchall()]
    connection.close()
    return tables

# Get all columns dynamically
def get_table_columns(tables):
    connection = connect_db()
    cursor = connection.cursor()
    table_columns = {}

    for table in tables:
        cursor.execute(f"DESCRIBE {table};")
        columns = [column[0] for column in cursor.fetchall()]
        table_columns[table] = columns

    connection.close()
    return table_columns

# Generate SQL query dynamically using fine-tuned OpenAI model
def generate_sql_query(user_query):
    openai.api_key = OPENAI_API_KEY

    # Call the fine-tuned model stored in .env
    response = openai.ChatCompletion.create(
        model=FINE_TUNED_MODEL,  # Fetch model from .env
        messages=[
            {"role": "system", "content": "Generate SQL queries dynamically based on user input."},
            {"role": "user", "content": user_query}
        ]
    )
    
    return response["choices"][0]["message"]["content"]

# Execute SQL Query and fetch results
def execute_sql_query(sql_query):
    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        connection.close()

        return results if results else "No results found."
    
    except Exception as e:
        return f"Error executing query: {str(e)}"

# Main chatbot function
def chatbot_query(user_input):
    sql_query = generate_sql_query(user_input)
    print(f"\nGenerated SQL Query:\n{sql_query}")

    result = execute_sql_query(sql_query)
    return result

# Run chatbot
if __name__ == "__main__":
    user_input = input("Enter your question: ")
    print("Processing query...")

    # Execute SQL and Fetch Results
    result = chatbot_query(user_input)

    print("\nChatbot Response:")
    print(result)
