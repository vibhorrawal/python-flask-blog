#Flask dependencies
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required

#App dependencies
from app import db
from app.auth import bp
from app.models import User
from app.utility import get_next_page_or
from app.auth.utility import verify_email_confirmation_token
from app.auth.email import send_password_reset_email, send_email_confirmation_mail 
from app.auth.forms import LoginForm, RegisterForm, \
    ResetPasswordRequestForm, ResetPasswordForm, CompleteRegisterationForm


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


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    User Registration view function.
    """
    if current_user.is_authenticated:
        flash('You are already registered, please logout for new registration.')
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        send_email_confirmation_mail(form.email.data)
        flash('Check your email for the instructions to reset your password')
        redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/complete_register/<token>', methods=['GET', 'POST'])
def complete_register(token):
    """
    Verify and complete User Registration view function.
    """
    if current_user.is_authenticated:
        flash('You are already registered, please logout for new registration.')
        return redirect(url_for('main.index'))
    user_email = verify_email_confirmation_token(token)
    if not user_email:
        flash('Your email cannot be verified.')
        redirect(url_for('mail.index'))
    form = CompleteRegisterationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=user_email)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful!')
        login_user(user, remember=True)
        return redirect(get_next_page_or())
    return render_template('auth/complete_register.html', title='Register', form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.get_user(form.email.data)
        if user:
            send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password')
        else:
            flash('Email is not registered.')
            return redirect(url_for('auth.register'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        flash('Password request cannot be verified.')
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
