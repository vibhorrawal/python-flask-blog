#Flask dependencies
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

#App dependencies
from app.models import User


class LoginForm(FlaskForm):
    """
    class to manage Login Form.
    """
    identifier = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

    def validate_email(self, email):
        """
        Method to validate if email already do not exist.
        """
        if User.query.filter_by(email=email.data).first() is not None:
            raise ValidationError('Please use a different email address.')    

class CompleteRegisterationForm(FlaskForm):
    """
    class to manage User registration form.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Register')

    def validate_username(self, username):
        """
        Method to validate if username already do not exist.
        """
        if User.query.filter_by(username=username.data).first() is not None:
            raise ValidationError('Please use a different username.')
        elif ' ' in username.data:
            raise ValidationError('Blanck spaces not allowed in username')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
                    'Repeat Password',
                    validators=[DataRequired(), EqualTo('password')]
                )
    submit = SubmitField('Request Password Reset')
