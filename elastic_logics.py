from elasticsearch import Elasticsearch, helpers
import warnings
from bs4 import BeautifulSoup
import os
from prepare_data import read_html_files


# Suppress InsecureRequestWarning and SecurityWarning
warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL 1.1.1+")
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

client = Elasticsearch(
  "https://localhost:9200",
  api_key="YVdaLV9ZNEJaQjY1MGt1aWR5aFI6Z0xSRWFFTTRTSkdXaXZrYWNCZXN2QQ==",
  verify_certs=False
)


def search_on_elastic(clean_query):
  words = clean_query.split(' ')
  query_with_and = " AND ".join(words)
  resp = client.search(index="websearch", query={"query_string": {"query": query_with_and}})
  urls = []
  for hit in resp["hits"]["hits"]:
    print(hit["_source"]['url'])
    urls.append(hit["_source"]['url'])
  return urls


def insert_data_elastic(folder):
  path_to_HTML_files = folder

  # Data preparer call
  bulk_data = read_html_files(path_to_HTML_files)

  # Inserting all data
  helpers.bulk(client, bulk_data)