#Flask and it's dependencies
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from config import Config

mail = Mail()
moment = Moment()
db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in for further access.'


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

    return app

from app import models

