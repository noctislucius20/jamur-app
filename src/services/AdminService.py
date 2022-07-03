from sqlalchemy import or_
from werkzeug.security import generate_password_hash
from nanoid import generate
from src import db
from datetime import datetime
from src.models.AdminModel import Admin as AdminModel
from src.exceptions.InvariantError import InvariantError

class AdminService:
    def add_admin(self, username, email, password, fullName, status):
        self.check_user_exists(username, email)
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = AdminModel(admin_id=f'admin-{generate(size=16)}', username=username, email=email, password=hashed_password, full_name=fullName, status=status, created_at=datetime.now())

        db.session.add(new_admin)
        db.session.commit()

        result = {'admin_id': new_admin.admin_id, 'username': new_admin.username, 'email': new_admin.email, 'fullName': new_admin.full_name, 'created_at': new_admin.created_at}
        return result
    
    def check_user_exists(self, username, email):
        admin = AdminModel.query.filter(or_(AdminModel.username==username, AdminModel.email==email)).first()

        if admin:
            raise InvariantError(message="Admin already exist", status_code=400)
