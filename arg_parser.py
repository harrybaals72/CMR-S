import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Scrape links and dates from a website.')
    parser.add_argument('url', type=str, help='The URL to scrape')
    parser.add_argument('-d', '--delay', type=int, default=1, help='Delay between requests in seconds')
    parser.add_argument('-o', '--output', type=str, default='/output', help='Output folder for the database')
    parser.add_argument('-s', '--soft-run', action='store_true', help='Run the scraper without writing to the database')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output (set log level to DEBUG)')
    parser.add_argument('--log-level', type=str, default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Set the logging level')
    
    return parser.parse_args()