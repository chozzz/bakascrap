# Mangascrapers

Scrape mangas out there! Built by [scrapy](https://github.com/scrapy/scrapy)

## Pre-installation
1. Install python3 and mysql
2. Configure mysql with a new database named `mangascrapers` (This can be configured from `pipelines.py`).

## Installation
1. Clone the repository
2. CWD to the repo, and run virtualenv - `python3 -m venv .`
3. Run `pip install -r requirements.txt`
4. Verify installation sucessful (by listing all available crawlers with `scrapy list`)
5. Run your crawler `scrapy crawl <crawler>`