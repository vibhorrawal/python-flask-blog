
from flask import render_template, flash, url_for,\
                  request, current_app, abort
from flask_login import current_user

from app import db
from app.user import bp
from app.models import User, Post

@bp.route('/<username>')
def profile(username):
    user = User.get_user(username)
    if user is None:
        abort(404)
    page = request.args.get('page', 1, type=int)
    posts = user.get_post().order_by(
        Post.timestamp.desc()).paginate(page,
                                        current_app.config['POSTS_PER_PAGE'],
                                        False)
    next_url = url_for('user.profile', username=user.username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('user.profile', username=user.username,
                       page=posts.prev_num) if posts.has_prev else None
    return render_template('user/profile.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


