from src import db
from flask_login import UserMixin

class Admin(db.Model, UserMixin):
    admin_id = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    roles = db.Column(db.String(10), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)


    def get_id(self):
        return self.admin_id
    