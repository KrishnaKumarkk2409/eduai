### README.md
# Jagran Josh Web Scraper

## Overview
This project is a web scraper designed to extract articles, including summaries and content, from the Jagran Josh Current Affairs website. It stores the data into a MySQL database, ensuring no duplicate entries and handling concurrency issues.

## Features
- Scrapes articles, summaries, and full content.
- Handles database creation (`temp`) and table creation (`jagranJosh`) automatically.
- Avoids duplicate entries when rerun.
- Implements retry mechanism to handle database deadlocks.

## Requirements
- Python 3.10 or higher
- MySQL Server installed (XAMPP recommended)
- Required Python libraries listed in `requirements.txt`.

## Installation
1. Clone the repository.
```
git clone <repository-url>
```

2. Navigate to the project directory.
```
cd jagran_josh_scraper
```

3. Install dependencies.
```
pip install -r requirements.txt
```

4. Setup MySQL:
- Create a user with username `root` and password `` (empty).
- Allow access to the database.

## Usage
1. Run the script:
```
python scraper.py
```
2. The data will be stored in the `temp` database under the `jagranJosh` table.

## Database Schema
**jagranJosh**
| Column              | Data Type     |
|---------------------|---------------|
| id                  | INT (Primary) |
| title               | VARCHAR(255)  |
| date_of_published   | DATE          |
| summary             | TEXT          |
| link                | TEXT UNIQUE   |
| image               | LONGBLOB      |
| image_link          | TEXT          |
| content             | TEXT          |

## Notes
- The script checks if the database and table exist before creating them.
- Duplicate links are skipped to prevent redundant entries.
- Implements retry logic to handle database deadlocks.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Author
- Harsh Mankotia

