#Python dependencies
import os
import logging
from logging.handlers import RotatingFileHandler

#Flask and it's dependencies
from flask import Flask, request, current_app
from flask_mail import Mail
from flask_login import LoginManager
from flask_moment import Moment
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

#Application Confirigation object
from config import Config

#Module Metadata
__version__ = '0.1d'

#Flask Extentions Objects
mail = Mail()
moment = Moment()
db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in for further access.'
login.session_protection = 'strong'


def create_app(appConfig=Config):
    app = Flask(__name__)
    app.config.from_object(appConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.error import bp as error_bp
    app.register_blueprint(error_bp)

    from app.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.message import bp as message_bp
    app.register_blueprint(message_bp, url_prefix='/message')

    if not os.path.exists('logs'):
        os.mkdir('logs')
    f_handle = RotatingFileHandler('logs/project.log', maxBytes=20480, backupCount=20)
    f_handle.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    f_handle.setLevel(logging.DEBUG)
    app.logger.addHandler(f_handle)
    app.logger.setLevel(logging.DEBUG)
    app.logger.info('Project Server startup')
    


    return app

from app import models
