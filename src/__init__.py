from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_cors import CORS


load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # DB connection variables
    pg_host = os.getenv('PGHOST')
    pg_port = os.getenv('PGPORT')
    pg_db = os.getenv('PGDATABASE')
    pg_user = os.getenv('PGUSER')
    pg_pass = os.getenv('PGPASSWORD')

    # flask app configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
    app.config['JSON_SORT_KEYS'] = False
    login_manager.login_view = 'auth.login'

    # app initialization
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # register blueprints for route
    from src.controllers.AdminController import admin
    from src.controllers.AuthController import auth
    from src.views import home

    app.register_blueprint(admin, url_prefix='/')
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    # load admin
    from src.models.AdminModel import Admin

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(user_id)


    return app