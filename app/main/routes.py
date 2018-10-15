#Other dependencies
from datetime import datetime

#Flask dependencies
from flask import render_template
from flask_login import current_user, login_required

from app import db

#Main Blueprint
from app.main import bp

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    """
    View function for home page of application.
    """
    return render_template('index.html', title='Home')
