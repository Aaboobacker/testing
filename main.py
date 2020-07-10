from flask import Flask, flash, jsonify, request, render_template, redirect
import requests
import json
import os 
from flask import send_from_directory 

app = Flask(__name__)
app.secret_key = "ugugku8687678t34yr78fgwi"


@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/<resource_id>', methods=['GET', 'POST'])
def home(resource_id):
    print(resource_id)
    if resource_id == 'favicon.ico':
        return render_template('home.html')

    url = "https://demo.ckan.org/api/3/action/datastore_search?resource_id={}&limit=5".format(
        resource_id)

    payload = {}
    headers = {
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    response = json.loads(response.text)

    fields = []
    for f in response['result']['fields']:
        fields.append(f['id'])

    return render_template('home.html', fields=fields, resource_id=resource_id)


@app.route('/b/addcolumn')
def addcolumn1(methods=['POST']):
    print(resource_id)
    if resource_id == 'favicon.ico':
        return render_template('addcolumn.html')
    fieldname = ''
    fieldtype = ''
    print("here")
    print(request.method)
    if request.method == 'GET':
        return render_template('addcolumn.html', fieldname=fieldname, fieldtype=fieldtype, resource_id=resource_id)
    
    elif request.method=='POST':
        fieldname = request.form['fieldname']
        fieldtype = request.form['fieldtype']

        url = "https://demo.ckan.org/api/3/action/datastore_search?resource_id={}&limit=5".format(
            resource_id)

        payload = {}
        headers = {
            'Authorization': 'ebb2e3c2-d11d-48dc-875b-cf0790d36f45'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        response = json.loads(response.text)

        fields = []
        fields = response['result']['fields']
            
        print("fieldsNames", fields)
        # fields.append({"type": fieldtype, "id": fieldname})
        # url = "http://demo.ckan.org/api/3/action/datastore_create"
        # payload = {
        #     "resource_id": resource_id,
        #     "fields": ,
        #     "force": "True",
        #     "primary_key": "Name"
        # }
        # response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        return render_template('addcolumn.html', fieldname=fieldname, fieldtype=fieldtype, resource_id=resource_id)


@app.route('/addRow', methods=['GET', 'POST'])
def addRow():
    _dict = {}
    for i in request.form:
        if i != "_id" and i != "resource_id":
            _dict[i] = request.form[i]
    print(_dict)

    resource_id = request.form['resource_id']

    try:
        for key, value in _dict.items():
            if not value:
                flash("Empty fields not allowed, fill all the form")
                return redirect('/'+resource_id)
    except:
        return redirect('/'+resource_id)

    url = "https://demo.ckan.org/api/3/action/datastore_upsert"

    payload = {"resource_id": resource_id,
               "records": [
                   _dict
               ],
               "force": "True",
               "method": "insert"
               }
    headers = {
        'Authorization': 'ebb2e3c2-d11d-48dc-875b-cf0790d36f45',
        'Content-Type': 'application/json',
        'Cookie': '__cfduid=d91f976fabc7324436f6938a97f4855461594151177'
    }
    print(url)
    print(payload)
    response = requests.request(
        "POST", url, headers=headers, data=json.dumps(payload))

    response = json.loads(response.text)

    try:
        if response['success']:
            flash('Data Addeed')
        else:
            flash('Some error occured')
    except:
        flash('Some error occured')
    return redirect('/'+resource_id)

@app.route('/<resource_id>/addcolumn', methods=['GET', 'POST'])
def addcolumn(resource_id):
    fieldname = ''
    fieldtype = ''
    if request.method=='GET':
        return render_template('addcolumn.html', fieldname=fieldname, fieldtype=fieldtype, resource_id=resource_id)
        # return('<form action="/test" method="post"><input type="submit" value="Send" /></form>')

    elif request.method=='POST':
        fieldname = request.form['fieldname']
        fieldtype = request.form['fieldtype']

        url = "https://demo.ckan.org/api/3/action/datastore_search?resource_id={}&limit=5".format(
            resource_id)

        payload = {}
        headers = {
            'Authorization': 'ebb2e3c2-d11d-48dc-875b-cf0790d36f45'
        }

        # get previous columns
        response = requests.request("GET", url, headers=headers, data=payload)

        response = json.loads(response.text)

        fields = []
        fields = response['result']['fields']
        
        for i in range(len(fields)): 
            if fields[i]['id'] == '_id': 
                del fields[i] 
                break
        # print("fieldsNames", fields)

        # add new column
        fields.append({"type": fieldtype, "id": fieldname})
        # url = "https://demo.ckan.org/api/3/action/datastore_create"
        payload = {
            "resource_id": resource_id,
            "fields": fields,
            "force": "True"
        }
        
        # print(url)
        # print(payload)
        # response = requests.request("POST", url, headers=headers, data=payload)
        # response = json.loads(response.text)
        # print(response)

        url = "https://demo.ckan.org/api/3/action/datastore_create"

        # payload = {"resource_id": "0314ad53-92ea-48a5-8bf0-a991e6cf41f2",
        #     "fields": [                {            "type": "text",            "id": "Name"        },        {            "type": "numeric",            "id": "Age"        },        {            "type": "text",            "id": "Country"        },        {            "type": "timestamp",            "id": "Date"        },        {            "type": "numeric",            "id": "Number"        },        {            "type": "text",            "id": "Address"        },        {            "type": "text",            "id": "abcd"        }    ],    "force": "True"}
        headers = {
        'Authorization': 'ebb2e3c2-d11d-48dc-875b-cf0790d36f45',
        'Content-Type': 'application/json',
        'Cookie': '__cfduid=d91f976fabc7324436f6938a97f4855461594151177'
        }
        print(payload)

        response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
        print(response.text.encode('utf8'))
        response = json.loads(response.text)
        try:
            if response['success']:
                flash('Column Addeed')
            else:
                flash('Some error occured')
        except:
            flash('Some error occured')
        return render_template('addcolumn.html', fieldname=fieldname, fieldtype=fieldtype, resource_id=resource_id)
    else:
        return("ok")


@app.route('/<resource_id>/search', methods=['GET', 'POST'])
def test(resource_id):
    if request.method=='GET':
        return render_template('search.html', resource_id=resource_id)

    elif request.method=='POST':
        value = request.form['value']
        url = "https://demo.ckan.org/api/3/action/datastore_search?q={}&resource_id={}".format(value,resource_id)

        payload = {}
        headers = {
            'Authorization': 'ebb2e3c2-d11d-48dc-875b-cf0790d36f45'
        }

        # get previous columns
        response = requests.request("GET", url, headers=headers, data=payload)

        response = json.loads(response.text)
        # print(response)

        fields = []
        result = {}
        for f in response['result']['fields']:
            if response['result']['records']:
                record = response['result']['records'][0]
                
                result[f['id']] = record[f['id']]
            else:
                result[f['id']] = ''

        
        # if response['result']['records']:
        #     result = response['result']['records'][0]
        print(result)
        return render_template('upsert.html', dictionary = result, resource_id=resource_id)
    else:
        return("ok")


@app.route('/upsert', methods=['GET', 'POST'])
def upsert():
    _dict = {}
    for i in request.form:
        if i != "_id" and i != "resource_id":
            _dict[i] = request.form[i]
    print(_dict)

    resource_id = request.form['resource_id']

    try:
        for key, value in _dict.items():
            if not value:
                flash("Empty fields not allowed, fill all the form")
                return redirect('/'+resource_id + '/search')
    except:
        return redirect('/'+resource_id)

    url = "https://demo.ckan.org/api/3/action/datastore_upsert"

    payload = {"resource_id": resource_id,
               "records": [
                   _dict
               ],
               "force": "True",
               "method": "upsert"
               }
    headers = {
        'Authorization': 'ebb2e3c2-d11d-48dc-875b-cf0790d36f45',
        'Content-Type': 'application/json',
        'Cookie': '__cfduid=d91f976fabc7324436f6938a97f4855461594151177'
        }
    print(url)
    print(payload)
    response = requests.request(
        "POST", url, headers=headers, data=json.dumps(payload))

    response = json.loads(response.text)

    try:
        if response['success']:
            flash('Data Addeed')
        else:
            flash('Some error occured')
    except:
        flash('Some error occured')
    return redirect('/'+resource_id + '/search')

app.run(port=5000, debug=True)
