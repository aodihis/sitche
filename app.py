from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
from controllers.scrapper_controller import scrape_bp
app = Flask(__name__)


app.register_blueprint(scrape_bp)
if __name__ == '__main__':
    app.run(debug=True)
