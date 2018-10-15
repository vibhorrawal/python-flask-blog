from flask import render_template

from app.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    """
    View function for home page of application.
    """
    return render_template('index.html', title='Home')
