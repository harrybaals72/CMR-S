import sqlite3
import os
import re
import logging

logger = logging.getLogger(__name__)

def get_ids_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT post_id FROM posts")
    ids = [str(row[0]).strip() for row in cursor.fetchall()]
    conn.close()
    return ids


def extract_id_from_filename(filename):
    """
    Extracts a numeric ID from a given filename.

    The function searches for a pattern in the filename that matches
    a sequence of 7 or more digits surrounded by hyphens and spaces.
    If such a pattern is found, the last numeric ID is returned as a string.
    If no match is found, the function returns None.

    Args:
        filename (str): The name of the file from which to extract the ID.

    Returns:
        str or None: The extracted numeric ID as a string, or None if no match is found.
    """
    matches = re.findall(r'- ([DM]{0,2}\d{7,})', filename)
    logger.debug(f"Matches: {matches}")
    if matches:
        return matches[-1]
    return None

def search_directory_for_ids(directory, ids, conn):
    logger.debug(f"Searching directory: {directory}")
    matching_files = []
    matching_ids = []
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(video_extensions):
                logger.debug(f"\nChecking video file: {file}")
                file_id = extract_id_from_filename(file)
                if not file_id:
                    logger.debug(f"No ID found in filename: {file}")
                    continue

                file_id = file_id.strip()
                logger.debug(f"Extracted ID: {file_id}")

                if file_id in ids:
                    # Extract the folder path
                    folder_path = root

                    logger.debug(f"Match found for ID {file_id} for file {file} in folder {folder_path}")
                    cursor = conn.cursor()
                    # Update only one entry with the given id and path IS NULL
                    cursor.execute('''
                        UPDATE posts
                        SET filename = ?, folder = ?
                        WHERE rowid = (
                            SELECT rowid
                            FROM posts
                            WHERE post_id = ? AND filename IS NULL
                            LIMIT 1
                        )
                    ''', (file, folder_path, file_id))
                    conn.commit()

                    matching_files.append(os.path.join(root, file))
                    matching_ids.append(file_id)

    conn.close()
    
    return (matching_files, matching_ids)

def update_database(db_path, matching_ids):
    logger.info(f"Updating downloaded status for {len(matching_ids)} files in the database")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    rows_updated = 0

    cursor.executemany('''
        UPDATE posts
        SET downloaded = 1
        WHERE post_id = ?
        AND mediaType = 2
    ''', [(post_id,) for post_id in matching_ids])

    rows_updated = cursor.rowcount
    logger.info(f"Rows updated: {rows_updated}")

    conn.commit()
    conn.close()

def update_downloaded_status(db_path, file_path):
    ids = get_ids_from_db(db_path)
    logger.debug(f"DB IDs: {ids}")
    logger.debug(f"Total DB IDs: {len(ids)}")

    conn = sqlite3.connect(db_path)

    matching_files, matching_ids = search_directory_for_ids(os.path.dirname(file_path), ids, conn)
    
    logger.debug(f"Matching files: {matching_files}")
    logger.debug(f"Total matching files: {len(matching_files)}")
    
    logger.debug(f"Matching IDs: {matching_ids}")
    logger.debug(f"Total matching IDs: {len(matching_ids)}")

    update_database(db_path, matching_ids)