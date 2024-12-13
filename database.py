import sqlite3
import os
import logging

logger = logging.getLogger(__name__) 

def create_or_update_db(data, db_path, overwrite):
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
	
	# Insert new entries
	for post_id, date, text, serverFileName, serverPath, post_url, mediaType in data:
		logger.debug(f"Checking if filename {serverFileName} already exists in the database")
		cursor.execute('''
			SELECT COUNT(*) FROM posts
			WHERE post_id = ? AND serverFileName = ?
		''', (post_id, serverFileName))
		row_count = cursor.fetchone()[0]

		if row_count == 0:
			logger.debug(f"Inserting post ID {post_id} into the database")
			cursor.execute('''
				INSERT INTO posts (post_id, date, text, serverFileName, serverPath, post_url, mediaType)
				VALUES (?, ?, ?, ?, ?, ?, ?)
			''', (post_id, date, text, serverFileName, serverPath, post_url, mediaType))
		else:
			logger.debug(f"Post ID {post_id} with serverFileName {serverFileName} already exists in the database, skipping insert")

	conn.commit()
	cursor.close()  # Explicitly close the cursor
	conn.close()

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