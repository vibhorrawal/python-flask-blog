#Other dependencies
import random
from time import time
from hashlib import md5
from datetime import datetime


#Flask and it's Dependencies
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

#Importing Database
from app import db, login

class User(UserMixin, db.Model):
    """
    Relational Table to store user data
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(240))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    
    def get_post(self):
        return self.posts

    def set_password(self, password):
        """
        Method to set user password.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Method to check correctness of password
        """
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        """
        Method to generate URL for User avatar
        """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    @staticmethod
    def get_user(identifier):
        user = User.query.filter_by(username=identifier).first()
        if user is None:
            user = User.query.filter_by(email=identifier).first()
        return user
    
    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    """
    Method to load User
    """
    return User.query.get(int(id))


class Post(db.Model):
    """
    Relational table to store posts by user
    """
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    @staticmethod
    def get_random_posts(num):
        """
        Getting number of random posts specefied
        """
        numPosts = len(Post.query.all())
        if num > numPosts:
            num = numPosts
        posts = list(Post.query.all())
        random.shuffle(posts)
        return posts[0:num]

    def __repr__(self):
        return '<Post {}>'.format(self.body)




