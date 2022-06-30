from asyncio.log import logger
from flask import Blueprint, request, make_response
from src.services.AdminService import AdminService


admin = Blueprint('admin', __name__)

@admin.route('/register', methods=['POST'])
def create_admin():
    data = request.get_json()

    try:
        new_admin = AdminService().add_admin(username=data.get('username'), password=data.get('password'), email=data.get('email'), fullName=data.get('fullName'), status=data.get('status'))

        response = make_response({"status": "success", "message": "New admin created", "data": new_admin})
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 201
        return response

    except:
        #server error 
        # response = make_response({"status": "error", "message": "Server fail"})
        # response.status_code = 500
        # response.headers['Content-Type'] = 'application/json'
        return logger.error()