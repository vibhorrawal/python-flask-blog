#Python dependencies
import sys
import colorama

#App dependencies
from app import create_app, db
from app.utility import setup_project
from app.models import User, Post, Message

colorama.init()

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Message':Message}

if __name__ == "__main__" and sys.argv[1]:
    if sys.argv[1] == 'run':
        app.run(threaded=True)
    elif sys.argv[1] == 'setup':
        setup_project()
    else:
        pass
else:
    app.run(threaded=True)
