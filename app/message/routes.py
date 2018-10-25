#Flask and it's dependencies
from flask import render_template
from flask_login import current_user, login_required

#Module blueprint
from app.message import bp

@bp.route('/message', methods=['GET', 'POST'])
@login_required
def message():
    """
    View function for private chat dashboard.
    """
    users = current_user.get_unread_users()
    return render_template('message/msg_dashboard.html', title='Message', users=users)