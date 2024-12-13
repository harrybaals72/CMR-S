import argparse
import logging

logger = logging.getLogger(__name__)

def parse_arguments():
	parser = argparse.ArgumentParser(description='Scrape links and dates from a website.')

	# Mutually exclusive group for url and site/user
	group = parser.add_mutually_exclusive_group(required=False)
	group.add_argument('--url', type=str, help='The URL to scrape')
	group.add_argument('-s', '--site', type=str, help='The site to scrape')

	# Second mutually exclusive group for site/user and file
	group2 = parser.add_mutually_exclusive_group(required=False)
	group2.add_argument('-f', action='store_true', help='Use FA site')
	group2.add_argument('-o', action='store_true', help='Use OFA site')
	
	# User argument (not part of the mutually exclusive group)
	parser.add_argument('-u', '--user', type=str, help='The user to scrape')

	parser.add_argument('-d', '--db-path', type=str, default='/output', help='Manually set path to database')
	parser.add_argument('--soft-run', action='store_true', help='Run the scraper without writing to the database')
	parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output (set log level to DEBUG)')
	parser.add_argument('--log-level', type=str, default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help='Set the logging level')
	parser.add_argument('-n', '--no-scrape', action='store_true', help='Disable scraping (default: False)')
	parser.add_argument('-w', '--write', action='store_true', help='Write to the database with local files')
	parser.add_argument('--file-path', type=str, default='/userData/', help='Local directory with files to match. Default is /userData/')
	parser.add_argument('--overwrite', action='store_true', help='Overwrite the database if it already exists')
	parser.add_argument('-g', '--generate', action='store_true', help='Generate a crawljob for undownloaded files')

	args = parser.parse_args()
	logger.info(f"Arguments: {args}")

	# Custom validation logic
	if args.site and not args.user:
		parser.error("--site requires --user")
	if args.user and (not args.site and (not args.f and not args.o)):
		parser.error("--user requires --site")
	if (args.f or args.o) and not args.user:
		parser.error("--f or --o requires --user")
	if args.f and args.o:
		parser.error("-f and -o are mutually exclusive")

	return args