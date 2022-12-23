import os
import jwt

from flask import Flask, g, jsonify, make_response, request

app = Flask(__name__)

UNAUTHORIZED_CODE = 401
SUCCESS_WITH_UPDATE = 201

@app.route('/')
def home():
    return make_response(
        jsonify({
            'ping': 'poing',
        }),
        201
    )

@app.route('/api/v0/goods/return', methods=['POST'])
def return_goods():

    token = request.headers.get('Authorization').split(' ').pop()
    payload = {}

    response_code = UNAUTHORIZED_CODE
    response_message = {
        'response': 'Failure',
        'reason': 'Unauthorizaed'
    }

    try:
        payload = jwt.decode(
            token, 
            os.environ.get('SECRET_KEY', 'super-secret-token'),
            algorithms=['HS256']
        )

        if 'Jane Doe' != payload.get('name', 'Jane Doe') :
            response_message['response'] = 'Success'
            response_message['reason'] = 'Action complete'
            response_code = SUCCESS_WITH_UPDATE
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
        'iss', 'sub', 'aud', 'iat', 'exp',
    ]).difference(set(doc.keys()))

    response_message = {
        'response': 'Success',
        'reason': 'Action complete'
    }
    response_code = SUCCESS_WITH_UPDATE

    if bool(fields_compare):
        response_message = {
            'response': 'Failure',
            'reason': 'Invalid format'
        }
        response_code = UNAUTHORIZED_CODE

    return response_code, response_message

@app.route('/api/v0/secret-key', methods=['GET'])
def get_secret_keys():
    return make_response(
        jsonify({
            'key': os.environ.get('SECRET_KEY')
        }),
        SUCCESS_WITH_UPDATE
    )
