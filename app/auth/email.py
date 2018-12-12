#Flask dependencies
from flask import render_template, current_app

#App dependencies
from app.email import send_email
from app.auth.utility import get_email_confirmation_token


def send_password_reset_email(user):
    """
    Methos to send password reset email
    """
    token = user.get_reset_password_token()
    send_email(
        '[Umhera] Reset Your Password',
        sender=current_app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template(
            'email/reset_password.txt',
            user=user,
            token=token
        ),
        html_body=render_template('email/reset_password.html',
        user=user,
        token=token)
    )

def send_email_confirmation_mail(user_email):
    """
    Method to generate and send email confirmation mail.
    """
    token = get_email_confirmation_token(user_email)
    send_email(
        '[Umhera] Confirm your email.',
        sender=current_app.config['ADMINS'][0],
        recipients=[user_email],
        text_body=render_template(
            'email/confirm_email.txt',
            email=user_email,
            token=token
        ),
        html_body=render_template('email/confirm_email.html',
        email=user_email,
        token=token)
    )