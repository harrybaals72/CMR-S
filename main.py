import os
from urllib.parse import urlparse

from arg_parser import parse_arguments
from database import create_or_update_db
from scraper import scrape_links

def main():
    
    args = parse_arguments()
    print(f"Parsing arguments: {args}")

    start_url = args.url
    delay = args.delay
    db_folder = args.output

    parsed_url = urlparse(start_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    print(f"Parsing URL: {start_url}")
    print(f"Base URL: {base_url}")
    print()
    
    db_path = os.path.join(db_folder, 'scraped_data.db')

    # Create the output folder if it doesn't exist
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    all_links = scrape_links(start_url, base_url, delay)

    # Print the data
    for post_id, date, full_url in all_links:
        print(f"ID: {post_id}, Date: {date}, Link: {full_url}")

    print(f"Total links found: {len(all_links)}")

    # Insert data into the database
    print("Inserting data into the database...")
    create_or_update_db(all_links, db_path)

if __name__ == '__main__':
    main()