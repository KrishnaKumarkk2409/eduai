# README

## Overview
This script scrapes current affairs articles from specified URLs, processes the data, and saves it into a MySQL database. It logs all actions to both the console and a log file (`adda_articles.log`) for transparency and debugging.

## Features
- Fetches articles from multiple URLs.
- Extracts relevant details, such as title, date, summary, and content.
- Avoids duplicate entries by checking the database for existing URLs.
- Logs actions and errors in detail.
- Saves extracted articles in a MySQL database.

## Requirements
- Python 3.8 or later
- MySQL database
- Required Python libraries (see `requirements.txt`)

## Installation
1. Clone the repository or copy the script files.
2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up a MySQL database and ensure the credentials in the script are correct.
4. Run the script:
   ```bash
   python adda_articles_scraper.py
   ```

## Configuration
- **Database Connection:**
  Modify the `connect_to_database()` function to update your MySQL credentials.
- **Logging:**
  Logs are saved in `adda_articles.log`. Adjust the logging setup in the script if needed.
- **URLs:**
  Update the `urls` list with the sources you want to scrape.

## Logging
- Log file: `adda_articles.log`
- Console and log file include:
  - Articles fetched
  - New articles added
  - Duplicate articles skipped
  - Errors encountered

## Notes
- Ensure your MySQL server is running before executing the script.
- The script creates a database and table automatically if they do not exist.

---

