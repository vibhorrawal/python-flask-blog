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
