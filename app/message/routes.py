import json

#Flask and it's dependencies
from flask import render_template, flash, abort, request
from flask_login import current_user, login_required

#App dependencies
from app.utility import format_datetime
from app.models import User

#Module blueprint
from app.message import bp

@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """
    View function for private chat dashboard.
    """
    unread_users = current_user.get_all_users()
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
        flash('You cannot chat with yourself')
        abort(404)
    if request.method == "POST":
        if request.form['push_message_box']:
            push_message = request.form['push_message_box']
            current_user.send_msg(With, push_message.strip())
    if current_user.id == With.id:
        flash('You cannot chat with yourself.')
        abort(404)
    chat = current_user.get_conversation_with(user=With, change_read=True)    
    return render_template('message/chat.html',
                            title=With.username, chat=chat,
                            With=With)

@bp.route('/new_msg/<With>', methods=['GET'])
@login_required
def new_msg(With):
    '''
    View function for Ajax call from js to retrive in the conversation.
    '''
    new_messages = list()
    With = User.get_user(With)
    for msg in current_user.get_new_conversation(With):
        new_messages.append(
            {
                'body': msg.body,
                'timestamp': format_datetime(msg.timestamp, format='from-now')
            }
        )    
    return json.dumps(dict(
        {
            'messages': new_messages,
            'username': With.username,
            'avatar': With.avatar(30)
        }
    ))

"""
@bp.route('/chat_list', methods=['GET'])
@login_required
def chat_list():
    '''
    View function for Ajax call from js to retrive list of 
    users, current_user is conversing with.
    '''
    chat_dict = list()
    for u in current_user.get_all_users():
        chat_dict.append({'name': u.username, 'avatar': u.avatar(30)})    
    return json.dumps(chat_dict)
"""
