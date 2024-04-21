from flask import Flask, render_template, request, redirect, url_for
from data_scrapper import *
from elastic_logics import insert_data_elastic
import os

app = Flask(__name__)

def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/scrapper")
def scrapper():
    return render_template("scrapper.html")

@app.route("/scrapper", methods=["POST"])
def scrape():
    if request.method == "POST":
        # Get form data
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

if __name__ == "__main__":
    app.run(debug=True)
