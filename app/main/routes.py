#Flask dependencies
from flask import render_template, current_app, redirect,\
                  flash, url_for, abort, g, request
from flask_login import current_user, login_required

#App dependencies
from app.models import Post, User #Database models
from app.main.forms import PostForm, SearchForm

#Main Blueprint
from app.main import bp

@bp.before_app_request
def before_request():
    """
    Method executed everytime a request is made.
    Currently working to update user last seen.
    """
    g.search_form = SearchForm()
    if current_user.is_authenticated:
        current_user.update_last_seen()

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    """
    View function for home page of application.
    """
    form = None
    if current_user.is_authenticated:
        form = PostForm()
        if form.validate_on_submit():
            Post.add_post(body_=form.post.data, author_=current_user)
            flash('Your post is now live!')
            return redirect(url_for('main.index'))
        posts = current_user.followed_posts().limit(current_app.config['POSTS_PER_PAGE'])
    else:
        posts = Post.get_random_posts(current_app.config['POSTS_PER_PAGE'])
    return render_template('index.html', title='Home', posts=posts, form=form)


@bp.route('/search')
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title='Search', posts=posts,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    """
    View function for current_user to follow user by username.
    """
    user = User.get_user(username)
    if user is None:
        flash('{} user not found.'.format(username))
        abort(404)
    elif user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for(get_next_page_or()))
    current_user.follow(user)
    flash('You are now following {}!'.format(username))
    return redirect(url_for('user.profile', username=username))

@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    """
    View function for current_user to unfollow user by username.
    """
    user = User.get_user(username)
    if user is None:
        flash('{} user not found.'.format(username))
        abort(404)
    elif user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for(get_next_page_or()))
    current_user.unfollow(user)
    flash('You are no longer following {}.'.format(user.username))
    return redirect(url_for('user.profile', username=username))
