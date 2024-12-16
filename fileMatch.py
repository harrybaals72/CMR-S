import sqlite3
import os
import re
import logging

logger = logging.getLogger(__name__)

def get_ids_from_db(db_path):
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()
	cursor.execute("SELECT post_id FROM posts")
	ids = [str(row[0]).strip() for row in cursor.fetchall()]
	conn.close()
	return ids

def get_filenames_from_db(db_path):
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()
	cursor.execute("SELECT serverFileName FROM posts")
	filenames = [row[0] for row in cursor.fetchall()] 
	conn.close()
	return filenames

def extract_id_from_filename(filename):
	"""
	Extracts a numeric ID from a given filename.

	The function searches for a pattern in the filename that matches
	a sequence of 7 or more digits surrounded by hyphens and spaces.
	If such a pattern is found, the last numeric ID is returned as a string.
	If no match is found, the function returns None.

	Args:
		filename (str): The name of the file from which to extract the ID.

	Returns:
		str or None: The extracted numeric ID as a string, or None if no match is found.
	"""
	matches = re.findall(r'- ([DM]{0,2}\d{7,})', filename)
	logger.debug(f"Matches: {matches}")
	if matches:
		return matches[-1]
	return None

def update_file_path(conn, fileName, found_folder):
	cursor = conn.cursor()

	try:
		#Check if there is only one row with the serverFileName
		cursor.execute('''
			SELECT COUNT(*) FROM posts
			WHERE serverFileName = ?
		''', (fileName,))
		row_count = cursor.fetchone()[0]
		logger.debug(f"Found {row_count} row(s) with filename {fileName}")
		if row_count > 1:
			raise Exception(f"Multiple rows found for filename {fileName} in DB")

		# Update rows where severFileName matches
		cursor.execute('''
			UPDATE posts
			SET localFileName = ?, folder = ?, downloaded = 1
			WHERE serverFileName = ?
		''', (fileName, found_folder, fileName)) 
		conn.commit()
		logger.info(f"Updated folder for filename {fileName} to {found_folder}")
		 
		# # Select rows where the localFileName matches and return the folder(s) found
		# cursor.execute('''
		# 	SELECT folder FROM posts
		# 	WHERE localFileName = ?
		# 	AND folder IS NOT NULL
		# ''', (fileName,))
		# folders = cursor.fetchall()

		# # Get the number of rows that have the localFileName that matches
		# row_count = len(folders)
		# logger.debug(f"Found {row_count} row(s) with filename {fileName}")

		# if row_count <= 1:
		# 	# Set db_folder to the folder found in the database if only one row is found, otherwise set it to None
		# 	db_folder = folders[0][0] if row_count == 1 else None

		# 	# If the folder in the database is different from the found folder, update the folder
		# 	if db_folder != found_folder:
		# 		cursor.execute('''
		# 			UPDATE posts
		# 			SET folder = ?, downloaded = 1
		# 			WHERE localFileName = ?
		# 		''', (found_folder, fileName))
		# 		conn.commit()

		# 		logger.info(f"Updated folder for filename {fileName} from {db_folder} to {found_folder}")
		# else:
		# 	logger.error(f"Multiple rows found for filename {fileName} at {folders} Skipping update")
	except sqlite3.Error as e:
			logger.error(f"Database error: {e}")
	except Exception as e:
			logger.error(f"Unexpected error: {e}")
	finally:
		cursor.close()


def search_and_update_directory_for_serverFileName_matches(db_path, serverFileNames, directory, host_data_dir):
	logger.info(f"Searching directory: {directory}")
	video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', 'm4v')

	conn = sqlite3.connect(db_path)

	for root, _, files in os.walk(directory):
		logger.debug(f"Iterating through files in directory: {root}")
		for file in files:
			if file.lower().endswith(video_extensions):
				logger.debug(f"\nChecking video file: {file}")
				if file in serverFileNames:
					logger.debug(f"Match found for filename {file} in folder {root}")
					if host_data_dir:
						if root == directory:
							subDirName = ''
						else:
							subDirName = os.path.relpath(root, directory)
						folder_path = os.path.join(host_data_dir, subDirName)
						logger.debug(f"Subdirectory: {subDirName}")
					else:
						folder_path = root
					
					logger.debug(f"Folder path: {folder_path}")
					logger.debug(f"Match found for filename {file} in folder {folder_path}")

					update_file_path(conn, file, folder_path)
	conn.close()

def update_downloaded_status(db_path, file_path, host_data_dir):
	serverFileNames = get_filenames_from_db(db_path)
	logger.debug(f"DB serverFileNames: {serverFileNames}")
	logger.debug(f"Total DB serverFileNames: {len(serverFileNames)}")

	search_and_update_directory_for_serverFileName_matches(db_path, serverFileNames, os.path.dirname(file_path), host_data_dir)