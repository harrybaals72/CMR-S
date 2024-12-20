import sqlite3
import os
import logging

logger = logging.getLogger(__name__) 

def create_db(db_path, overwrite):
	if overwrite and os.path.exists(db_path):
		logger.info(f"Deleting existing database at {db_path}")
		os.remove(db_path)

	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

	# Check if the 'posts' table exists
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='posts'")
	table_exists = cursor.fetchone()
	
	if table_exists:
		logger.debug("Table 'posts' exists")
	else:
		# Create the table if it doesn't exist
		logger.info("Table 'posts' does not exist. Creating a new table")
		cursor.execute('''
			CREATE TABLE posts (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				post_id INTEGER,
				date TEXT,
				text TEXT,
				serverFileName TEXT,
				localFileName TEXT,
				folder TEXT,
				serverPath TEXT,
				post_url TEXT,
				mediaType INTEGER,
				downloaded INTEGER DEFAULT 0
			)
		''')
		conn.commit()
	
	cursor.close()  # Explicitly close the cursor
	conn.close()
	################################### END OF CREATE_DB ###################################


def insert_new_row(conn, post_id, date, text, serverFileName, serverPath, post_url, mediaType):
	cursor = conn.cursor()

	logger.debug(f"Inserting new row with post ID {post_id}, serverFileName {serverFileName} into the database\n")
	cursor.execute('''
		INSERT INTO posts (post_id, date, text, serverFileName, serverPath, post_url, mediaType)
		VALUES (?, ?, ?, ?, ?, ?, ?)
	''', (post_id, date, text, serverFileName, serverPath, post_url, mediaType))

	conn.commit()
	cursor.close()  # Explicitly close the cursor
	################################### END OF INSERT_NEW_ROW ###################################

def update_row(conn, post_id, date, text, serverFileName, serverPath, post_url, mediaType):
	cursor = conn.cursor()

	logger.debug(f"Updating row with post ID {post_id}, serverFileName {serverFileName} in the database \n")
	cursor.execute('''
		UPDATE posts
		SET date = ?, text = ?, serverFileName = ?, serverPath = ?, post_url = ?, mediaType = ?
		WHERE post_id = ? AND serverFileName = ?
	''', (date, text, serverFileName, serverPath, post_url, mediaType, post_id, serverFileName))

	conn.commit()
	cursor.close()  # Explicitly close the cursor
	################################### END OF UPDATE_ROW ###################################


def update_db(conn, data):
	inserted_count = 0
	updated_count = 0

	for post_id, date, text, serverFileName, serverPath, post_url, mediaType in data:
		cursor = conn.cursor()

		if mediaType == 0:
			# Check if a row with a matching post_id
			logger.debug(f"Media type is 0, checking for post ID {post_id}")
			cursor.execute('''
				SELECT * FROM posts
				WHERE post_id = ?
			''', (post_id,))
		else:
			# Check if a row with a matching post_id and serverFileName is already exists in the database
			logger.debug(f"Media type is not 0, checking for post ID {post_id} and serverFileName {serverFileName}")
			cursor.execute('''
				SELECT * FROM posts
				WHERE post_id = ? AND serverFileName = ?
			''', (post_id, serverFileName))
			
		rows = cursor.fetchall()
		logger.debug(f"{len(rows)} rows returned for id: {post_id} and SFN: {serverFileName}")

		cursor.close()  # Close the cursor before updating the row

		if len(rows) == 0:
			logger.info(f"No rows found with post ID {post_id} and serverFileName {serverFileName}, inserting new row")
			insert_new_row(conn, post_id, date, text, serverFileName, serverPath, post_url, mediaType)
			inserted_count += 1
		elif len(rows) == 1:
			logger.debug(f"Row with post ID {post_id} and serverFileName {serverFileName} already exists, updating row")
			update_row(conn, post_id, date, text, serverFileName, serverPath, post_url, mediaType)
			updated_count += 1
		else:
			logger.error(f"Multiple rows found with post ID {post_id} and serverFileName {serverFileName}, skipping update")
			raise Exception(f"Multiple rows found with post ID {post_id} and serverFileName {serverFileName}, which is unexpected.")
		
		cursor.close()  # Explicitly close the cursor
		
	conn.commit()
	logger.info(f"\n\nInserted {inserted_count} new rows and updated {updated_count} rows.\n")
	
	################################### END OF UPDATE_DB ###################################


def create_or_update_db(data, db_path, overwrite):
	create_db(db_path, overwrite)

	conn = sqlite3.connect(db_path)
	conn.row_factory = sqlite3.Row

	update_db(conn, data)
	conn.close()
	################################### END OF CREATE_OR_UPDATE_DB ###################################


def get_undownloaded_video_posts_from_db(db_path):
	logger.debug(f"Fetching undownloaded video posts from database: {db_path}")
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

	cursor.execute('''
		SELECT DISTINCT serverFileName, serverPath, post_url
		FROM posts
		WHERE downloaded = 0
		AND mediaType = 2
	''')

	rows = cursor.fetchall()
	conn.close()

	return rows
	################################### END OF GET_UNDOWNLOADED_VIDEO_POSTS_FROM_DB ###################################