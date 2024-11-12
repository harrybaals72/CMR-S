import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Scrape links and dates from a website.')
    parser.add_argument('url', type=str, help='The URL to scrape')
    parser.add_argument('-d', '--delay', type=int, default=1, help='Delay between requests in seconds')
    parser.add_argument('-o', '--output', type=str, default='/output', help='Output folder for the database')
    return parser.parse_args()