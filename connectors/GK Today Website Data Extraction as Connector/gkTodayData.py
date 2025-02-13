import sys
from bs4 import BeautifulSoup  # type: ignore
import requests
import mysql.connector  # type: ignore
from datetime import datetime
import io
from PIL import Image
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)

# Set console to UTF-8 encoding
sys.stdout.reconfigure(encoding="utf-8")

# Database setup
def setup_database():
    conn = mysql.connector.connect(
        host="18.210.106.165",
        user="anyhost",
        password="hLE2IkBYyFqXWh[B"
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
    cursor.execute('''CREATE TABLE IF NOT EXISTS gkToday (
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

# Function to download and compress images
def download_and_compress_image(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image = Image.open(io.BytesIO(response.content))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.thumbnail((800, 800))
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG', quality=70)
        return img_byte_arr.getvalue()
    except Exception as e:
        logging.error(f"Failed to process image from {image_url}: {e}")
        return None

# Fetch article details from its page
def fetch_article_details(article_url):
    try:
        response = requests.get(article_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        content_parts = []
        for tag in soup.find_all(["p", "h4", "h3"]):
            text = tag.text.strip()
            if not any(keyword in text.lower() for keyword in [
                "leave a reply", "cancel reply", "comment", "name", "email", "Δ",
                "current affairs section", "gk mcqs section", "pdf ebooks store",
                "upsc exams", "banking exams", "category", "month"]):
                content_parts.append(text)
        full_context = "\n".join(content_parts).strip()
        image_tag = soup.find("img", class_="wp-post-image")
        image_link = image_tag["src"] if image_tag else "No image available"
        return full_context, image_link
    except Exception as e:
        logging.error(f"Error fetching article details from {article_url}: {e}")
        return "", "No image available"

# Fetch articles from a single page
def fetch_articles_from_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        articles = []
        for title in soup.find_all("h1", id="list"):
            article = {
                "title": title.a.text.strip() if title.a else "Title not found",
                "link": title.a["href"] if title.a else None
            }
            date_tag = title.find_next("span", class_="meta_date")
            article["date"] = datetime.strptime(date_tag.text.strip(), "%B %d, %Y").date() if date_tag else None
            
            seo_tag = title.find_next("p")
            article["seo"] = seo_tag.text.strip() if seo_tag else "Snippet not found"
            if article["link"]:
                article["context"], article["image_link"] = fetch_article_details(article["link"])
                article["image"] = download_and_compress_image(article["image_link"]) if article["image_link"] != "No image available" else None
            else:
                article["context"] = "Full context not available"
                article["image"] = None
                article["image_link"] = "No image available"
            articles.append(article)
        return articles
    except Exception as e:
        logging.error(f"Error fetching articles from page {url}: {e}")
        return []

# Main scraping function
def scrape(start_url, conn, cursor, max_pages=50):
    # Fetch all existing links from the database
    cursor.execute("SELECT link FROM gkToday")
    existing_links = set(row[0] for row in cursor.fetchall())
    logging.info(f"Loaded {len(existing_links)} existing article links from the database.")

    base_url = "https://www.gktoday.in/page/{}/"
    for page_number in range(1, max_pages + 1):
        current_url = base_url.format(page_number)
        logging.info(f"Scraping page {page_number}: {current_url}")
        articles = fetch_articles_from_page(current_url)
        if not articles:
            logging.warning(f"No articles found on page {page_number}. Stopping.")
            break

        for article in articles:
            # Check if the article link already exists in the database
            if article["link"] in existing_links:
                logging.warning(f"Duplicate article found: {article['title']}. Terminating the program.")
                sys.exit(0)  # Terminate the program on duplicate

            # Add the new article to the database
            cursor.execute('''INSERT INTO gkToday (title, date_of_published, summary, link, image, image_link, content) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s)''', 
                           (article["title"], article["date"], article["seo"], article["link"], article["image"], article["image_link"], article["context"]))
            conn.commit()
            logging.info(f"Added new article: {article['title']}")

            # Add the link to the set of existing links
            existing_links.add(article["link"])

# Entry point
if __name__ == "__main__":
    try:
        setup_database()
        conn, cursor = connect_to_database()
        start_url = "https://www.gktoday.in/category/current-affairs/"
        scrape(start_url, conn, cursor, max_pages=50)  # Scrape up to 50 pages
    except Exception as e:
        logging.error(f"Critical error: {e}")
    finally:
        cursor.close()
        conn.close()
        logging.info("Scraping completed and database connection closed.")
