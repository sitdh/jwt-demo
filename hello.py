import os
from dotenv import load_dotenv

from flask import Flask, g, jsonify, make_response, request
import jwt

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return make_response(
        jsonify({
            'ping': 'poing',
        }),
        200
    )

@app.route('/api/v0/goods/return', methods=['GET'])
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
    except:
        pass

    return make_response(
        jsonify(response_message),
        response_code
    )

@app.route('/api/v0/secret-key', methods=['GET'])
def get_secret_keys():
    return make_response(
        jsonify({
            'key': os.environ.get('SECRET_KEY')
        }),
        200
    )
