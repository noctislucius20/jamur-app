from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

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

    # app initialization
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints for route
    from src.controllers.AdminController import admin


    app.register_blueprint(admin, url_prefix='/api')

    return app