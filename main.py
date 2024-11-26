import os
import logging
import sys
from urllib.parse import urlparse, urlunparse

from log_config import configure_logging
from arg_parser import parse_arguments
from database import create_or_update_db
from cm_api import get_posts_from_api, get_profile_name
from fileMatch import update_downloaded_status
from generate import get_undownloaded_posts

def main():
    args = parse_arguments()

    print(f"Parsing arguments: {args}")

    db_folder = args.db_path
    no_scrape = args.no_scrape
    write = args.write
    file_path = args.file_path
    overwrite = args.overwrite
    generate = args.generate

    # Determine the logging level
    log_level = logging.DEBUG if args.verbose else getattr(logging, args.log_level)

    configure_logging(log_level=log_level, log_file=db_folder + '/scraper.log')

    # Create a logger for main.py
    logger = logging.getLogger(__name__)

    host_data_dir = os.getenv('HOST_DATA_DIR')

    if host_data_dir:
        logger.info(f"Host data directory: {host_data_dir}")

    if args.url:
        start_url = args.url
    elif args.o:
        start_url = f"https://coomer.su/onlyfans/user/{args.user}"
    elif args.f:
        start_url = f"https://coomer.su/fansly/user/{args.user}"
    else:
        start_url = f"https://coomer.su/{args.site}/user/{args.user}"

    parsed_url = urlparse(start_url)

    # Remove the query part by setting it to an empty string
    cleaned_url = parsed_url._replace(query='')
    
    url = urlunparse(cleaned_url)
    
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    path = cleaned_url.path
    api_url = f"{base_url}/api/v0{path}"

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
    logger.info(f"Database path: {db_path}")
    
    if not no_scrape:
        # Get data from the API
        all_links = get_posts_from_api(api_url, url, 0)

        if not args.soft_run:
            # Insert data into the database
            logger.info("Inserting data into the database...")
            create_or_update_db(all_links, db_path, overwrite)
        else:
            logger.info("Soft run enabled. Skipping database write.")
    else:
        logger.info("Scraping disabled")
    
    if write:
        logger.info(f"Updating the database with local files from path {file_path}")
        update_downloaded_status(db_path, file_path, host_data_dir)
    else:
        logger.info("Database write disabled, run with -w argument to enable. Use --no-scrape to disable scraping.")
    
    if generate:
        logger.info("Generating a file for undownloaded files")
        get_undownloaded_posts(db_path, file_path, profile_name)

if __name__ == '__main__':
    main()