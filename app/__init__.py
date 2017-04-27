# Basic setup and layout of the application was set up with the tutorial
# https://scotch.io/tutorials/build-a-crud-web-app-with-python-and-flask-part-one

# third-party imports
from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

#local imports
from config import app_config

# database variable initialization
db = SQLAlchemy()

login_manager = LoginManager()
mail = Mail()
    
def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('config.py')
    
    Bootstrap(app)
    db.init_app(app)
    mail.init_app(app)
    
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"
    
    migrate = Migrate(app, db)

    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)
    
    return app
    
