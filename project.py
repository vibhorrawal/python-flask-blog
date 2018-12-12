#Python dependencies
import sys
import colorama

#App dependencies
from app import create_app, db
from app.models import User, Post, Message

colorama.init()

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Message':Message}
