from werkzeug.security import check_password_hash
from flask_login import login_user


import jwt
import datetime
from src.exceptions.InvariantError import InvariantError

from src.models.AdminModel import Admin as AdminModel


class AuthService:
    def login_admin(self, username, password):
        admin = AdminModel.query.filter_by(username=username).first()
        if not admin:
            raise InvariantError(message="User not found", status_code=404)
        
        logged_in = check_password_hash(admin.password, password)
        # check password user
        if not logged_in:
            raise InvariantError(message="Wrong password", status_code=401)
        
        token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'secret', algorithm='HS256')
        login_user(admin)

        user_data = {
            "admin_id": admin.admin_id,
            "email" : admin.email,
            "username" : admin.username,
            "fullName" : admin.full_name,
            "token": token
        }

        return user_data