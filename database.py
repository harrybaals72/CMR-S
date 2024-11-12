import sqlite3

def create_or_update_db(data, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER,
            date TEXT,
            text TEXT,
            filename TEXT PRIMARY KEY,
            path TEXT,
            mediaType INTEGER,
            downloaded INTEGER DEFAULT 0
        )
    ''')
    
    # Insert new entries
    for post_id, date, text, filename, path, mediaType in data:
        cursor.execute('''
            INSERT OR IGNORE INTO posts (id, date, text, filename, path, mediaType, downloaded)
            VALUES (?, ?, ?, ?, ?, ?, 0)
        ''', (post_id, date, text, filename, path, mediaType))
    
    conn.commit()
    conn.close()