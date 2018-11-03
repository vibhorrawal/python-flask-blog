#Python dependencies
import os
import sys
import subprocess
import logging
from logging.handlers import RotatingFileHandler

def get_next_page_or(default='main.index'):
    """
    Method to get next page to a terminating event like user login
    """    
    #Flask and it's dependencies
    from flask import request, url_for
    from werkzeug.urls import url_parse
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
    try:
        #Creating Virtual Environment
        subprocess.check_call([sys.executable, "-m", "venv", "venv"], shell=True)
        #Activating Virtual Environment
        subprocess.check_call(["venv/Scripts/activate"])
        #Installing Dependencies
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r" "requirements.txt"], shell=True)
        
        #Creating .env file
        env_data = '''FLASK_APP=project.py
    SECRET_KEY=some-secret-key'''
        open('.env', 'w').write(env_data)
        
        #Initializing database
        subprocess.check_call("flask", "db", "migrate")
        subprocess.check_call("flask", "db", "upgrade")

        #App dependencies
        from app.models import User, Post, Message
        #Creating Test Data

    except subprocess.CalledProcessError as c:
        print(c)
        print(c.returncode)
    except Exception as e:
        print(e)


