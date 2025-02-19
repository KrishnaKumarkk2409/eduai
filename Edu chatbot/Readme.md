# AI-Powered SQL Chatbot

## Overview
This project is an AI-powered SQL chatbot built with Streamlit, OpenAI API, and MySQL. It allows users to input natural language queries, which are processed using an AI model to generate SQL queries dynamically. The chatbot then retrieves relevant information from the MySQL database and presents it in a structured format.

## Features
- **Natural Language Processing**: Uses OpenAI's fine-tuned model to understand user queries.
- **Dynamic SQL Query Generation**: AI automatically constructs SQL queries based on user input.
- **Database Search**: Searches across multiple tables dynamically.
- **Interactive UI**: Built with Streamlit for a user-friendly experience.
- **Secure Database Connection**: Uses `.env` variables to protect credentials.

## Technologies Used
- Python
- Streamlit
- OpenAI API
- MySQL
- dotenv (for environment variable management)

## Installation
### Prerequisites
- Python 3.7+
- MySQL Database
- OpenAI API Key

### Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repository.git
   cd your-repository
   ```
2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up Environment Variables**
   Create a `.env` file and add the following variables:
   ```env
   MYSQL_HOST=your_mysql_host
   MYSQL_USER=your_mysql_user
   MYSQL_PASSWORD=your_mysql_password
   MYSQL_DEFAULT_DATABASE=your_database_name
   OPENAI_API_KEY=your_openai_api_key
   FINE_TUNED_MODEL=your_fine_tuned_model_id
   ```
5. **Run the Streamlit App**
   ```bash
   streamlit run new.py
   ```

## File Descriptions
- **`new.py`**: Main Streamlit application that provides a UI for user queries, generates SQL queries using OpenAI, and displays results.
- **`sql.py`**: Backend script that handles database connections, retrieves tables/columns, and executes SQL queries.

## How It Works
1. The user enters a natural language query in the Streamlit interface.
2. The AI extracts keywords and dynamically generates a SQL query.
3. The query is executed against the MySQL database.
4. The results are displayed in a structured format.

## API Endpoints (Internal)
- **`generate_sql_query(user_query)`**: Converts natural language to SQL.
- **`execute_query(user_query)`**: Runs the generated SQL query and retrieves results.
- **`get_all_tables()`**: Fetches all table names in the database.
- **`get_table_columns(tables)`**: Retrieves column names for tables dynamically.

## Future Enhancements
- Implement more advanced AI fine-tuning for complex queries.
- Add user authentication and role-based access.
- Extend support for additional databases (PostgreSQL, SQLite).
- Improve error handling and SQL injection protection.

## License
This project is licensed under the MIT License.

## Contributing
Pull requests are welcome! Open an issue for major changes before submitting a PR.

