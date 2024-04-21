import requests
from bs4 import BeautifulSoup
import os

def retrieve_domain_names(file_path):
    domain_names = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip() 
            domain_names.append(line)
    return domain_names

def get_urls(domains):
    for domain in domains:
        # print(domain)
        response = requests.get(domain)
        soup = BeautifulSoup(response.content, 'html.parser')
        urls = []

        for link in soup.find_all('a'):
            if 'href' in link.attrs:
                url = link.attrs['href']
                print(url)
                if url.startswith('/'):
                    urls.append(domain + url)
                if url.startswith(domain):
                    urls.append(url)

    return urls

def save_html(urls, folder):
    folder_path = folder
    os.makedirs(folder_path, exist_ok=True)

    for index, url in enumerate(urls[:100]):
        if url.startswith("https://") or url.startswith("http://"):
            response = requests.get(url)
            if response.status_code == 200:
                filename = f"html_file_{index}.html"
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(response.text)
            else:
                continue