#Other dependencies
from datetime import datetime

#Flask dependencies
from flask import render_template, current_app, flash, redirect, url_for
from flask_login import current_user, login_required

from app import db
from app.models import Post, User

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

@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.get_user(username)
    if user is None or user == current_user:
        flash('You cannot follow {} this user!'.format(username))
        return redirect(url_for(get_next_page_or()))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user.profile', username=username))

@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.get_user(username)
    if user is None or user == current_user:
        flash('You cannot unfollow {} this user!'.format(username))
        return redirect(url_for(get_next_page_or()))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are no longer following {}.'.format(user.username))
    return redirect(url_for('user.profile', username=username))



