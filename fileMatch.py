import sqlite3
import os
import re
import logging

logger = logging.getLogger(__name__)

def get_ids_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM posts")
    ids = {row[0] for row in cursor.fetchall()}
    conn.close()
    return ids


def extract_id_from_filename(filename):
    """
    Extracts a numeric ID from a given filename.

    The function searches for a pattern in the filename that matches
    a sequence of 7 or more digits surrounded by hyphens and spaces.
    If such a pattern is found, the numeric ID is returned as a string.
    If no match is found, the function returns None.

    Args:
        filename (str): The name of the file from which to extract the ID.

    Returns:
        str or None: The extracted numeric ID as a string, or None if no match is found.
    """
    match = re.search(r'- (\d{7,}) -', filename)
    if match:
        return match.group(1)
    return None

def search_directory_for_ids(directory, ids):
    matching_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_id = extract_id_from_filename(file)
            if file_id in ids:
                matching_files.append(os.path.join(root, file))
    return matching_files

def update_downloaded_status(db_path, file_path):
    ids = get_ids_from_db(db_path)
    # matching_files = search_directory_for_ids(os.path.dirname(file_path), ids)
    matching_files = []
    for root, _, files in os.walk(os.path.dirname(file_path)):
        for file in files:
            matching_files.append(os.path.join(root, file))
    logger.debug(f"Matching files: {matching_files}")
    