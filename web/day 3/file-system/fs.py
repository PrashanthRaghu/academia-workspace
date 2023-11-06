import os

from flask import Flask
from flask import request, send_file


import exceptions

app = Flask(__name__)


@app.route('/api/files/', methods=['POST'])
def create_file():
    log_message = {
        'operation': 'create file',
        'status': 'processing'
    }

    app.logger.info(str(log_message))

    file_path = os.getcwd() + '\storage\\'
    data = dict(request.form)
    file_name = data.get('name')
    file_id = data.get('file_id')

    file = request.files['file']

    overwrite = data.get('overwrite', False)

    if not overwrite and os.path.isfile(file_id):
        log_message['status'] = 'unsuccessful'
        log_message['reason'] = 'File Already exists'
        app.logger.error(str(log_message))
        err = exceptions.FileExistsException()
        return str(err), err.status
    else:
        log_message['status'] = 'successful'
        app.logger.info(str(log_message))
        file.save(file_path + file_id)
        return "", 200


@app.route('/api/files/<file_id>', methods=['GET'])
def get_file(file_id):
    log_message = {
        'operation': 'get file',
        'status': 'processing'
    }

    app.logger.info(str(log_message))

    file_path = os.getcwd() + '\storage\\{}'.format(file_id)

    if not os.path.isfile(file_path):
        log_message['status'] = 'unsuccessful'
        log_message['reason'] = 'File Does not exist'
        app.logger.error(str(log_message))
        err = exceptions.FileDoesNotExistsException()
        return str(err), err.status
    else:
        log_message['status'] = 'successful'
        app.logger.info(log_message)        
        return send_file(file_path), 200
    
@app.route('/api/files/<file_id>', methods=['DELETE'])
def remove_file(file_id):
    log_message = {
        'operation': 'remove file',
        'status': 'processing'
    }

    app.logger.info(str(log_message))

    file_path = os.getcwd() + '\storage\\{}'.format(file_id)

    if not os.path.isfile(file_path):
        log_message['status'] = 'unsuccessful'
        log_message['reason'] = 'File Does not exist'
        app.logger.error(str(log_message))
        err = exceptions.FileDoesNotExistsException()
        return str(err), err.status
    else:
        os.remove(file_path)
        log_message['status'] = 'successful'
        app.logger.info(log_message)        
        return "", 200
    