import logging
import os
import urllib.parse
from database import get_undownloaded_video_posts_from_db
from datetime import datetime

logger = logging.getLogger(__name__)

def get_extension(filename):
	_, extension = os.path.splitext(filename)
	return extension

def write_urls_to_file(folder_path, rows, profile_name, current_time):
	# Create the full file path using the profile name and current time
	file_path = os.path.join(folder_path, f"{profile_name}_{current_time}.txt")
	
	logger.debug(f"Writing undownloaded URLs to file: {file_path}")
	with open(file_path, 'w') as file:
		for row in rows:
			post_url = row[2]

			logger.info(f"Writing URL to file: {post_url}")
			file.write(f"{post_url}\n")
	logger.info(f"URLs written to file: {file_path}")


def write_urls_to_crawljob(folder_path, rows, profile_name, current_time):
	# Create the full file path using the profile name and current time
	file_path = os.path.join(folder_path, f"{profile_name}_{current_time}.crawljob")

	logger.debug(f"Writing undownloaded URLs to file: {file_path}")
	with open(file_path, 'w') as file:
		for row in rows:
			base_url = "coomer.su/data/"
			serverFileName, serverPath, *rest = row

			full_url = urllib.parse.urljoin(base_url, serverPath)
			logger.info(f"Writing URL to file: {full_url} with filename {serverFileName}, packageName {profile_name}, and folder /output/simpcity/{profile_name}/{current_time}")				

			file.write(f"text={full_url}\n")
			file.write(f"filename={serverFileName}\n")
			file.write(f"packageName={profile_name}\n")
			file.write(f"downloadFolder=/output/simpcity/{profile_name}/{current_time}\n\n")

	logger.info(f"URLs written to file: {file_path}")


def generate_undownloaded_post_links(db_path, file_path, profile_name):
	logger.debug(f"Generating a file for undownloaded files in database: {db_path}")
	rows = get_undownloaded_video_posts_from_db(db_path)
	logger.info(f"Total number of undownloaded posts: {len(rows)}")

	current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
	write_urls_to_crawljob(file_path, rows, profile_name, current_time)
	write_urls_to_file(file_path, rows, profile_name, current_time)