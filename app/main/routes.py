#Other dependencies
from datetime import datetime

#Flask dependencies
from flask import render_template, current_app
from flask_login import current_user, login_required

from app import db
from app.models import Post

#Main Blueprint
from app.main import bp

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/')
@bp.route('/index')
def index():
    """
    View function for home page of application.
    """
    if current_user.is_authenticated:
        posts = current_user.get_post()
    else:
        posts = Post.get_random_posts(current_app.config['POSTS_PER_PAGE'])
    return render_template('index.html', title='Home', posts=posts)
