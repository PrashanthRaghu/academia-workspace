
from flask import request
import jwt

from app import app

from exceptions.auth import *

def authenticate_request(called):
    def f(*args, **kwargs):
        auth_header = request.headers.get('X-Auth-Header')
        log_message = {'operation': 'auth_user', 'status': 'processing'}
        app.logger.info(log_message)

        if not auth_header:
            log_message['status'] = 'unsuccessful'
            log_message['reason'] = 'Token header missing'
            app.logger.info(log_message)
            return str(TokenMissingError()), 403

        try:
            payload = jwt.decode(auth_header, 
                                 "mysecretkey",
                                 algorithms='HS256')
        except Exception as e:
            log_message['status'] = 'unsuccessful'
            log_message['reason'] = 'Token invalid'
            app.logger.error(e)
            return str(TokenInvalidError()), 403
        
        log_message['status'] =  'successful'
        app.logger.info(log_message)
        return called(*args, **kwargs)

    f.__name__ = called.__name__
    return f