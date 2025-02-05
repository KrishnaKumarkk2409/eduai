### `README.md`

# Fashion Vogue Web Scraping Project

## Overview

The **Fashion Vogue Web Scraping** project is designed to collect and store fashion-related articles from Vogue India’s website. The project focuses on scraping articles that cover fashion trends, extracting key information such as article titles, publication dates, summaries, content, and images. This data is then inserted into a MySQL database for storage and later retrieval. This scraper supports automatic pagination and error handling for robust performance.

This project serves as an efficient tool for gathering a large volume of articles from a dynamic website while ensuring minimal server overload by implementing randomized request delays and retry mechanisms.

## Key Features

- **Article Extraction**: Scrapes the following information from each article:
  - Title of the article
  - Date of publication
  - Article summary
  - Full article content
  - Image (main image for each article)
  - Image URL (the link to the image)
  
- **Database Integration**: Data is saved in a MySQL database for structured storage.
  - The database `temp` is created automatically if it doesn't already exist.
  - A table `fashion_vogue` is created with columns for article metadata.

- **Pagination Support**: Scrapes multiple pages by following "Next Page" links, allowing for comprehensive data extraction across a large number of articles.

- **Robust Error Handling**: Implements retries on failed requests with randomized delays between each retry attempt, making the scraper resilient to temporary network issues and server limitations.

- **Logging**: Detailed logging of events and errors is provided through the `scraping.log` file to help monitor scraper activity.

## System Requirements

- **Python Version**: 3.7+
- **MySQL**: Version 5.7 or higher for database functionality.
- **Libraries**: All required Python libraries are listed in `requirements.txt`.

## Installation and Setup

### 1. Clone the repository:
First, clone the repository to your local machine:

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create a Virtual Environment (optional but recommended):
It’s highly recommended to set up a virtual environment for Python dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install dependencies:
Install the required Python libraries listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configure the MySQL Database:
Ensure that your MySQL database is set up and accessible. Update the `db_config` dictionary in the script with the following details:
- `host`: The IP address or hostname of the MySQL server.
- `user`: The MySQL username.
- `password`: The MySQL password.
- (Optional) Update `db_name` if you want to use a database other than `temp`.

### 5. Run the Scraper:
Once everything is set up, run the scraping script:

```bash
python scrape_vogue.py
```

The script will start scraping articles from Vogue India and store them in the MySQL database. It will automatically handle pagination and continue scraping until no further pages are available.

### 6. Check Logs:
The script logs all operations, including errors, to a log file named `scraping.log`. Check this file for detailed information on the scraping process.

## Database Schema

The project uses a MySQL database to store article details. The following schema is used to store the data:

- **Database**: `temp` (automatically created if it doesn't exist).
- **Table**: `fashion_vogue`

### Table Structure:

| Column         | Data Type       | Description                                             |
|----------------|-----------------|---------------------------------------------------------|
| `id`           | INT (AUTO_INCREMENT) | Primary key, auto-incremented identifier for each article. |
| `title`        | VARCHAR(255)     | The title of the article.                               |
| `date_of_published` | DATE         | The publication date of the article (formatted as YYYY-MM-DD). |
| `summary`      | TEXT            | A brief summary of the article.                         |
| `link`         | VARCHAR(500)     | A unique URL of the article.                            |
| `image`        | LONGBLOB         | The binary data of the article's main image (if available). |
| `image_link`   | TEXT            | The URL link to the article’s main image.               |
| `content`      | TEXT            | Full content of the article.                            |

## How the Scraper Works

1. **Initial Request**: The scraper begins by sending an HTTP GET request to the Vogue India fashion trends page.
2. **Parsing HTML**: The HTML content of the page is parsed using `BeautifulSoup`.
3. **Article Extraction**: For each article found on the page, the scraper extracts:
   - Title, publication date, summary, content, image URL, and the full article URL.
4. **Retry Mechanism**: If any request fails (e.g., server issues or network timeouts), the scraper will automatically retry up to three times with a delay between attempts.
5. **Next Page**: After processing a page, the scraper looks for the "Next Page" button and continues scraping until no further pages are available.
6. **Data Insertion**: The scraper checks if an article already exists in the database. If not, it inserts the new article into the `fashion_vogue` table.
7. **Error Logging**: Any errors encountered (network issues, parsing errors, etc.) are logged for future review.

## Logging

The script logs detailed information about each action, including:

- **Page Scraping**: Successful page scrapes and the number of articles found.
- **Database Operations**: Insertion of articles and checks for existing articles.
- **Errors**: Failed attempts to fetch pages, parse data, or insert records.

All logs are stored in `scraping.log`.

## License

This project is open-source and available under the MIT License.

## Contributing

Feel free to fork the repository and submit pull requests. If you have any suggestions or improvements, open an issue in the repository, and we can discuss them.

## Contact

For any questions, you can contact the maintainer at [your-email@example.com].

## Acknowledgments

- [Vogue India](https://www.vogue.in) for the articles that are being scraped.
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing.
- [Requests](https://docs.python-requests.org/en/latest/) for making HTTP requests.
- [MySQL Connector](https://dev.mysql.com/doc/connector-python/en/) for connecting to MySQL databases in Python.

```

### `requirements.txt`

```txt
# Required Libraries for Web Scraping Project

# Requests library for making HTTP requests
requests==2.28.2

# BeautifulSoup library for parsing HTML content
beautifulsoup4==4.11.1

# MySQL Connector for connecting and interacting with MySQL databases
mysql-connector-python==8.0.31

# Libraries for handling dates and times
datetime==4.3

# Logging library is part of Python's standard library
logging==0.5.1.2

# (Optional) If you need other libraries for extra functionalities, add them here
```

---

#### Key Additions and Changes:
- **Expanded Features Section**: More detailed breakdown of functionality like database integration and error handling.
- **Detailed Database Schema**: Explanation of the database table and its structure.
- **How the Scraper Works**: Step-by-step process of the scraper, covering request handling, parsing, retries, and data insertion.
- **Installation & Setup**: Clearer and more professional steps, with extra details on setting up a virtual environment.
- **Logging**: Emphasis on the importance of the logging mechanism for debugging and monitoring.

This structure should give users a comprehensive understanding of the project and make it easier for others to contribute or run the project on their own. Let me know if you need more details or further customizations!