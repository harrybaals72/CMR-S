import sqlite3
import logging
import os

logger = logging.getLogger(__name__)

def get_posts_from_db(db_path):
    logger.debug(f"Getting undownloaded posts from database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT path
        FROM posts
        WHERE downloaded = 0
        AND mediaType = 2
    ''')

    posts = cursor.fetchall()
    conn.close()

    return posts

def write_urls_to_file(folder_path, urls, profile_name):
    # Create the full file path using the profile name
    file_path = os.path.join(folder_path, f"{profile_name}.txt")

    logger.debug(f"Writing undownloaded URLs to file: {file_path}")
    with open(file_path, 'w') as file:
        for url in urls:
            file.write(f"{url}\n")
    logger.info(f"URLs written to file: {file_path}")

def get_undownloaded_posts(db_path, file_path, profile_name):
    logger.debug(f"Generating a file for undownloaded files in database: {db_path}")
    rows = get_posts_from_db(db_path)
    logger.info(f"Total number of undownloaded posts: {len(rows)}")
    write_urls_to_file(file_path, [row[0] for row in rows], profile_name)
    