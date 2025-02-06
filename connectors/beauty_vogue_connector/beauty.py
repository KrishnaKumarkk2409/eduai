import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import mysql.connector
from mysql.connector import Error
import logging
import time
import random
from datetime import datetime

# Set the output encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Configure logging
logging.basicConfig(filename='beauty_scrapping.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database connection details
db_config = {
    'host': '18.210.106.165',
    'user': 'anyhost',
    'password': 'hLE2IkBYyFqXWh[B'
}

# Function to create a connection to the database
def create_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        logging.error(f"Error connecting to MySQL: {e}")
        return None

# Function to check if the database exists, and create it if not
def ensure_database_exists(connection):
    try:
        cursor = connection.cursor()
        # Check if the 'temp' database exists
        cursor.execute("SHOW DATABASES LIKE 'temp';")
        result = cursor.fetchone()
        if not result:
            # Create the 'temp' database if it doesn't exist
            cursor.execute("CREATE DATABASE temp;")
            logging.info("Database 'temp' created.")
        else:
            logging.info("Database 'temp' already exists.")
        
        # Switch to the 'temp' database
        cursor.execute("USE temp;")
        logging.info("Switched to database 'temp'.")
    except Error as e:
        logging.error(f"Error ensuring database exists: {e}")

# Function to create the table if it doesn't exist
def create_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS beauty_vogue (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            date_of_published DATE,
            summary TEXT,
            link VARCHAR(500) UNIQUE,
            image LONGBLOB,
            image_link TEXT,
            content TEXT
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        logging.info("Table 'beauty_vogue' created or already exists.")
    except Error as e:
        logging.error(f"Error creating table: {e}")

# Function to check if an article already exists in the database
def article_exists(connection, article_link):
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM beauty_vogue WHERE link = %s"
        cursor.execute(query, (article_link,))
        result = cursor.fetchone()
        return result[0] > 0
    except Error as e:
        logging.error(f"Error checking article existence: {e}")
        return False

# Function to insert a new article into the database
def insert_article(connection, title, date_of_published, summary, link, image, image_link, content):
    try:
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO beauty_vogue (title, date_of_published, summary, link, image, image_link, content)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (title, date_of_published, summary, link, image, image_link, content))
        connection.commit()
        logging.info(f"Inserted article: {title}")
    except Error as e:
        logging.error(f"Error inserting article: {e}")

# Function to send a GET request with retries
def fetch_with_retries(url, max_retries=3, delay=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response
            elif response.status_code == 502:
                logging.warning(f"Attempt {attempt + 1}: Received 502 Bad Gateway for URL: {url}. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logging.error(f"Failed to retrieve the webpage. Status code: {response.status_code}, URL: {url}")
                return None
        except Exception as e:
            logging.error(f"Error during request: {e}")
            if attempt < max_retries - 1:
                logging.warning(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logging.error("Max retries reached. Skipping this page.")
                return None
    return None

# Base URL and initial page
base_url = "https://www.vogue.in"
current_page = f"{base_url}/beauty"

# Initialize the counter for total articles
total_articles = 0
consecutive_errors = 0
max_consecutive_errors = 5

# Connect to the database
connection = create_db_connection()
if connection is None:
    print("Failed to connect to the database. Exiting.")
    logging.error("Failed to connect to the database. Exiting.")
    exit()
else:
    print("Successfully connected to the database.")

# Ensure the 'temp' database exists and switch to it
ensure_database_exists(connection)
print("Database 'temp' ensured and switched to.")

# Create the table if it doesn't exist
create_table(connection)
print("Table 'beauty_vogue' ensured.")

while current_page:
    print(f"Scraping page: {current_page}")  # Debugging: Print the current page URL
    
    # Add a random delay between requests to avoid overwhelming the server
    time.sleep(random.uniform(1, 5))
    
    # Fetch the page with retries
    response = fetch_with_retries(current_page)
    if not response:
        consecutive_errors += 1
        if consecutive_errors >= max_consecutive_errors:
            logging.error("Too many consecutive errors. Stopping the scraper.")
            break
        continue  # Skip to the next page
    else:
        consecutive_errors = 0  # Reset the counter on successful request
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    logging.info(f"Parsed HTML title: {soup.title.string if soup.title else 'No title found'}")
    
    # Find all the article containers
    articles = soup.find_all('div', class_='summary-item__content')
    logging.info(f"Found {len(articles)} articles on the page.")
    
    if not articles:
        logging.warning(f"No articles found on page: {current_page}")
        # Continue to the next page instead of breaking
        current_page = None
        continue
    
    # Iterate over each article container
    for article in articles:
        # Extract the headline
        headline = article.find('h2', class_='summary-item__hed')
        title = headline.get_text(strip=True) if headline else "Title not found"
        
        # Extract the publication date
        date = article.find('time', class_='summary-item__publish-date')
        raw_date = date.get_text(strip=True) if date else "Date not found"
        
        # Convert the date to YYYY-MM-DD format
        try:
            parsed_date = datetime.strptime(raw_date, "%d %B %Y").strftime("%Y-%m-%d")
        except ValueError:
            parsed_date = "Date not found"
            logging.warning(f"Failed to parse date: {raw_date}")
        
        # Extract the article URL
        link_tag = article.find('a', class_='summary-item__hed-link')
        full_url = urljoin(base_url, link_tag['href']) if link_tag and 'href' in link_tag.attrs else "URL not found"
        
        # Extract the image URL
        image_tag = article.find('img', class_='responsive-image__image')
        if image_tag and 'src' in image_tag.attrs:
            # Extract the full-resolution image URL
            image_url = image_tag['src']
            # Ensure the URL is absolute (not relative)
            if not image_url.startswith('http'):
                image_url = urljoin(base_url, image_url)
        else:
            # Fallback: Try finding the first image in the entire page that matches the article title
            fallback_image_tag = soup.find('img', alt=lambda x: x and title.lower() in x.lower())
            if fallback_image_tag and 'src' in fallback_image_tag.attrs:
                image_url = fallback_image_tag['src']
                if not image_url.startswith('http'):
                    image_url = urljoin(base_url, image_url)
            else:
                # Final fallback: Use the first image on the page if no match is found
                fallback_image_tag = soup.find('img', class_='responsive-image__image')
                if fallback_image_tag and 'src' in fallback_image_tag.attrs:
                    image_url = fallback_image_tag['src']
                    if not image_url.startswith('http'):
                        image_url = urljoin(base_url, image_url)
                else:
                    image_url = "Image URL not found"
        
        # Fetch the individual article page
        article_response = fetch_with_retries(full_url)
        if not article_response:
            logging.error(f"Failed to retrieve the article: {full_url}")
            continue
        
        # Parse the article's page HTML
        article_soup = BeautifulSoup(article_response.text, 'html.parser')
        
        # Extract the summary
        summary_div = article_soup.find('div', class_='SplitScreenContentHeaderDek-emptdL')
        summary = summary_div.get_text(strip=True) if summary_div else "Summary not found"
        
        # Extract the article content
        content_div = article_soup.find('div', class_='body__inner-container')
        content = content_div.get_text(strip=True) if content_div else "Content not found"
        
        # Display the summary and content in the console
        print(f"Title: {title}")
        print(f"Publish Date: {parsed_date}")
        print(f"URL: {full_url}")
        print(f"Image URL: {image_url}")
        print(f"Summary: {summary}")
        print(f"Content: {content[:200]}...")  # Show only the first 200 characters of the content
        print(f"-" * 40)
        
        # Download the image as binary data (optional)
        image_binary = None
        try:
            if image_url != "Image URL not found":
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    image_binary = image_response.content
        except Exception as e:
            logging.error(f"Error downloading image: {e}")
        
        # Check if the article already exists in the database
        if article_exists(connection, full_url):
            logging.info(f"Article already exists: {title}")
            continue
        
        # Insert the article into the database
        insert_article(
            connection,
            title,
            parsed_date,
            summary,
            full_url,
            image_binary,
            image_url,
            content
        )
        
        # Increment the article counter
        total_articles += 1
    
    # Find the "Next Page" button
    next_page_button = soup.find('a', class_='BaseButton-bLlsy ButtonWrapper-xCepQ cRxydS giwzDJ button button--primary', string='Next Page')
    if next_page_button and 'href' in next_page_button.attrs:
        next_page_url = next_page_button['href']
        # Construct the full URL for the next page
        current_page = urljoin(current_page, next_page_url)
        logging.info(f"Found next page: {current_page}")
    else:
        logging.info("No more pages to scrape.")
        current_page = None  # Exit the loop when there's no next page


# Close the database connection
if connection.is_connected():
    connection.close()

# Print the total number of articles scraped
print(f"Total number of articles scraped: {total_articles}")