#Python dependencies
import os
import sys
import time
import subprocess
from subprocess import check_output as run_out
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
        #Creating .env file
        env_data = '''FLASK_APP=project.py
SECRET_KEY=some-secret-key'''
        env_file = open('.env', 'w')
        env_file.write(env_data)
        env_data.close()
        
        #Initializing database
        run_out(["flask", "db", "migrate"], shell=True)
        run_out(["flask", "db", "migrate"], shell=True)
        run_out(["flask", "db", "upgrade"], shell=True)

        #App dependencies
        from app import db
        from app.models import User, Post, Message
        
        #Creating Test Data
        for i in range(1, 6):
            u = User(username='U{}'.format(i), email='u{}@example.com'.format(i), about_me='User U{}'.format(i))
            u.set_password('password')
            db.session.add(u)

        for i in range(1, 6):
            u = User.get_user('U{}'.format(i))
            for j in range(1, 6):
                p = Post(author=u, body='U{} post {}.'.format(i, j))
                db.session.add(p)
                time.sleep(5)
                if i != j:
                    u.follow(User.get_user('U{}'.format(j)))
                    m = Message(sender=u,
                                recipient=User.get_user('U{}'.format(j)),
                                body='U{} {} message to U{}'.format(i, j, j))
                    db.session.add(m)
                            
        db.session.commit()
    except Exception as e:
        print(e)


