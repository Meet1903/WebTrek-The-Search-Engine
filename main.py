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

# API key should have cluster monitor rightps
# print(client.info())

documents = [
  { "index": { "_index": "websearch"}},
  {"name": "Snow Crash", "author": "Neal Stephenson", "release_date": "1992-06-01", "page_count": 470, "_extract_binary_content": True, "_reduce_whitespace": True, "_run_ml_inference": True},
  { "index": { "_index": "websearch"}},
  {"name": "Revelation Space", "author": "Alastair Reynolds", "release_date": "2000-03-15", "page_count": 585, "_extract_binary_content": True, "_reduce_whitespace": True, "_run_ml_inference": True},
  { "index": { "_index": "websearch"}},
  {"name": "1984", "author": "George Orwell", "release_date": "1985-06-01", "page_count": 328, "_extract_binary_content": True, "_reduce_whitespace": True, "_run_ml_inference": True},
  { "index": { "_index": "websearch"}},
  {"name": "Fahrenheit 451", "author": "Ray Bradbury", "release_date": "1953-10-15", "page_count": 227, "_extract_binary_content": True, "_reduce_whitespace": True, "_run_ml_inference": True},
  { "index": { "_index": "websearch"}},
  {"name": "Brave New World", "author": "Aldous Huxley", "release_date": "1932-06-01", "page_count": 268, "_extract_binary_content": True, "_reduce_whitespace": True, "_run_ml_inference": True},
  { "index": { "_index": "websearch"}},
  {"name": "The Handmaid's Tale", "author": "Margaret Atwood", "release_date": "1985-06-01", "page_count": 311, "_extract_binary_content": True, "_reduce_whitespace": True, "_run_ml_inference": True},
]

# client.bulk(operations=documents, pipeline="ent-search-generic-ingestion")

# client.search(index="websearch")
# resp = client.search(index="websearch", query={"match_all": {}})
# resp = client.search(index="websearch", query={"query_string": {"query": "meet AND hey AND hello"}})
# print("Got {} hits:".format(resp["hits"]["total"]["value"]))
# for hit in resp["hits"]["hits"]:
#     print(hit["_source"])

path_to_HTML_files = "/Users/meetdiwan/Documents/GIT/Search-Engine/html_files"
bulk_data = read_html_files(path_to_HTML_files)
# client.bulk(operations=bulk_data, pipeline="ent-search-generic-ingestion")
helpers.bulk(client, bulk_data)