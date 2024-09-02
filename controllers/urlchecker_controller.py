from flask import Blueprint, request, jsonify, render_template, Response
import requests
from jsonschema import validate, ValidationError
from schema.urlchecker import schema as urlcheckerjsonschema
import services.urlchecker

# Define the blueprint for the scrape controller
checker_bp = Blueprint('checker_bp', __name__)

@checker_bp.route('/url-checker')
def webpage():
    return render_template('urlchecker.html')

# {
#     'urls' : ['url1', 'url2']
# }
@checker_bp.route('/process-url-checker', methods=['POST'])
def checker():
    if request.headers['Content-Type'] != 'application/json':
        return Response("Invalid content type", status=415)
    content = request.json

    try:
        # Validate the JSON data against the schema
        validate(instance=content, schema=urlcheckerjsonschema)
        print("JSON is valid and correctly formatted.")
    except ValidationError as e:
        print(f"JSON is not valid: {e.message}")
        return Response("JSON is not valid", status=415)

    results = services.urlchecker.check(urls=content['urls'])
    return jsonify(results)