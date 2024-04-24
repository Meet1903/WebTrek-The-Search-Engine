from elasticsearch import Elasticsearch, TransportError, helpers
# from elasticsearch.exceptions import BulkIndexError
import warnings
from bs4 import BeautifulSoup
import os
from prepare_data import read_html_files
import datetime

history_page_data_limit = 10

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
  query_body = {
     "size": 25, 
     "query": {"query_string": {"query": query_with_and}}
  }
  resp = client.search(index="websearch", body=query_body)
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
  try:
      print(len(bulk_data))
      response = helpers.bulk(client, bulk_data)
      success_count = response[0]
      print(f"{success_count} documents were successfully inserted.")
  except helpers.BulkIndexError as e:
      print("Bulk indexing failed for some documents:")
      for i, item in enumerate(e.errors):
          print(f"Document {i+1} failed:", item)

def insert_query_history(query):
  timestamp = datetime.datetime.now()
  document = {'query': query, 'timestamp': timestamp}
  client.index(index='history', document=document)

def fetch_history(page_number = 1):
  page_size = history_page_data_limit
  from_offset = (page_number - 1) * page_size

  query_body = {
      "query": {"match_all": {}},
      "sort": [{"timestamp": {"order": "desc"}}],
      "from": from_offset,
      "size": page_size
  }
  resp = client.search(index="history", body=query_body)
  queries = []
  timestamps = []
  for hit in resp["hits"]["hits"]:
    queries.append(hit["_source"]['query'])
    timestamps.append(hit["_source"]['timestamp'])
  return queries, timestamps

def delete_all_history():
  try:
    query_body = {
       "query": {"match_all": {}}
    }
    client.delete_by_query(index=['history'], body=query_body)
  except:
    return 'No history available'
  
def change_limit():
  try:
    response = client.indices.put_settings(index='websearch', body={"index": {"max_result_window": 20000}})
    if response.get("acknowledged"):
        print("Index settings updated successfully.")
    else:
        print("Failed to update index settings.")
  except TransportError as e:
      print(f"Failed to update index settings: {e}")