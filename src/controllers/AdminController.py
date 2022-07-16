import logging
from flask import Blueprint, render_template, request, make_response, url_for, redirect
from jsonschema import ValidationError, validate
from src.validators.AdminValidator import admin_schema
from src.services.AdminService import AdminService
from src.exceptions.InvariantError import InvariantError


admin = Blueprint('admin', __name__)

@admin.route('/register', methods=['GET', 'POST'])
def create_admin():
    if request.method == 'POST':
        data = request.form.to_dict()

        try:
            if data.get('password') != data.get('confirm-password'):
                raise ValidationError(message='Password and confirm password does not match!')
            validate(instance=data, schema=admin_schema)
            new_admin = AdminService().add_admin(username=data.get('username'), password=data.get('password'), email=data.get('email'), fullName=data.get('fullname'), roles='admin', status=True)

            response = make_response({"status": "success", "message": "New admin created", "data": new_admin})
            response.headers['Content-Type'] = 'application/json'
            response.status_code = 201
            return redirect(url_for('auth.login'))

        except ValidationError as e:
            response = make_response({"status": "error", "message": e.schema.get('message')[e.validator]})
            response.status_code = 400
            response.headers['Content-Type'] = 'application/json'
            print(logging.exception("message"))
            return response
        
        except InvariantError as e:
            response = make_response({"status": "error", "message": e.message})
            response.status_code = e.status_code
            response.headers['Content-Type'] = 'application/json'
            print(logging.exception("message"))
            return response

        except:
            #server error 
            response = make_response({"status": "error", "message": "Server fail"})
            response.status_code = 500
            response.headers['Content-Type'] = 'application/json'
            print(logging.exception("message"))
            return render_template('home/page-500.html')

    return render_template('home/register.html')