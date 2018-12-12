#Python dependencies
import jwt
from time import time

#Flask dependencies
from flask import current_app

def get_email_confirmation_token(user_email, expires_in=900):
    """
    Method to generate secure web token for email confirmation.
    """
    return jwt.encode(
        {'email': user_email, 'exp': time() + expires_in},
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    ).decode('utf-8')

def verify_email_confirmation_token(token):
    """
    Method to verify email confirmation token
    """
    try:
        user_email = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )['email']
    except:
        return
    return user_email