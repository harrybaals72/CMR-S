import os
import logging
import sys
from urllib.parse import urlparse, urlunparse

from arg_parser import parse_arguments
from database import create_or_update_db
from cm_api import get_posts_from_api, get_profile_name

args = parse_arguments()

# Determine the logging level
log_level = logging.DEBUG if args.verbose else getattr(logging, args.log_level)

# Configure logging
logging.basicConfig(
    level=log_level,  # Set the base logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log", encoding='utf-8'),  # Log to a file with UTF-8 encoding
        logging.StreamHandler(sys.stdout)  # Log to the console
    ]
)

# Create a logger for main.py
logger = logging.getLogger(__name__)

def main():
    print(f"Parsing arguments: {args}")

    start_url = args.url
    delay = args.delay
    db_folder = args.output
    no_scrape = args.no_scrape
    update = args.update

    parsed_url = urlparse(start_url)
    # Remove the query part by setting it to an empty string
    cleaned_url = parsed_url._replace(query='')
    
    url = urlunparse(cleaned_url)
    
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    path = cleaned_url.path
    api_url = f"{base_url}/api/v1{path}"

    logger.debug(f"Parsing URL: {start_url}")
    logger.info(f"URL: {url}")
    logger.debug(f"Base URL: {base_url}")
    logger.debug(f"Path: {path}")
    logger.debug(f"API URL: {api_url}\n")

    profile_name = get_profile_name(api_url)
    logger.info(f"Profile name: {profile_name}")

    # Create the output folder if it doesn't exist
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)
    db_path = os.path.join(db_folder, profile_name + '.db')
    
    if not no_scrape:
        # Get data from the API
        all_links = get_posts_from_api(api_url, url, 0, delay)

        if not args.soft_run:
            # Insert data into the database
            logger.info("Inserting data into the database...")
            create_or_update_db(all_links, db_path)
        else:
            logger.info("Soft run enabled. Skipping database write.")
    else:
        logger.info("Scraping disabled")
    
    if update:
        logger.info("Updating the database with local files...")
    else:
        logger.info("Database update disabled, run with -u argument to enable. Use --no-scrape to disable scraping.")

if __name__ == '__main__':
    main()