#Python dependencies
import os
import logging
from logging.handlers import RotatingFileHandler

#Flask andit's dependencies
from flask import request, url_for
from werkzeug.urls import url_parse


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
    file_handler = RotatingFileHandler('logs/project.log',
                                    maxBytes=20480,
                                    backupCount=20)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)    
    app.logger.info('Server startup')
