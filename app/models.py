#Other dependencies
import random
from hashlib import md5
from datetime import datetime


#Flask and it's Dependencies
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

#Importing Database
from app import db, login


follow_tab = db.Table('follow_tab', 
        db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
    )

class User(UserMixin, db.Model):
    """
    Relational Table to store user data
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.Text)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship(
        'User',
        secondary=follow_tab,
        primaryjoin=(follow_tab.c.follower_id == id),
        secondaryjoin=(follow_tab.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )
    msg_sent = db.relationship('Message',
                               foreign_keys='Message.sender_id',
                               backref='sender', lazy='dynamic')
    msg_received = db.relationship('Message',
                                   foreign_keys='Message.recipient_id',
                                   backref='recipient', lazy='dynamic')


    def get_post(self):
        """
        Method to get post by user.
        """
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
    
    def follow(self, user):
        """
        If user do not follow supplied user then starts following.
        """
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        """
        If user follows supplied user then, unfollow.
        """
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        """
        Is our user following supplied user.
        """
        return self.followed.filter(
            follow_tab.c.followed_id == user.id).count() > 0

    def get_followers_count(self):
        """
        Method provide followers count.
        """
        return.followers.count()

    def get_followed_count(self):
        """
        Method provide count of users following self.
        """
        return self.followed.count()

    def followed_posts(self):
        """
        Posts by all users, our user is following,
        in chronologically reversed order(newest first).
        Left outer join on,
        Post <--> follow_tab
        """
        return Post.query.join(follow_tab,
                    (follow_tab.c.followed_id == Post.user_id)).filter(
                        follow_tab.c.follower_id == self.id).order_by(Post.timestamp.desc())
   
    def get_conversation_with(self, user, change_read=False):
        """
        Returns Conversation with supplied user,
        changes read flag depending on supplied flag.
        """
        #Self --> User messages
        mySide = list(self.msg_sent.filter_by(recipient_id=user.id).all())
        #self <-- User messages
        userSide = list(self.msg_received.filter_by(sender_id=user.id).all())
        #Joinning two sides
        conversation=sorted(mySide+userSide,
                            key = lambda x: x.timestamp,
                            reverse=True)
        #If read flag is True then read flag on messges is changes
        if change_read:
            for message in conversation:
                if message.recipient_id == self.id:
                    message.is_read = True
            db.session.commit()
        return conversation
    
    def get_unread_users(self):
        """
        Returns all users from whom unread messages.
        """
        msg = Message.query.filter_by(recipient_id=self.id, is_read=False).all()
        unread_users = list()
        for m in msg:
            unread_users.append(User.query.get(int(m.sender_id)))
        return list(set(unread_users))

    def send_msg(self, user, msg):
        m = Message(sender=self,
                    recipient=user,
                    body=msg)
        db.session.add(m)
        db.session.commit()

    @staticmethod
    def get_user(identifier):
        """
        Method to get user using email or username.
        """
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
        Getting number of random posts specefied.
        """
        numPosts = len(Post.query.all())
        if num > numPosts:
            num = numPosts
        posts = list(Post.query.all())
        random.shuffle(posts)
        return posts[0:num]

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Message(db.Model):
    """
    Model to store all private messages.
    """
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)


    def __repr__(self):
        return '<Message: {}>'.format(self.body)


