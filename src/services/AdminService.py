from unittest import result
from werkzeug.security import generate_password_hash
from nanoid import generate
from src import db
from datetime import datetime
from src.models.AdminModel import Admin as AdminModel

class AdminService:
    def add_admin(self, username, email, password, fullName, status):
        hashed_password = generate_password_hash(password, method='sha256')
        new_admin = AdminModel(admin_id=f'admin-{generate(size=16)}', username=username, email=email, password=hashed_password, full_name=fullName, status=status, created_at=datetime.now())

        db.session.add(new_admin)
        db.session.commit()

        result = {'admin_id': new_admin.admin_id, 'username': new_admin.username, 'email': new_admin.email, 'fullName': new_admin.full_name, 'created_at': new_admin.created_at}
        return result