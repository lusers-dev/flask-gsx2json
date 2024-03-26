import re
import json
import csv
import sys
from six.moves import urllib
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = "super-secret-flask-key-e3b0c44298fc1c149afbf4c8996fb9"


def json_pretty_print(json_dict):
    """pretty print json data"""
    return json.dumps(json_dict,
                      indent=2,
                      sort_keys=True)


def gsx2json(gsx_id):
    '''Construct URL'''

    '''sheet permissions must be to anyone with link'''
    url = '{}{}{}'.format(
            'https://docs.google.com/spreadsheets/d/',
            str(gsx_id),
            '/export?gid=0&format=csv'
            )

    req = urllib.request.Request(url) 

    results_list = []

    response = None
    try:
        response = urllib.request.urlopen(req, timeout=10)
        if response:
            for r_line in response.read().decode('utf-8').splitlines():
                if r_line.strip():
                    results_list.append(r_line.strip()) 
    except urllib.error.HTTPError as e:
        return e.read()

    json_obj = []

    if len(results_list) > 0:
        try: 
            reader = csv.DictReader(results_list) 

        except Exception as e:
            return e.read()
            #pass
        
        if reader: 
            for row in reader: 
                json_obj.append(row)

            if len(json_obj) > 0:
                payload = { "rows": json_obj }
                return (json_pretty_print(payload))

@app.route("/")
def gsx2json_index():
    return render_template("index.html")


@app.route("/gsx2json/", methods=['POST', 'GET'])
def gsx2json_process():
    output = None
    entry = None

    try:
        '''require variable gsx_id and error handler'''
        if not 'gsx_id' in request.args or not request.args['gsx_id']:
            return str('Google Sheet ID Required!')

        if request.args['gsx_id']:
            try:
                entry = str(request.args['gsx_id'])
            except Exception as e:
                return flash(e) 
                #pass

    except Exception as e:
        return flash(e)
        #pass

    if entry:
        try: 
            output = gsx2json(entry)

        except Exception as e:
            return flash(e)
            #pass

    return output


