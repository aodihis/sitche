from flask import Blueprint, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup

# Define the blueprint for the scrape controller
scrape_bp = Blueprint('scrape_bp', __name__)

@scrape_bp.route('/')
def webpage():
    return render_template('urlscraper.html')

# Define a route for scraping URLs
@scrape_bp.route('/scrape', methods=['POST'])
def scrape():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        # Call the function to scrape URLs from the provided URL
        urls = scrape_urls(url)
        return jsonify(urls)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# The function to scrape URLs
def scrape_urls(start_url):
    # Send a GET request to the provided URL
    response = requests.get(start_url)
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract and return all the URLs found on the page
    return [a['href'] for a in soup.find_all('a', href=True)]
