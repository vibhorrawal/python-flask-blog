#Flask dependencies
from flask import render_template

#App dependencies
from app import db
from app.error import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    """
    View function for 404 Page not found error.
    """
    return render_template('error/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    """
    View function for 500 Internal Server Error error.
    """
    db.session.rollback()
    return render_template('error/500.html'), 500
