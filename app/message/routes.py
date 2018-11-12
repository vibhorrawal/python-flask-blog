#Other dependencies
import json

#Flask and it's dependencies
from flask import render_template, flash, abort
from flask_login import current_user, login_required

#App dependencies
from app.models import User

#Module blueprint
from app.message import bp

@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """
    View function for private chat dashboard.
    """
    unread_users = current_user.get_unread_users()
    return render_template('message/msg_dashboard.html',
                            title='Message Dashboard',
                            unread_users=unread_users)


@bp.route('/chat/<With>', methods=['GET', 'POST'])
@login_required
def chat(With):
    """
    View function for chat page.
    """
    With = User.get_user(With)
    if current_user.id == With.id:
        flash('You cannot chat with yourself.')
        abort(404)
    chat = current_user.get_conversation_with(user=With)    
    return render_template('message/chat.html',
                            title=With.username,
                            chat=chat)


@bp.route('/chat_list', methods=['GET'])
@login_required
def chat_list():
    """
    View function for Ajax call from js to retrive list of 
    users, current_user is conversing with.
    """
    chat_dict = list()
    for u in current_user.get_all_users():
        chat_dict.append({'name': u.username, 'avatar': u.avatar(30)})    
    return json.dumps(chat_dict)

