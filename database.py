import sqlite3
import os
import logging

logger = logging.getLogger(__name__) 

def add_folder_column(cursor):
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
        add_folder_column(cursor)

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
    for post_id, date, text, filename, serverPath, folder, path, mediaType in data:
        logger.debug(f"Checking if post ID {post_id} already exists in the database")
        cursor.execute('''
            SELECT COUNT(*) FROM posts
            WHERE post_id = ? AND date = ? AND text = ?
        ''', (post_id, date, text))
        row_count = cursor.fetchone()[0]

        if row_count == 0:
            logger.debug(f"Inserting post ID {post_id} into the database")
            cursor.execute('''
                INSERT INTO posts (post_id, date, text, filename, folder, path, mediaType, downloaded)
                VALUES (?, ?, ?, ?, ?, ?, ?, 0)
            ''', (post_id, date, text, filename, folder, path, mediaType))
        else:
            logger.debug(f"Post ID {post_id} already exists in the database, skipping insert")

    conn.commit()
    conn.close()