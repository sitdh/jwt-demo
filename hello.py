import os
from flask import Flask, g, jsonify, make_response, request
import jwt

# from dotenv import load_dotenv
# load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return make_response(
        jsonify({
            'ping': 'poing',
        }),
        200
    )

@app.route('/api/v0/goods/return', methods=['POST'])
def return_goods():

    token = request.headers.get('Authorization').split(' ').pop()
    payload = {}

    response_code = 401
    response_message = {
        'Response': 'Fail',
        'Reason': 'Not authorizaed'
    }

    try:
        payload = jwt.decode(
            token, 
            os.environ.get('SECRET_KEY', 'super-secret-token'),
            algorithms=['HS256']
        )

        if 'Jane Doe' != payload.get('name', 'Jane Doe') :
            response_message['Response'] = 'Success'
            response_message['Reason'] = 'Action complete'
            response_code = 200
        else:
            response_code, response_message = field_validation(request.json)
    except:
        pass

    return make_response(
        jsonify(response_message),
        response_code
    )

def field_validation(doc):
    fields_compare = set([
        # Mandatory fields
        'doc_no', 'reference_doc_no', 'request_type'
    ]).difference(set(doc.keys()))

    response_message = {
        'Response': 'Success',
        'Reason': 'Action complete'
    }
    response_code = 201

    if bool(fields_compare):
        response_message = {
            'Response': 'Fail',
            'Reason': 'Invalid format'
        }
        response_code = 401

    return response_code, response_message

@app.route('/api/v0/secret-key', methods=['GET'])
def get_secret_keys():
    return make_response(
        jsonify({
            'key': os.environ.get('SECRET_KEY')
        }),
        200
    )
