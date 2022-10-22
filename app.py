
from flask import Flask, request, make_response
import json
import apihelpers as apih
import dbhelpers as dbh
from flask_cors import CORS
from dbcreds import production_mode

app = Flask(__name__)
CORS(app)


@app.post('/api/painting')
def new_painting():
    is_valid = apih.check_endpoint_info(request.json, ['artist', 'date_painted', 'img_url', 'name'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    results = dbh.run_statement('CALL new_painting(?,?,?,?)', 
    [request.json.get('artist'), request.json.get('date_painted'), request.json.get('img_url'), request.json.get('name')])    

    if(type(results) == list):
        return make_response(json.dumps(results[0][0], default=str), 200)
    else:
        return make_response(json.dumps('Sorry, Error', default=str), 500)

@app.get('/api/painting')
def get_paintings():
    is_valid = apih.check_endpoint_info(request.args, ['artist'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    results = dbh.run_statement('CALL get_paintings(?)', [request.args.get('artist')])

    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)    

@app.get('/api/painting')
def get_artist():

    results = dbh.run_statement('CALL get_artist()')

    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)


if(production_mode == True):
    print("running in Production Mode")
    app.run(debug=True)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode")
    app.run(debug=True)



