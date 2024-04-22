
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urlparse


def extract_text_from_html_file(file_path):
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
        else:
            title = url
        text = soup.get_text()
        text = re.sub(r'[^a-zA-Z0-9]+', ' ', text)
        text = text.strip()
        lines = text.split('\n')
        # text = '|'.join(lines)  # Separate lines with '|'
        lines_without_empty = [line.strip() for line in lines if line.strip()]
        text = '    '.join(lines_without_empty)

        document = {
            "_index": "websearch",
            "_id": url,
            "_source": {
                "title": title,
                "domain": domain,
                "url": url,
                "content": text,
            },
        }
        return document
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