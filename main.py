import requests
from bs4 import BeautifulSoup
import re
import time
import sqlite3
import argparse
import os
from urllib.parse import urlparse

def get_links_from_page(soup, base_url):
    # Extract all the links on the page that match the pattern '/post/<a bunch of numbers>'
    pattern = re.compile(r'/post/\d+')
    links = soup.find_all('a', href=pattern)
    
    full_links_with_dates = []
    for link in links:
        href = link.get('href')
        full_link = base_url + href

        # Extract the ID from the href
        post_id = int(re.search(r'/post/(\d+)', href).group(1))
        
        # Find the date within the same element
        timestamp = link.find('time', class_='timestamp')
        date = timestamp.get('datetime') if timestamp else 'No date found'
        
        full_links_with_dates.append((post_id, date, full_link))
    
    return full_links_with_dates

def get_next_page_url(soup, base_url, current_url):
    next_button = soup.find('a', class_='next')
    if next_button:
        return base_url + next_button.get('href')
    else:
        print(f"No next button found for page: {current_url}")
        return None

def create_or_update_db(data, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            date TEXT,
            full_url TEXT
        )
    ''')
    
    # Insert new entries
    for post_id, date, full_url in data:
        cursor.execute('''
            INSERT OR IGNORE INTO posts (id, date, full_url)
            VALUES (?, ?, ?)
        ''', (post_id, date, full_url))
    
    conn.commit()
    conn.close()

def main():
    parser = argparse.ArgumentParser(description='Scrape links and dates from a website.')
    parser.add_argument('url', type=str, help='The URL to scrape')
    args = parser.parse_args()

    print(f"Parsing arguments: {args}")

    start_url = args.url
    parsed_url = urlparse(start_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    print(f"Parsing URL: {start_url}")
    print(f"Base URL: {base_url}")
    print()

    # Define the database path
    db_folder = '/output'
    db_path = os.path.join(db_folder, 'scraped_data.db')

    # Create the output folder if it doesn't exist
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    all_links = []
    link_count = 0

    current_url = start_url
    while current_url:
        print(f"Scraping URL: {current_url}")

        time.sleep(1)

        # Send an HTTP request to the website
        response = requests.get(current_url)

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Get links from the current page
        links = get_links_from_page(soup, base_url)
        all_links.extend(links)

        # Update the link count
        link_count += len(links)

        # Get the URL for the next page
        current_url = get_next_page_url(soup, base_url, current_url)

    # Print the data
    for post_id, date, full_url in all_links:
        print(f"ID: {post_id}, Date: {date}, Link: {full_url}")

    print(f"Total links found: {link_count}")

    # Insert data into the database
    print("Inserting data into the database...")
    create_or_update_db(all_links, db_path)

if __name__ == '__main__':
    main()