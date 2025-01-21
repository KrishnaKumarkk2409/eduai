from flask import Flask, render_template
import mysql.connector # type: ignore
from PIL import Image
import io
import base64

app = Flask(__name__)

# Connect to MySQL Database
def get_articles():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Temp"
    )
    cursor = conn.cursor()

    # Fetch all data from gkToday table
    cursor.execute('''SELECT title, date_of_published, summary, image, image_link, content FROM gkToday''')
    articles = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    # Process articles
    processed_articles = []
    for article in articles:
        title, date, summary, image_data, image_link, content = article

        # Debug: Check image data length
        print(f"Title: {title}, Image Data Length: {len(image_data) if image_data else 0}")

        # Convert binary image data to Base64 for rendering
        if isinstance(image_data, bytes) and len(image_data) > 0:
            try:
                img_base64 = base64.b64encode(image_data).decode('utf-8')
                mime_type = "jpeg"  # Assuming all images are JPEG for now
            except Exception as e:
                print(f"Error processing image for {title}: {e}")
                img_base64 = None
        else:
            img_base64 = None

        processed_articles.append({
            'title': title,
            'date': date,
            'summary': summary,
            'image': img_base64,
            'mime_type': mime_type if img_base64 else None,
            'image_link': image_link,
            'content': content
        })
    
    return processed_articles

@app.route('/')
def index():
    articles = get_articles()
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
