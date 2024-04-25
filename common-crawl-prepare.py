from bs4 import BeautifulSoup
from warcio.archiveiterator import ArchiveIterator
import os
from data_scrapper import delete_files_in_folder
from prepare_data import read_html_files, extract_text_from_html_file
from elastic_logics import insert_data_elastic

warc_file_paths = ['Path_To_File/FileName1.warc', 'Path_To_File/FileName2.warc']
folder_path = 'Path_To_Folder'

def is_english_page(soup):
    html_tag = soup.find('html')
    if html_tag and html_tag.has_attr('lang'):
        lang = html_tag['lang']
        return lang.startswith('en')
    else:
        return False
    
def read_warc_file(warc_file_path, start_index, end_index):
    counter = 0
    with open(warc_file_path, 'rb') as stream:
        for index, record in enumerate(ArchiveIterator(stream)):
            if start_index <= index < end_index:
                if record.rec_type == 'response':
                    try:
                        url = record.rec_headers.get_header('WARC-Target-URI')
                        content = record.content_stream().read()
                        soup = BeautifulSoup(content, 'html.parser')
                        if not is_english_page(soup):
                            continue
                        filename = f"html_file_{index}.html"
                        file_path = os.path.join(folder_path, filename)
                        with open(file_path, 'w', encoding='utf-8', errors='ignore') as file:
                            file.write(content.decode('utf-8', errors='ignore'))
                    except:
                        continue
            if index >= end_index:
                break

if __name__ == '__main__':
    for warc_file_path in warc_file_paths:
        start_index = 0
        end_index = 2000
        while end_index < 120000:
            read_warc_file(warc_file_path, start_index, end_index)
            insert_data_elastic(folder_path)
            delete_files_in_folder(folder_path)
            start_index = end_index
            end_index += 2000