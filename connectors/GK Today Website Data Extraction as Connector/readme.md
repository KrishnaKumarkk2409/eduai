### README.md
# GK Today Web Scraper

## Overview
This project is a web scraper designed to extract articles, including images and content, from the GK Today website. It stores the data into a MySQL database, handling image compression before insertion.

## Features
- Scrapes articles, summaries, and full content.
- Downloads and compresses images before storing them in the database.
- Creates the database (`Temp`) and table (`gkToday`) if they do not exist.
- Avoids duplicate entries when rerun.

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
cd gk_today_scraper
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
2. The data will be stored in the `Temp` database under the `gkToday` table.

## Database Schema
**gkToday**
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
- Images are compressed to reduce size without losing quality.
- Duplicate links are skipped to prevent redundant entries.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Author
- Harsh Mankotia

