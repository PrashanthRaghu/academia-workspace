
from flask import Flask
from flask import request, make_response

import jwt

import exceptions

app = Flask(__name__)

@app.route('/api/token/<int:employee_id>', methods=['POST'])
def fetch_token(employee_id):
    log_message = {
        'operation': 'fetch token',
        'status': 'processing'
    }

    app.logger.info(str(log_message))

    payload = {
        'id': employee_id,
        'iss': 'DSCE',
        'sub': 'Employee Microservice Token'
    }

    try:
        token = jwt.encode(payload, 
                           key="mysecretkey")
        
    except:
        log_message['status'] = 'unsuccessful'
        log_message['reason'] = 'Token generation error'
        app.logger.error(str(log_message))
        err = exceptions.TokenGenerationError()
        return str(err), err.status

    app.logger.info(str(log_message))
    return {'token': token}, 200

