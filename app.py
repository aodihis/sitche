from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
from controllers.scrapper_controller import scrape_bp
from controllers.generator_controller import generator_bp
from controllers.urlchecker_controller import checker_bp
app = Flask(__name__)


app.register_blueprint(scrape_bp)
app.register_blueprint(generator_bp)
app.register_blueprint(checker_bp)
if __name__ == '__main__':
    app.run(debug=True)
