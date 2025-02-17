import os
import openai
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import mysql.connector

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed to store session data

# Get OpenAI API Key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

# Get Database credentials from .env
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Database connection function
def get_db_connection():
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    return connection

@app.route('/')
def index():
    session['chat_history'] = []  
    return render_template('dashboard/home.html')

@app.route('/home')
def home():
    return render_template('dashboard/home.html', active_page='home')

@app.route('/chat')
def ai():
    return render_template('dashboard/chat_screen.html', active_page='chat')

@app.route('/learning')
def learning():
    return render_template('dashboard/my_learning.html', active_page='learning')

@app.route('/profile')
def profile():
    return render_template('dashboard/profile.html', active_page='profile')

@app.route('/general_knowledge')
def general_knowledge():
    return render_template('dashboard/general_knowledge.html')

@app.route('/details')
def details():
    # Get the article ID from the query parameters
    news_id = request.args.get('id')
    
    if not news_id:
        return "Error: Missing article ID", 400

    # Pass the article ID to the details page
    return render_template('dashboard/details.html', news_id=news_id)


@app.route('/api/news', methods=['GET'])
def get_news():
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Query to fetch data
        query = "SELECT id, title, date_of_published, image_link, summary, content FROM addaConnector ORDER BY date_of_published DESC"
        cursor.execute(query)
        news_data = cursor.fetchall()

        # Close the connection
        cursor.close()
        conn.close()

        # Return the data as JSON
        return jsonify(news_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/news/<int:news_id>', methods=['GET'])
def get_news_details(news_id):
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Query to fetch the full news details based on the ID
        query = "SELECT * FROM addaConnector WHERE id = %s"
        cursor.execute(query, (news_id,))
        news_detail = cursor.fetchone()

        # Close the connection
        cursor.close()
        conn.close()

        if news_detail:
            return jsonify(news_detail), 200
        else:
            return jsonify({"error": "News not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    # Get JSON data from the request
    data = request.get_json()
    user_input = data.get('text', '')

    # Retrieve previous conversation history from session
    if 'chat_history' not in session:
        session['chat_history'] = []

    session['chat_history'].append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[{"role": "system", "content": "You are a helpful AI assistant."}] + session['chat_history'],
            max_tokens=150
        )

        ai_reply = response['choices'][0]['message']['content'].strip()
        session['chat_history'].append({"role": "assistant", "content": ai_reply})

    except Exception as e:
        ai_reply = f"Error: {str(e)}"

    return jsonify({'reply': ai_reply, 'chat_history': session['chat_history']})



if __name__ == '__main__':
    app.run(debug=True)
