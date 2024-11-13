import requests
import logging
from time import sleep

from utilities import processText

logger = logging.getLogger(__name__)

def send_get_request(url):
    try:
        logger.debug(f"Sending GET request to: {url}")
        response = requests.get(url)
        response.raise_for_status() # Raise an exception for 4xx/5xx status codes
        data = response.json() # Parse the JSON response
        logger.debug(f"Data received from API: {data}, Size: {len(data)}")
        return data
    except requests.exceptions.HTTPError as err:
        logger.error(f"HTTP error occurred: {err}")
    except Exception as err:
        logger.error(f"An error occurred: {err}")
    return None

def get_profile_name(api_url):
    data = send_get_request(api_url + "/profile")
    return data.get('name') if data else None

def get_posts_from_api(api_url, cleaned_url, offset):
    postsRemaining = True
    posts_list = []

    while postsRemaining:
        url = f"{api_url}?o={offset}"
        offset += 50

        data = send_get_request(url)

        if not data:
            logger.debug("Response is an empty array, ending search")
            postsRemaining = False
            continue
        else:
            logger.debug("Response is not empty, processing data")
            posts_list.extend(processResponse(data, cleaned_url))
            sleep(1)
    
    # Print the data
    logger.debug(f"Total posts found: {len(posts_list)}")
    for post_id, date, text, filename, path, mediaType in posts_list:
        logger.debug(f"ID: {post_id}, Date: {date}, Filename: {filename}, text: {text}, path: {path}, mediaType: {mediaType}\n")

    logger.info(f"Total links found: {len(posts_list)}")
    return posts_list

def is_non_image_file(file_obj):
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    file_name = file_obj.get('name', '').lower()
    return not any(file_name.endswith(ext) for ext in image_extensions)
    
def processResponse(data, cleaned_url):
    posts_list = []
    for post in data:
        # Check if 'file' exists and is not empty
        file_present = 'file' in post and bool(post['file'])
        # Check if 'attachments' exists and is not empty
        attachments_present = 'attachments' in post and bool(post['attachments'])

        post_id = post.get('id')
        text = post.get('content')
        date = post.get('published')
        url = f"{cleaned_url}/post/{post_id}"

        text = processText(text)
        if not text or not text.strip():
            text = None
        
        if file_present or attachments_present:
            non_image_files = []

            if file_present and is_non_image_file(post['file']):
                non_image_files.append(post['file'])

            if attachments_present:
                non_image_files.extend(
                    attachment for attachment in post['attachments'] if is_non_image_file(attachment)
                )
            
            if non_image_files:
                logger.info(f"Video files found for ID {post.get('id')}:")

                for file in non_image_files:
                    print(f"Filename: {file.get('name')}")
                    filename = file.get('name')
                    posts_list.append((post_id, date, text, None, url, 2))
                    logger.info("Post added:")
                    logger.info(f"ID: {post_id}, Date: {date}, Filename: {filename}, text: {text}\n\n")
            else:
                logger.debug(f"No video files found for ID {post.get('id')}")
                if file_present:
                    posts_list.append((post_id, date, text, None, url, 1))
                elif attachments_present:
                    posts_list.append((post_id, date, text, None, url, 1))
                
        else:
            logger.debug(f"No files or attachments found for ID {post.get('id')}")
            posts_list.append((post_id, date, text, None, url, 0))
    
    return posts_list
    