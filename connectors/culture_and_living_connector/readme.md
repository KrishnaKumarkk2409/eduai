# Culture and Living Web Scraper

## Overview

This Python project is designed to scrape articles from the **Culture and Living** section of the **Vogue India** website (https://www.vogue.in/culture-and-living). It extracts various article details such as titles, publication dates, summaries, content, and images. The data is then stored in a MySQL database for future reference. This script handles retry logic for fetching web pages, ensures that the database is properly set up, and checks for existing articles to prevent duplicates.

## Features

- **Scrape Articles**: Extracts title, publication date, summary, full content, and image data for each article.
- **Database Integration**: Stores scraped data in a MySQL database, including text and binary data (for images).
- **Error Handling**: Implements retries for network issues and skips already existing articles in the database.
- **Next Page Navigation**: Automatically follows pagination to scrape multiple pages of articles.
- **Logging**: Detailed logging for each step of the scraping process, including successful actions and errors.

## Technologies

- **Python**: The script is written in Python, utilizing libraries like `requests`, `BeautifulSoup`, and `mysql-connector`.
- **MySQL**: Data is stored in a MySQL database, ensuring efficient storage and retrieval of scraped articles.
- **Requests Library**: Used for making HTTP requests to fetch pages and articles.
- **BeautifulSoup**: Parses HTML content and extracts relevant data.
- **Logging**: Built-in Python logging to track the execution process.
- **DateTime**: For handling and formatting dates to store in the database.

## Requirements

Before running the script, ensure the following Python packages are installed:

- requests
- beautifulsoup4
- mysql-connector-python

You can install the required packages using `pip`:

```bash
pip install requests beautifulsoup4 mysql-connector-python
```

You also need a running MySQL database instance. The script is set to connect to a MySQL database using the credentials:

- **Host**: `18.210.106.165`
- **User**: `anyhost`
- **Password**: `hLE2IkBYyFqXWh[B`

### MySQL Setup

1. Create a MySQL instance if you haven't already, and ensure the required credentials are configured.
2. The script will automatically create the database `temp` if it doesn't already exist and switch to it.

## Setup Instructions

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/culture-and-living-web-scraper.git
cd culture-and-living-web-scraper
```

### Step 2: Configure the Database

Ensure you have access to a MySQL database, either locally or remotely. Update the `db_config` in the script with your MySQL database connection details:

```python
db_config = {
    'host': 'your_host',
    'user': 'your_user',
    'password': 'your_password'
}
```

### Step 3: Run the Scraper

To run the scraper, execute the Python script:

```bash
python culture_and_living_connecotr.py
```

This will start scraping articles from the **Culture and Living** section of **Vogue India**, logging the output, and saving the data to the database.

### Step 4: Check Database

Once the script has completed running, you can check the `culture_and_living_vogue` table in your MySQL database to see the scraped data.

## Code Explanation

### Key Functions

1. **`create_db_connection()`**:
    - Establishes a connection to the MySQL database using the provided credentials. Returns the connection object if successful.

2. **`ensure_database_exists()`**:
    - Ensures that the `temp` database exists. If not, it will be created. The script will then switch to this database.

3. **`create_table()`**:
    - Creates the `culture_and_living_vogue` table to store article details if it doesn't already exist.

4. **`article_exists()`**:
    - Checks whether an article already exists in the database based on the article's unique link. Prevents the insertion of duplicate entries.

5. **`insert_article()`**:
    - Inserts a new article into the database, including title, publication date, summary, content, image URL, and image data (binary).

6. **`fetch_with_retries()`**:
    - A helper function to make HTTP requests with retries. It handles common errors (e.g., 502 Bad Gateway) and waits for a specified delay before retrying.

7. **`scrape_articles()`**:
    - The main function that scrapes the articles from the web pages. It extracts article data, checks if the article exists in the database, and stores new articles.

### Scraping Process

- **Fetching the Main Page**: The script starts by scraping the main Culture and Living page.
- **Extracting Article Data**: It then extracts details like title, publication date, and content from each article.
- **Downloading Images**: The script also downloads images for each article, storing them as binary data in the database.
- **Pagination**: After processing the articles on the current page, the script finds the "Next Page" button and continues scraping until no further pages are available.

### Logging

The script logs all important actions and errors in a `culture_and_living_vogue_data.log` file. This includes:

- Page scraping attempts and successes.
- Article details, such as the title and publication date.
- Any errors encountered, such as failed connections or missing data.

### Handling Errors

The scraper is designed to handle various types of errors:

- **Network Errors**: If the script fails to fetch a page (e.g., due to a network timeout or server issue), it will retry up to a specified number of times.
- **Duplicate Entries**: Before inserting a new article into the database, the script checks if the article already exists based on its unique link.

### Rate Limiting

The scraper adds a random delay between requests to avoid overwhelming the target website's server, which helps prevent your IP from being blocked.

## Database Schema

The scraper stores the scraped article details in a MySQL database. Below is the schema of the table `culture_and_living_vogue` where the data is stored:

### Table Name: `culture_and_living_vogue`

| Column Name     | Data Type       | Description                                                                                                                                       |
|-----------------|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| `id`            | `INT AUTO_INCREMENT` | **Primary Key**. A unique identifier for each article. Automatically increments with each new article insertion.                                |
| `title`         | `VARCHAR(255)`   | The title of the article. It is stored as a string of up to 255 characters.                                                                       |
| `date_of_published` | `DATE`        | The publication date of the article in `YYYY-MM-DD` format.                                                                                        |
| `summary`       | `TEXT`           | A brief summary of the article content, stored as text.                                                                                           |
| `link`          | `VARCHAR(500)`   | The URL of the article. It is stored as a string of up to 500 characters. This field is **unique** for each article to avoid duplicates.         |
| `image`         | `LONGBLOB`       | The binary data of the image associated with the article, stored as a long binary object (this can be an image file like PNG, JPEG, etc.).       |
| `image_link`    | `TEXT`           | The URL of the image associated with the article. This is useful for downloading the image.                                                      |
| `content`       | `TEXT`           | The full content of the article, extracted from the article page. It is stored as text.                                                          |

### SQL Schema for Creating the Table

Here is the SQL query to create the `culture_and_living_vogue` table in MySQL:

```sql
CREATE TABLE IF NOT EXISTS culture_and_living_vogue (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique identifier for each article
    title VARCHAR(255),  -- Title of the article
    date_of_published DATE,  -- Date when the article was published
    summary TEXT,  -- Summary of the article
    link VARCHAR(500) UNIQUE,  -- Unique URL for the article (used to prevent duplicates)
    image LONGBLOB,  -- Image binary data (optional)
    image_link TEXT,  -- URL of the image (optional)
    content TEXT  -- Full content of the article
);
```

### Table Description

- **`id`**: This is an auto-incrementing field that uniquely identifies each article in the table. The value of `id` will be automatically generated when a new article is inserted.
  
- **`title`**: This field stores the title of the article, which is a string of up to 255 characters.

- **`date_of_published`**: This stores the publication date of the article in the format `YYYY-MM-DD`. This ensures that the data is consistent and in a recognizable date format.

- **`summary`**: This stores the summary of the article. It's a text field, so it can accommodate longer summaries.

- **`link`**: This field stores the unique URL of the article. This is critical for ensuring that no duplicate articles are stored in the database. This field is marked as `UNIQUE`, so if an article with the same URL is scraped again, it will not be inserted.

- **`image`**: This field stores the image associated with the article as binary data. It's stored as a `LONGBLOB`, which can accommodate large binary data like image files.

- **`image_link`**: This field stores the URL of the image associated with the article. This allows you to retrieve the image later or verify the image URL.

- **`content`**: This field stores the full content of the article, extracted from the page. It's stored as `TEXT`, which allows it to accommodate large amounts of text.

### ER Diagram (Optional)

If you'd like to visualize the structure, here is a simple representation of the `culture_and_living_vogue` table schema:

```
+----------------------+      +-----------------------+
| culture_and_living_vogue |      | Column Name          |
+----------------------+      +-----------------------+
| id                   | <---- | INT AUTO_INCREMENT   |
| title                |      | VARCHAR(255)         |
| date_of_published    |      | DATE                 |
| summary              |      | TEXT                 |
| link                 |      | VARCHAR(500) UNIQUE  |
| image                |      | LONGBLOB             |
| image_link           |      | TEXT                 |
| content              |      | TEXT                 |
+----------------------+      +-----------------------+
```

## Conclusion

This project provides a reliable and efficient way to scrape and store articles from the Culture and Living section of Vogue India. It is designed to be robust with error handling, retries, and pagination support. With the data stored in a MySQL database, you can easily query and analyze the articles in the future.

Feel free to modify and extend the script to suit your needs. Contributions and improvements are welcome!

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

For further inquiries or support, please contact [harshmankotia.encap@gmail.com,harsh.mankotia@encaptechno.com].
```

