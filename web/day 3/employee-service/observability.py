import time
from flask import request, make_response


def setup_logger(called):
    def f(*args, **kwargs):
        from app import app
        request.logger = app.logger
        return called(*args, **kwargs)
    f.__name__ = called.__name__
    return f

def time_request(called):
    def f(*args, **kwargs):
        from app import app
        request.start_time = time.time() * 1000
        res = called(*args, **kwargs)
        request.end_time = time.time() * 1000
        request.time = request.end_time - request.start_time
        app.logger.info('request time: {}'.format(request.time))
        return res
    f.__name__ = called.__name__
    return f

def setup_tracing(called):
    def f(*args, **kwargs):
        request.req_id = 'req_{}'.format(time.time() * 1000)
        res, status = called(*args, **kwargs)
        res_send = make_response(res)
        res_send.headers['X-Request-Id'] = request.req_id
        return res_send, status
    f.__name__ = called.__name__
    return f
