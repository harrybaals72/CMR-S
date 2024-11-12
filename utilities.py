import re
from bs4 import BeautifulSoup

def remove_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def processText(text):
    modifiedText = remove_html_tags(text)
    modifiedText = modifiedText.replace('\n', ' ')
    modifiedText = modifiedText.strip()
    modifiedText = re.sub(' +', ' ', modifiedText)
    return modifiedText