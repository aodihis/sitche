from flask import Blueprint, request, make_response, send_file, Response
import requests
import services.scrapper
import json
import pandas as pd
from io import BytesIO
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
