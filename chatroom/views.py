from flask import Blueprint, render_template, request
from flask_login import current_user, login_required, LoginManager
from sqlalchemy import desc
from models import Chatroom, User
from chatroom.forms import ChatForm
from app import db

# CONFIG
chatroom_blueprint = Blueprint('chatroom', __name__, template_folder='templates')

# If request method is POST or form valid then add the users chat to database with allocated data.


# VIEWS
@chatroom_blueprint.route('/chatroom', methods=('GET', 'POST'))
# @login_required
def chatroom():

    form = ChatForm()

    chats = Chatroom.query.order_by('post_time').all()

    if form.validate_on_submit():

        # get an unused number to give the 'chat' a unique ID
        next_chat_id = Chatroom.query.order_by(desc('chat_id')).first().chat_id + 1

        new_chat = Chatroom(chat_id=next_chat_id,
                            content=form.message.data,
                            user_id=current_user.user_id)
        # add the chat
        db.session.add(new_chat)
        db.session.commit()
        # reload the page once chatted so that you can see your message.
        chats = Chatroom.query.order_by('post_time').all()
        return render_template('chatroom.html', form=form, chats=chats)

    # load the page the first time
    return render_template('chatroom.html', form=form, chats=chats)
