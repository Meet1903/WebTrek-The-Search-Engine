
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse

bulk_data = []

def extract_text_from_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html = file.read()
    soup = BeautifulSoup(html, 'html.parser')
    url = soup.find('meta', {'property': 'og:url'})['content']

    # Extract the domain from the URL
    domain = urlparse(url).netloc
    title = soup.find('h1').get_text()
    print(url, domain, title, "\n\n\n\n")
    text = soup.get_text()
    text = text.strip()
    lines = text.split('\n')
    # text = '|'.join(lines)  # Separate lines with '|'
    lines_without_empty = [line.strip() for line in lines if line.strip()]
    text = '    '.join(lines_without_empty)

    document = {
        "_index": "websearch",
        "_source": {
            "title": title,
            "domain": domain,
            "url": url,
            "content": text,
        },
    }
    bulk_data.append(document)
    # filename = "html_text.txt"
    # with open(filename, 'a', encoding='utf-8') as file:
    #     file.write(text + '\n')  # Append the text followed by a newline character
    return text

def read_html_files(folder_path):
    html_files = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".html"):
            file_path = os.path.join(folder_path, filename)
            text_data = extract_text_from_html_file(file_path)
            # print(bulk_data)
            return bulk_data
            break