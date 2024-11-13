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

        # Check if the 'folder' column exists
        cursor.execute("PRAGMA table_info(posts)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'folder' not in columns:
            logger.debug("Column 'folder' does not exist")
            # Create a new table with the desired schema
            cursor.execute('''
                CREATE TABLE posts_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id INTEGER,
                    date TEXT,
                    text TEXT,
                    filename TEXT,
                    folder TEXT,
                    path TEXT,
                    mediaType INTEGER,
                    downloaded INTEGER DEFAULT 0
                )
            ''')

            logger.debug("New table 'posts_new' created")
            # Copy data from the old table to the new table
            cursor.execute('''
                INSERT INTO posts_new (id, post_id, date, text, filename, path, mediaType, downloaded)
                SELECT id, post_id, date, text, filename, path, mediaType, downloaded
                FROM posts
            ''')

            # Drop the old table
            logger.debug("Dropping old table 'posts'")
            cursor.execute("DROP TABLE posts")

            # Rename the new table to the original table name
            logger.debug("Renaming new table to 'posts'")
            cursor.execute("ALTER TABLE posts_new RENAME TO posts")

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
                path TEXT,
                mediaType INTEGER,
                downloaded INTEGER DEFAULT 0
            )
        ''')
    
    # Insert new entries
    for post_id, date, text, filename, folder, path, mediaType in data:
        cursor.execute('''
            INSERT OR IGNORE INTO posts (post_id, date, text, filename, folder, path, mediaType, downloaded)
            VALUES (?, ?, ?, ?, ?, ?, ?, 0)
        ''', (post_id, date, text, filename, folder, path, mediaType))
    
    conn.commit()
    conn.close()