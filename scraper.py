import time
import requests
import re
from bs4 import BeautifulSoup

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

def scrape_links(start_url, base_url, delay):
    all_links = []

    current_url = start_url
    while current_url:
        print(f"Scraping URL: {current_url}")

        time.sleep(delay)

        # Send an HTTP request to the website
        response = requests.get(current_url)

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Get links from the current page
        links = get_links_from_page(soup, base_url)
        all_links.extend(links)

        # Get the URL for the next page
        current_url = get_next_page_url(soup, base_url, current_url)
    
    return all_links