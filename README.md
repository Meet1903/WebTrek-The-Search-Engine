# Web Trek - The Search Engine

Welcome to WebTrek, your new search engine built with Python and powered by ElasticSearch. WebTrek combines cutting-edge technology with intuitive design to revolutionize the way you explore the vast realm of the internet.

At its core, WebTrek utilizes ElasticSearch, a powerful and scalable search engine, to index and search through a vast array of web content rapidly and efficiently. Whether you're looking for articles, blog posts, product reviews, or any other type of online content, WebTrek provides lightning-fast search results tailored to your needs.

But WebTrek doesn't stop there. In addition to its robust search capabilities, it also features a sophisticated web scraper component. This allows WebTrek to autonomously traverse the web, collecting fresh data from various sources to ensure that its index remains up-to-date and comprehensive.

## Setup:

1. **ElasticSearch Installation:** Ensure ElasticSearch is installed and running on your machine. Follow the steps outlined in the [ElasticSearch download](https://www.elastic.co/downloads/elasticsearch) page for installation instructions.

2. **Generate API Key:** Create an API key for performing operations on ElasticSearch using Python. You can refer to the guide on [how to generate an API key](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-create-api-key.html). Alternatively, you can use Kibana to generate the API key via its UI. Install Kibana from the [Kibana download page](https://www.elastic.co/downloads/kibana) and refer to the [API keys documentation](https://www.elastic.co/guide/en/kibana/current/api-keys.html) for assistance. 

3. **Update API Key:** After generating the API key, capture the api_key value and update the "api_key" variable in elastic_logics.py as follows:

```
client = Elasticsearch(
  "https://localhost:9200",
  api_key="YOUR_API_KEY",
  verify_certs=False
)
```
Ensure to replace YOUR_API_KEY_HERE with the actual API key obtained in the previous step.

4. **Install Dependencies:** Install all dependencies using below command:

```
pip install -r requirements.txt
```

By following these setup instructions, you'll be ready to utilize ElasticSearch for WebTrek seamlessly.

## Data Gathering


Navigate to the "Go to Scraper" button and click on it to access the Scraper component of WebTrek. Here, you'll have the opportunity to input the webpage or domain you wish to include in your search engine's index. Additionally, you'll be prompted to specify the path where temporary HTML files will be stored on your local machine.

Once you've provided this information, simply click on the "Scrape" button to initiate the scraping process. WebTrek will then gather the data from the specified webpage/domain and store it in your ElasticSearch node. Once completed, the scraped data will be seamlessly integrated into your search engine, ready for utilization.


## Run the program
Once the setup is done. Run main.py using below command.
```
python main.py
```
