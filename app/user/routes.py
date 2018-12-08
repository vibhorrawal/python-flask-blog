#Other dependencies
import json

#Flask and it's dependencies
from flask import render_template, url_for,\
                  request, current_app, abort, \
                  flash, redirect
from flask_login import current_user, login_required

#App dependencies
from app.user import bp
from app.user.forms import EditProfileForm

from app.models import User, Post

@bp.route('/<username>')
def profile(username):
    """
    View function for user profile page.
    """
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
    return render_template('user/profile.html',
                           user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)

@bp.route('/_ffCount/<username>', methods=['GET'])
def _ffCount(username):
    """
    View function for Ajax call from js.
    """
    user = User.get_user(username)
    if user is None:
        abort(404)
    return json.dumps({
        'Following': user.get_followed_count(),
        'Followers': user.get_followers_count()
    })

@bp.route('/followers/<username>')
def followers(username):
    """
    View function to list all followers of a user.
    """
    u = User.get_user(username)
    if u is None:
        abort(404)
    users = u.get_followers()
    return render_template('user/followers.html', user=u, users=users)

@bp.route('/followed/<username>')
def followed(username):
    """
    View function to list all followed people of a user.
    """
    u = User.get_user(username)
    if u is None:
        abort(404)
    users = u.get_followed()
    return render_template('user/followed.html', user=u, users=users)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.set_about(form.username.data, form.about_me.data)
        flash('Your changes have been saved.')
        return redirect(url_for('user.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('user/edit_profile.html', title='Edit Profile',
                           form=form)

@bp.route('/<username>/popup')
def user_popup(username):
    user = User.get_user(username)
    if user is None:
        flash('User not found.')
        abort(404)
    return render_template('user/popup.html', user=user)