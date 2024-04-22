import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse

ignored_domains = ['instagram.com', 'twitter.com', 'youtube.com', 'facebook.com', 'mailto:']

def delete_files_in_folder(folder_path):
    files = os.listdir(folder_path)
    
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

def retrieve_domain_names(file_path):
    domain_names = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip() 
            domain_names.append(line)
    return domain_names

def unearth_urls(domain):
    urls = set()
    parsed_domain = urlparse(domain)
    response = requests.get(domain)
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.find_all('a'):
        if 'href' in link.attrs:
            url = link.attrs['href']
            # print(domain, url)
            if any(ignored_domain in url for ignored_domain in ignored_domains):
                continue
            if url.startswith('/'):
                urls.add(parsed_domain.scheme + "://" + parsed_domain.netloc + url)
            if url.startswith(domain):
                urls.add(url)
    return list(urls)

def get_urls(domains):
    counter = 0 
    while counter < len(domains) and len(set(domains)) < 10000:
        if any(ignored_domain in domains[counter] for ignored_domain in ignored_domains):
            counter += 1
            continue
        domains.extend(unearth_urls(domains[counter]))
        counter += 1
    print(domains)
    domains = set(domains)
    return list(domains)
    

def save_html(urls, folder):
    folder_path = folder
    os.makedirs(folder_path, exist_ok=True)
    for index, url in enumerate(urls[:1000]):
        if url.startswith("https://") or url.startswith("http://"):
            response = requests.get(url)
            if response.status_code == 200:
                filename = f"html_file_{index}.html"
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(response.text)
            else:
                continue