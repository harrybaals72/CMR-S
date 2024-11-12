import sqlite3

def create_or_update_db(data, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            date TEXT,
            full_url TEXT,
            text TEXT,
            downloaded INTEGER DEFAULT 0
        )
    ''')
    
    # Insert new entries
    for post_id, date, full_url in data:
        cursor.execute('''
            INSERT OR IGNORE INTO posts (id, date, full_url, text, downloaded)
            VALUES (?, ?, ?, NULL, 0)
        ''', (post_id, date, full_url))
    
    conn.commit()
    conn.close()