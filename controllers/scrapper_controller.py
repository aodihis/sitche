from flask import Blueprint, request, jsonify, render_template, Response
import requests
import services.scrapper
import json
import time

# Define the blueprint for the scrape controller
scrape_bp = Blueprint('scrape_bp', __name__)

@scrape_bp.route('/')
def webpage():
    return render_template('urlscraper.html')

# Define a route for scraping URLs
@scrape_bp.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')
    limit = request.args.get('limit', default=100)
    if not url:
        return jsonify({"error": "URL is required"}), 400
    try:
        req = requests.get(url)
        if req.status_code != 200:
            return jsonify({"error": "Invalid url."}),500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    try:
        # Call the function to scrape URLs from the provided URL
        return Response(scrape_sse_generator(url,int(limit)), mimetype="text/event-stream")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def scrape_progress(links: set, external: set, finished:bool):
    if finished:
        yield f"data: {json.dumps({'status': 'complete', 'data': services.scrapper.buildScrapeDict(links, external)})}\n\n"
    else:
        yield f"data: {json.dumps({'status': 'in-progress', 'progress': len(links)})}\n\n"

def scrape_sse_generator(url,limit):
    for progress_update in services.scrapper.scrape(url, limit, generator_callback=scrape_progress):
           yield progress_update
