import requests
from bs4 import BeautifulSoup  # type: ignore
import sys
from multiprocessing import Pool
import re
import mysql.connector  # type: ignore
from datetime import datetime
import time
import logging

# Ensure proper encoding for output
sys.stdout.reconfigure(encoding='utf-8')

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(), logging.FileHandler("scraping.log")])

# Create database if not exists
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS temp")
cursor.close()
conn.close()

# URLs to scrape
urls = [
    "https://www.jagranjosh.com/current-affairs/national-india-1283851987-catlistshow-1",
    "https://www.jagranjosh.com/current-affairs/international-world-1283850903-catlistshow-1",
    "https://www.jagranjosh.com/current-affairs/economy-1284037727-catlistshow-1",
    "https://www.jagranjosh.com/current-affairs/corporate-1284120896-catlistshow-1"
]

# Function to clean up the content
def clean_content(text):
    text = re.sub(r'\+ More \+', '', text)
    text = re.sub(r'ALSO READ:.*', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to fetch detailed article data
def fetch_article_content(article_url):
    try:
        response = requests.get(article_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        summary = soup.find('h2', class_='Details_SortSummery__77Dsv')
        summary_text = summary.get_text(strip=True) if summary else 'No summary available'

        content = []
        for element in soup.find_all(['span', 'strong']):
            text = element.get_text(strip=True)
            if text:
                content.append(text)

        content_text = ' '.join(content) if content else 'No content available'
        content_text = clean_content(content_text)
        return summary_text, content_text
    except Exception as e:
        logging.error(f"Error fetching content from {article_url}: {e}")
        return 'Failed to fetch article', ''

# Function to fetch articles from a given URL
def fetch_articles(url):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="temp"
    )
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS jagranJosh (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        date_of_published DATE,
        summary TEXT,
        link TEXT UNIQUE,
        image LONGBLOB,
        image_link TEXT,
        content TEXT
    )''')

    response = requests.get(url)
    articles = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        for item in soup.find_all('h3'):
            link_tag = item.find('a')
            if link_tag:
                title = link_tag.text.strip()
                link = link_tag['href']
                pub_date = item.find_next_sibling('div', class_='Listing_PubDate__LvHzJ')
                date_time = pub_date.text.strip() if pub_date else 'No date available'
                date_only = re.sub(r', \d{2}:\d{2} IST', '', date_time)

                img_tag = item.find_next('img')
                img_url = img_tag['src'] if img_tag else 'No image available'

                summary, article_content = fetch_article_content(link)

                retries = 3
                while retries > 0:
                    try:
                        cursor.execute('SELECT id FROM jagranJosh WHERE link = %s', (link,))
                        result = cursor.fetchone()
                        if not result:
                            cursor.execute('''INSERT INTO jagranJosh (title, date_of_published, summary, link, image, image_link, content) 
                                              VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                                           (title, datetime.strptime(date_only, "%b %d, %Y"), summary, link, None, img_url, article_content))
                            conn.commit()
                            logging.info(f"Inserted new article: {title}")
                        else:
                            logging.info(f"Article already exists: {title}")
                        break
                    except mysql.connector.errors.InternalError as e:
                        if 'Deadlock' in str(e):
                            retries -= 1
                            time.sleep(1)
                        else:
                            raise e

                articles.append({
                    'title': title,
                    'link': link,
                    'date_time': date_only,
                    'image_url': img_url,
                    'summary': summary,
                    'content': article_content
                })

    else:
        logging.error(f"Failed to retrieve the webpage: {url}. Status code: {response.status_code}")

    cursor.close()
    conn.close()
    return articles

# Main function to use multiprocessing
def main():
    with Pool(processes=2) as pool:
        pool.map(fetch_articles, urls)

    logging.info("Data fetching and insertion completed.")

if __name__ == "__main__":
    main()
