#Flask dependencies
from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, current_user, login_required

#App dependencies
from app import db
from app.auth import bp
from app.models import User
from app.utility import get_next_page_or
from app.auth.email import send_password_reset_email 
from app.auth.forms import LoginForm, RegisterForm, \
    ResetPasswordRequestForm, ResetPasswordForm


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login View function
    """
    if current_user.is_authenticated:
        flash('You are already logged in, please logout to login using different id.')
        return redirect(get_next_page_or('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_user(identifier=form.identifier.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(get_next_page_or())
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
@login_required
def logout():
    """
    Logout view function.
    """
    logout_user()
    flash('Log out successful.')
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['Get', 'Post'])
def register():
    """
    User Registration view function.
    """
    if current_user.is_authenticated:
        flash('You are already registered, please logout for new registration.')
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful!')
        login_user(user, remember=True)
        return redirect(get_next_page_or())
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.get_user(form.email.data)
        if user:
            send_password_reset_email(user)
        else:
            flash('User not found')
            abort(404)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
