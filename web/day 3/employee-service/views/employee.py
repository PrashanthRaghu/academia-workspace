import time
import os
import uuid

from flask import request, make_response, send_file
from flask import Blueprint

from models import employee
from services.fs import FileManager
from exceptions.exceptions import *
from observability import setup_logger, time_request, setup_tracing

from auth.auth_middleware import authenticate_request

app_employee = Blueprint('employee', __name__)

count = 0
manager = FileManager()

PIC_FOLDER = 'C:\\Users\\Prashanth\\workspace\\web\\day 3\\employee-service\\pics'

@app_employee.route("/api/employee/", methods=["POST"])
@setup_logger
@time_request
@setup_tracing
@authenticate_request
def create_employee():
    global count
    emp = request.json
    count += 1

    emp = employee.Employee(emp['name'], count, emp['address'])

    log_message = {'tracking_id': request.req_id,
                    'operation': 'create employee',
                    'status': 'processing'}
    
    request.logger.info(str(log_message))
    # Validation error
    if not emp.validate():
        log_message['status'] = 'unsuccessful'
        request.logger.error(str(log_message))
        err = ValidationError()
        return str(err), err.status
    
    emp.save()
    log_message['status'] = 'successful'
    request.logger.info(str(log_message))
    return str(emp), 201

@app_employee.route("/api/employee/<int:employee_id>", methods=["PUT"])
@setup_logger
@time_request
@setup_tracing
@authenticate_request
def alter_employee_data(employee_id):
    emp_req = request.json
    emp_to_change = None

    log_message = { 'tracking_id': request.req_id,
                    'operation': 'alter employee',
                    'status': 'processing'}
    
    request.logger.info(str(log_message))

    emp = employee.Employee('', employee_id, '')
    emp_to_change = emp.get_by_id()

    log_message = { 'tracking_id': request.req_id,
                    'operation': 'alter employee',
                    'status': 'processing'}
    
    if not emp_to_change:
        log_message['status'] = 'unsuccessful'
        log_message['reason'] = 'Employee not present'
        request.logger.error(log_message)
        err = EmployeeNotPresentError()
        return str(err), err.status
    
    emp_to_validate = employee.Employee(emp_req.get('name', ''), 
                                        employee_id, emp_req.get('address'))

    if not emp_to_validate.validate():
        log_message['status'] = 'unsuccessful'
        log_message['reason'] = 'Invalid input data'
        request.logger.error(log_message)
        err = ValidationError()
        return str(err), err.status
    
    emp_to_change.name = employee.get('name', emp_to_change.name)
    emp_to_change.address = employee.get('address', emp_to_change.address)

    emp_to_change.save()
    request.logger.info(str(log_message))

    log_message['status'] = 'successful'

    request.logger.info(str(log_message))
    return str(emp_to_change), 200

@app_employee.route("/api/employee/<int:employee_id>", methods=["GET"])
@setup_logger
@setup_tracing
@time_request
@authenticate_request
def get_employee_information(employee_id):
    
    log_message = {
        'tracking_id': request.req_id,
        'operation': 'get employee',
        'status': 'processing'
    }

    request.logger.info(log_message)

    emp = employee.Employee('', employee_id, '')
    emp = emp.get_by_id()

    if not emp:
        log_message['status'] = 'unsuccessful'
        log_message['reason'] = 'Employee not present'
        request.logger.error(log_message)
        err = EmployeeNotPresentError()
        return str(err), err.status
    
    log_message['status'] = 'successful'
    request.logger.error(log_message)
    return str(emp), 200

@app_employee.route("/api/employee/<int:employee_id>", methods=["DELETE"])
@setup_logger
@setup_tracing
@time_request
@authenticate_request
def remove_employee_data(employee_id):
    try:
        emp = employee.Employee('', employee_id, '')
        emp.delete()
    except KeyError as e:
        err = EmployeeNotPresentError()
        return str(err), err.status
    
    return make_response(""), 200

@app_employee.route("/api/employee/<int:employee_id>/profile_pic", methods=["POST"])
@setup_logger
@setup_tracing
@time_request
@authenticate_request
def upload_profile_pic(employee_id):

    log_message = {
        'tracking_id': request.req_id,
        'operation': 'upload profile pic',
        'status': 'processing'
    }

    request.logger.info(log_message)

    profile_pic = request.files['picture']

    emp = employee.Employee('', employee_id, '').get_by_id()

    if not emp:
        log_message['status'] = 'unsuccessful'
        log_message['reason'] = 'Employee not present'
        request.logger.error(log_message)

        err = EmployeeNotPresentError()
        return str(err), err.status

    profile_pic_name = str(employee_id)

    if profile_pic:
        profile_pic.save('{}/{}.png'.format(PIC_FOLDER, employee_id))
        log_message['status'] = 'successful'
        request.logger.info(log_message)
        return '', 200
    else:
        log_message['status'] = 'unsuccessful'
        log_message['reason'] = 'File not uploaded'
        request.logger.error(log_message)

        err = FileMissingInUploadError()
        return str(err), err.status

@app_employee.route("/api/employee/<int:employee_id>/profile_pic", methods=["DELETE"])
@setup_logger
@setup_tracing
@time_request
@authenticate_request
def remove_profile_pic(employee_id):
    log_message = {
        'tracking_id': request.req_id,
        'operation': 'remove profile pic',
        'status': 'processing'
    }

    request.logger.info(log_message)
    emp = employee.Employee('', employee_id, '').get_by_id()

    if not emp:
        log_message['status'] = 'unsuccessful'
        log_message['reason'] = 'Employee not present'
        request.logger.error(log_message)
        err = EmployeeNotPresentError()
        return str(err), err.status

    if not os.path.isfile('{}/{}.png'.format(PIC_FOLDER, employee_id)):
        # Non-Critical error
        log_message['status'] = 'unsuccessful'
        log_message['reason'] = 'no file to delete'
        request.logger.error(log_message)
        return str(NoFileToDeleteError()), 400
    else:
        log_message['status'] = 'successful'
        os.remove('{}/{}.png'.format(PIC_FOLDER, employee_id))
        request.logger.info(log_message)
        return "", 200

@app_employee.route("/api/employee/<int:employee_id>/profile_pic", methods=["GET"])
@setup_logger
@setup_tracing
@time_request
@authenticate_request
def download_profile_pic(employee_id):
    log_message = {
        'tracking_id': request.req_id,
        'operation': 'download profile pic',
        'status': 'processing'
    }

    request.logger.info(log_message)
    emp = employee.Employee('', employee_id, '').get_by_id()

    if not emp:
        log_message['status'] = 'unsuccessful'
        log_message['reason'] = 'Employee not present'
        request.logger.error(log_message)
        err = EmployeeNotPresentError()
        return str(err), err.status

    if not os.path.isfile('{}/{}.png'.format(PIC_FOLDER, employee_id)):
        # Non-Critical error
        log_message['status'] = 'unsuccessful'
        log_message['reason'] = 'no profile file to download'
        request.logger.error(log_message)
        return str(NoFileToDownloadError()), 400
    else:
        return send_file('{}/{}.png'.format(PIC_FOLDER, employee_id), as_attachment=False), 200


@app_employee.route("/v2/api/employee/<int:employee_id>/profile_pic", methods=["POST"])
@setup_logger
@setup_tracing
@time_request
@authenticate_request
def upload_profile_pic_v2(employee_id):

    log_message = {
        'tracking_id': request.req_id,
        'operation': 'upload profile pic',
        'status': 'processing'
    }

    request.logger.info(log_message)

    profile_pic = request.files['picture']

    emp = employee.Employee('', employee_id, '').get_by_id()

    if not emp:
        log_message['status'] = 'unsuccessful'
        log_message['reason'] = 'Employee not present'
        request.logger.error(log_message)

        err = EmployeeNotPresentError()
        return str(err), err.status

    profile_pic_name = str(employee_id)

    if profile_pic:
        profile_pic.save('{}/{}.png'.format(PIC_FOLDER, employee_id))
        emp.pic_id = str(uuid.uuid4())

        manager.create('{}/{}.png'.format(PIC_FOLDER, employee_id), emp.pic_id)
        emp.save()

        os.remove('{}/{}.png'.format(PIC_FOLDER, employee_id))

        log_message['status'] = 'successful'
        request.logger.info(log_message)
        return '', 200
    else:
        log_message['status'] = 'unsuccessful'
        log_message['reason'] = 'File not uploaded'
        request.logger.error(log_message)

        err = FileMissingInUploadError()
        return str(err), err.status

@app_employee.route("/v2/api/employee/<int:employee_id>/profile_pic", methods=["DELETE"])
@setup_logger
@setup_tracing
@time_request
@authenticate_request
def remove_profile_pic_v2(employee_id):
    log_message = {
        'tracking_id': request.req_id,
        'operation': 'remove profile pic',
        'status': 'processing'
    }

    request.logger.info(log_message)
    emp = employee.Employee('', employee_id, '').get_by_id()

    if not emp:
        log_message['status'] = 'unsuccessful'
        log_message['reason'] = 'Employee not present'
        request.logger.error(log_message)
        err = EmployeeNotPresentError()
        return str(err), err.status

    if not os.path.isfile('{}/{}.png'.format(PIC_FOLDER, employee_id)):
        # Non-Critical error
        log_message['status'] = 'unsuccessful'
        log_message['reason'] = 'no file to delete'
        request.logger.error(log_message)
        return str(NoFileToDeleteError()), 400
    else:
        log_message['status'] = 'successful'
        os.remove('{}/{}.png'.format(PIC_FOLDER, employee_id))
        request.logger.info(log_message)
        return "", 200

@app_employee.route("/v2/api/employee/<int:employee_id>/profile_pic", methods=["GET"])
@setup_logger
@setup_tracing
@time_request
@authenticate_request
def download_profile_pic_v2(employee_id):
    log_message = {
        'tracking_id': request.req_id,
        'operation': 'download profile pic',
        'status': 'processing'
    }

    request.logger.info(log_message)
    emp = employee.Employee('', employee_id, '').get_by_id()

    if not emp:
        log_message['status'] = 'unsuccessful'
        log_message['reason'] = 'Employee not present'
        request.logger.error(log_message)
        err = EmployeeNotPresentError()
        return str(err), err.status

    data = manager.fetch(emp.pic_id)
    return data, 200

