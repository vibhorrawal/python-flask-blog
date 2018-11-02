#Python dependencies
import os
import sys
import subprocess
import logging
from logging.handlers import RotatingFileHandler

#Flask and it's dependencies
from flask import request, url_for
from werkzeug.urls import url_parse

from app.models import 

def get_next_page_or(default='main.index'):
    """
    Method to get next page to a terminating event like user login
    """
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for(default)
    return next_page

def setup_logging(app):
    """
    Method to setup logging from server for the project.
    """
    if not os.path.exists('logs'):
        os.mkdir('logs')
    f_handle = RotatingFileHandler('logs/project.log', maxBytes=20480, backupCount=20)
    f_handle.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    f_handle.setLevel(logging.ERROR)
    app.logger.addHandler(f_handle)
    app.logger.setLevel(logging.ERROR)
    app.logger.info('Server startup')


def setup_project():
    """
    Method to setup project.
    """
    subprocess.call([sys.executable, "-m", "pip", "install", "-r" "requirements.txt"])
    
    env_data = '''FLASK_APP=project.py
SECRET_KEY=some-secret-key'''
    open('.env', 'w').write(env_data)
    #create dummy data