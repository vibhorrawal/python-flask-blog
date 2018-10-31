
from app import create_app, db

from app.models import User, Post, Message

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Message':Message}

if __name__ == "__main__":
    app.run(threaded=True)
#app.run(threaded=True, ssl_context='adhoc')
