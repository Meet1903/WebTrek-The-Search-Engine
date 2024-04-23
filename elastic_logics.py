from elasticsearch import Elasticsearch, helpers
import warnings
from bs4 import BeautifulSoup
import os
from prepare_data import read_html_files
import datetime


warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL 1.1.1+")
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

client = Elasticsearch(
  "https://localhost:9200",
  api_key="YOUR_API_KEY",
  verify_certs=False
)


def search_on_elastic(clean_query):
  words = clean_query.split(' ')
  query_with_and = " AND ".join(words)
  resp = client.search(index="websearch", query={"query_string": {"query": query_with_and}})
  urls = []
  titles = []
  for hit in resp["hits"]["hits"]:
    print(hit["_source"]['url'])
    urls.append(hit["_source"]['url'])
    titles.append(hit["_source"]['title'])
  return urls, titles


def insert_data_elastic(folder):
  path_to_HTML_files = folder
  bulk_data = read_html_files(path_to_HTML_files)
  helpers.bulk(client, bulk_data)

def insert_query_history(query):
  timestamp = datetime.datetime.now()
  document = {'query': query, 'timestamp': timestamp}
  client.index(index='history', document=document)

def fetch_history():
  # resp = client.search(index="history", body={"query": {"match_all": {}}})
  resp = client.search(index="history", body={"query": {"match_all": {}}, "sort": [{"timestamp": {"order": "desc"}}], "size": 15})
  queries = []
  timestamps = []
  for hit in resp["hits"]["hits"]:
    queries.append(hit["_source"]['query'])
    timestamps.append(hit["_source"]['timestamp'])
  return queries, timestamps

def delete_all_history():
  try:
    client.delete_by_query(index=['history'], body={"query": {"match_all": {}}})
  except:
    return 'No history available'