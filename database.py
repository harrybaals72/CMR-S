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
        logger.debug("Table 'posts' does not exist. Creating a new table")
        cursor.execute('''
            CREATE TABLE posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER,
                date TEXT,
                text TEXT,
                filename TEXT,
                folder TEXT,
                serverPath TEXT,
                path TEXT,
                mediaType INTEGER,
                downloaded INTEGER DEFAULT 0
            )
        ''')
    
    # Insert new entries
    for post_id, date, text, filename, folder, serverPath, path, mediaType in data:
        logger.debug(f"Checking if filename {filename} already exists in the database")
        cursor.execute('''
            SELECT COUNT(*) FROM posts
            WHERE post_id = ? AND filename = ?
        ''', (post_id, filename))
        row_count = cursor.fetchone()[0]

        if row_count == 0:
            logger.debug(f"Inserting post ID {post_id} into the database")
            cursor.execute('''
                INSERT INTO posts (post_id, date, text, filename, folder, serverPath, path, mediaType, downloaded)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
            ''', (post_id, date, text, filename, folder, serverPath, path, mediaType))
        else:
            logger.debug(f"Post ID {post_id} with filename {filename} already exists in the database, skipping insert")

    conn.commit()
    conn.close()