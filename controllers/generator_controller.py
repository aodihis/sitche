from flask import Blueprint, request, make_response, send_file, Response
import pandas as pd
from io import BytesIO, StringIO
from schema.xls_generator import schema as xlsjsonschema
from schema.sitemap_generator import schema as sitemapjsonschema
from jsonschema import validate, ValidationError
import xml.etree.ElementTree as et
from xml.dom import minidom
from urllib.parse import urljoin, urlparse

# Define the blueprint for the scrape controller
generator_bp = Blueprint('file_generator_bp', __name__)

# format json { 
# "filename" : "excel",
# "sheet": 
#  [
#    { 
#    "title" : "Sheet1", 
#    "data" : 
#     {"header": ["A", "A2"], 
#      "data":[["data1", "data2"], ["data1", "data2"]]
#     }
#  }
#  ]
# }
@generator_bp.route('/download-xls', methods=['POST'])
def xls_generator():
    if request.headers['Content-Type'] != 'application/json':
        return Response("Invalid content type", status=415)
    content = request.json

    try:
        # Validate the JSON data against the schema
        validate(instance=content, schema=xlsjsonschema)
        print("JSON is valid and correctly formatted.")
    except ValidationError as e:
        print(f"JSON is not valid: {e.message}")
        return Response("JSON is not valid", status=415)

    output = BytesIO()
    writter = pd.ExcelWriter(output, engine='xlsxwriter')
    for sheet in content['sheet']:
        dataFrame  = {}
        for i, header in enumerate(sheet['data']['header']):
            dataFrame[header] = {}
            for id, data in enumerate(sheet['data']['data']):
                dataFrame[header][id] = data[i]
        df = pd.DataFrame(dataFrame)
        df.to_excel(writter, sheet_name=sheet['title'])
    writter.close()
    output.seek(0)
    response = make_response(send_file(output, download_name=f"{content['filename']}.xlsx", as_attachment=True))
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    return response

# json format
# {
#     "urls" :[ 'url1', 'url2', 'url3']
# }
@generator_bp.route('/generate-sitemap', methods=['POST'])
def generate_sitemap():
    if request.headers['Content-Type'] != 'application/json':
        return Response("Invalid content type", status=415)
    content = request.json

    try:
        # Validate the JSON data against the schema
        validate(instance=content, schema=sitemapjsonschema)
        print("JSON is valid and correctly formatted.")
    except ValidationError as e:
        print(f"JSON is not valid: {e.message}")
        return Response("JSON is not valid", status=415)
    
    urlset = et.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')

    urls = set()
    for url in content['urls']:
        urls.add(urljoin(url, urlparse(url).path))
    for url in urls:
        url_element = et.SubElement(urlset, 'url')
        loc = et.SubElement(url_element, 'loc')
        loc.text = url
    xml_str = minidom.parseString(et.tostring(urlset)).toprettyxml(indent="  ")
    output = BytesIO()
    output.write(str.encode(xml_str))
    output.seek(0)
    return send_file(output, download_name="sitemap.xml", as_attachment=True, mimetype="application/xml")