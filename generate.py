import sqlite3
import logging

logger = logging.getLogger(__name__)

def get_undownloaded_posts(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT *
        FROM posts
        WHERE downloaded = 0
        AND mediaType = 2
    ''')

    posts = cursor.fetchall()
    conn.close()

    return posts

def generate_crawljob(db_path):
    rows = get_undownloaded_posts(db_path)
    for row in rows:
        logger.debug(f"Row: {row}")
    logger.debug(f"Total rows: {len(rows)}")