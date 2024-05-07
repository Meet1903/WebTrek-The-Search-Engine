
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urlparse
import hashlib
import datetime

def generate_short_id(url):
    hash_object = hashlib.md5(url.encode())
    return hash_object.hexdigest()

def is_string_larger_tan_512(string, encoding='utf-8'):
    encoded_bytes = string.encode(encoding)
    return len(encoded_bytes) > 512

def extract_text_from_html_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html = file.read()
            soup = BeautifulSoup(html, 'html.parser')
            if soup.find('meta', {'property': 'og:url'}):
                url = soup.find('meta', {'property': 'og:url'})['content']
            else:
                return
            # Extract the domain from the URL
            domain = urlparse(url).netloc
            if soup.find('h1'):
                title = soup.find('h1').get_text().strip()
            elif soup.find('h2'):
                title = soup.find('h2').get_text().strip()
            else:
                title = url
            text = soup.get_text()
            text = re.sub(r'[^a-zA-Z0-9]+', ' ', text)
            text = text.strip()
            lines = text.split('\n')
            # text = '|'.join(lines)  # Separate lines with '|'
            lines_without_empty = [line.strip() for line in lines if line.strip()]
            text = '    '.join(lines_without_empty)
            if is_string_larger_tan_512(url):
                id = generate_short_id(url)
            else:
                id = url
            if not id:
                id = datetime.datetime.now()
            document = {
                "_index": "websearch",
                "_id": id,
                "_source": {
                    "title": title,
                    "domain": domain,
                    "url": url,
                    "content": text,
                },
            }
            return document
    except Exception as e:
        print("Error in data loading", e)
        return

def read_html_files(folder_path):
    bulk_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".html"):
            file_path = os.path.join(folder_path, filename)
            document = extract_text_from_html_file(file_path)
            if document:
                bulk_data.append(document)
    return bulk_data