import logging
import requests
from bs4 import BeautifulSoup
import sys
import io
import mysql.connector 
from datetime import datetime

# Fix encoding for special characters
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("adda_articles.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# List of URLs to fetch articles from
urls = [
    "https://currentaffairs.adda247.com/national-current-affairs/",
    "https://currentaffairs.adda247.com/international-current-affairs/",
    "https://currentaffairs.adda247.com/appointments/",
    "https://currentaffairs.adda247.com/current-affairs-sports/",
    "https://currentaffairs.adda247.com/current-affairs-awards/",
    "https://currentaffairs.adda247.com/banking-current-affairs/"
]

# Total articles fetched
total_articles = 0
all_articles_data = []

# Database setup
def setup_database():
    conn = mysql.connector.connect(
        host="18.210.106.165",
        user="anyhost",
        password="hLE2IkBYyFqXWh[B",
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS Temp")
    conn.close()
    logging.info("Database checked/created.")

# Connect to MySQL Database and create table
def connect_to_database():
    conn = mysql.connector.connect(
         host="18.210.106.165",
        user="anyhost",
        password="hLE2IkBYyFqXWh[B",
        database="temp"
    )
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS addaConnector (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        date_of_published DATE,
        summary TEXT,
        link VARCHAR(500) UNIQUE,
        image LONGBLOB,
        image_link TEXT,
        content TEXT
    )''')
    logging.info("Connected to database and ensured table exists.")
    return conn, cursor

# Check if article already exists in the database
def article_exists(cursor, link):
    cursor.execute("SELECT 1 FROM addaConnector WHERE link = %s", (link,))
    return cursor.fetchone() is not None

# Function to format date
def format_date(date_str):
    try:
        # Convert dates like "September 14th, 2024" to "2024-09-14"
        return datetime.strptime(date_str.replace('th', '').replace('rd', '').replace('nd', '').replace('st', '').strip(), "%B %d, %Y").strftime("%Y-%m-%d")
    except Exception as e:
        logging.error(f"Date parsing error: {e}")
        return None

# Main processing
setup_database()
conn, cursor = connect_to_database()

try:
    for main_url in urls:
        try:
            logging.info(f"Fetching articles from: {main_url}")
            response = requests.get(main_url, timeout=15)
            response.encoding = 'utf-8'
            response.raise_for_status()
            logging.info("Main page fetched successfully.")

            main_soup = BeautifulSoup(response.text, 'html.parser')

            # Find all article containers
            articles = main_soup.find_all('img', {'class': 'full wp-post-image'})
            if not articles:
                logging.info("No articles found on this page.")
                continue

            logging.info(f"Found {len(articles)} articles.")
            total_articles += len(articles)

            for index, article_img in enumerate(articles):
                try:
                    logging.info(f"Processing article {index + 1}...")

                    # Extract the title from the 'alt' attribute
                    title = article_img['alt'] if 'alt' in article_img.attrs else "No title found"

                    # Extract the article link from the parent <a> tag
                    parent_a_tag = article_img.find_parent('a', href=True)
                    article_url = parent_a_tag['href'] if parent_a_tag else "No URL found"

                    if article_exists(cursor, article_url):
                        logging.info(f"Article already exists: {title} | URL: {article_url}")
                        continue

                    # Fetch the article page
                    article_response = requests.get(article_url, timeout=15)
                    article_response.encoding = 'utf-8'
                    article_response.raise_for_status()
                    article_soup = BeautifulSoup(article_response.text, 'html.parser')

                    # Extract the subheading/byline
                    subheading_tag = article_soup.find('p', {'class': 'subheading-byline'})
                    subheading = subheading_tag.text.strip() if subheading_tag else "No subheading found"

                    # Extract the published date
                    published_date_tag = article_soup.find('span', {'class': 'last-updated'})
                    if published_date_tag:
                        published_date_text = published_date_tag.text.strip()
                        if "Last updated on" in published_date_text:
                            published_date = format_date(published_date_text.replace("Last updated on", "").strip())
                        elif "Published On" in published_date_text:
                            published_date = format_date(published_date_text.replace("Published On", "").strip())
                        else:
                            published_date = format_date(published_date_text)
                    else:
                        published_date = None

                    # Extract the main content
                    content_div = article_soup.find('div', {'class': 'entry-content'})
                    main_content = []
                    if content_div:
                        for tag in content_div.find_all(['p', 'h2', 'ul', 'li']):
                            text = tag.text.strip()
                            if text.lower() == "summary of the news":
                                continue
                            if tag.name == 'li':
                                main_content.append(f"- {text}")
                            else:
                                main_content.append(text)

                    # Extract the image URL
                    image_tag = article_soup.find('img', {'alt': title})
                    image_url = image_tag['src'] if image_tag and 'src' in image_tag.attrs else "No image found"

                    # Insert into database with NULL for image
                    cursor.execute('''INSERT INTO addaConnector (title, date_of_published, summary, link, image, image_link, content)
                                      VALUES (%s, %s, %s, %s, NULL, %s, %s)''',
                                   (title, published_date, subheading, article_url, image_url, "\n".join(main_content)))
                    conn.commit()

                    logging.info(f"New article added: {title} | URL: {article_url}")

                except Exception as e:
                    logging.error(f"Error processing article {index + 1}: {e}")
                    continue

        except Exception as e:
            logging.error(f"Error fetching the page {main_url}: {e}")

finally:
    if conn.is_connected():
        conn.close()
    logging.info("Database connection closed.")

# Summary
logging.info(f"Total articles fetched: {total_articles}")
