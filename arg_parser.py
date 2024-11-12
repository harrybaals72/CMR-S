import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Scrape links and dates from a website.')

    # Mutually exclusive group for url and site/user
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', type=str, help='The URL to scrape')
    group.add_argument('-s', '--site', type=str, help='The site to scrape')

    # User argument (not part of the mutually exclusive group)
    parser.add_argument('-u', '--user', type=str, help='The user to scrape')

    parser.add_argument('-d', '--delay', type=int, default=1, help='Delay between requests in seconds')
    parser.add_argument('-o', '--output', type=str, default='/output', help='Output folder for the database')
    parser.add_argument('--soft-run', action='store_true', help='Run the scraper without writing to the database')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output (set log level to DEBUG)')
    parser.add_argument('--log-level', type=str, default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help='Set the logging level')
    parser.add_argument('--no-scrape', action='store_true', help='Disable scraping (default: False)')
    parser.add_argument('-w', '--write', action='store_true', help='Write to the database with local files')
    parser.add_argument('--file-path', type=str, default='/userData/', help='Local directory with files to match. Default is /userData/')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite the database if it already exists')

    args = parser.parse_args()

    # Custom validation logic
    if args.site and not args.user:
        parser.error("--site requires --user")
    if args.user and not args.site:
        parser.error("--user requires --site")

    return args