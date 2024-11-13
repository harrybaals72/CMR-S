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
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
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