from flask import Flask, render_template, request, redirect, url_for
from data_scrapper import get_urls, save_html, delete_files_in_folder
from elastic_logics import insert_data_elastic, search_on_elastic, insert_query_history, fetch_history, delete_all_history
from prepare_query import prepare_query
import os

app = Flask(__name__)

def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")

@app.route("/")
def index():
    return render_template("index.html", data=' ')

@app.route("/", methods=["POST"])
def search():
    if request.method == "POST":
        query = request.form.get("query")
        insert_query_history(query)
        clearn_query = prepare_query(query)
        urls, titles = search_on_elastic(clearn_query)
        # final_words = clearn_query
        title_url_pairs = zip(titles, urls)
    return render_template("index.html", title_url_pairs =title_url_pairs)

@app.route("/scrapper")
def scrapper():
    return render_template("scrapper.html")

@app.route("/scrapper", methods=["POST"])
def scrape():
    if request.method == "POST":
        domains = request.form.get("url")
        folder = request.form.get("path")
        domains = domains.replace(" ", "").split(",")
        print(domains, folder)
        urls = get_urls(domains)
        print(folder)
        save_html(urls, folder)
        insert_data_elastic(folder)
        delete_files_in_folder(folder)
        return "Scraping completed successfully!" 

@app.route("/history")
def history():
    next_page = False
    prev_page = False
    current_page = 1
    page = request.args.get('page')
    if page:
        current_page = int(page)

    queries, timestamps = fetch_history(page_number=current_page)
    history = zip(queries, timestamps)

    is_data_on_next_page, _ = fetch_history(page_number=current_page + 1)
    
    if is_data_on_next_page:
        next_page = True
    if current_page > 1:
        prev_page = True
    return render_template("history.html", history=history, current_page = current_page, next_page=next_page, prev_page = prev_page)

@app.route("/history", methods=["POST"])
def clean_history():
    delete_all_history()
    return render_template("history.html", history=None)

if __name__ == "__main__":
    app.run(debug=True)
