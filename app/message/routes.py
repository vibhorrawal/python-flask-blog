from flask import render_template

from app.message import bp

@bp.route('/message', methods=['GET', 'POST'])
@login_required
def message():
    return render_template('message/msg_dashboard.html', title='Message')