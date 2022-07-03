import logging
from functools import wraps
import jwt
from flask import Blueprint, render_template, request, make_response, url_for, redirect, jsonify
from jsonschema import ValidationError, validate
from src.exceptions.InvariantError import InvariantError
from src.services.AuthService import AuthService


auth = Blueprint('auth', __name__)

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        # decode token
        token = request.headers.get('Authorization').replace('Bearer ', '')
        try:
            if not token:
                return make_response(jsonify({'status': 'error', 'message': 'Token is missing!'}), 401)
            output = jwt.decode(token, 'secret', algorithms=['HS256'])
        except:
            return make_response(jsonify({'status': 'Unauthorized', 'message': 'Token is invalid!'}), 401)
        
        return f(*args, **kwargs)
    
    return decorator
        
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form.to_dict()

        try:
            admin = AuthService().login_admin(data['username'], data['password'])
            response = make_response({"status": "success", "data": admin})
            response.headers['Content-Type'] = 'application/json'
            response.status_code=200
            return redirect(url_for('home.index'))
            
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
            return response
    
    return render_template('home/login.html')