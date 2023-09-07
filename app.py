# IMPORTS
import logging
import socket
from functools import wraps
from flask import Flask, render_template, session, request
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI,shutdown
import os


# LOGGING
class SecurityFilter(logging.Filter):
    def filter(self, record):
        return "SECURITY" in record.getMessage()


# create file handler to log security messages to file
path = os.path.dirname(os.path.realpath(__file__))
fh = logging.FileHandler(path + '\\globalPartnershipNCL.log', 'a')
fh.setLevel(logging.WARNING)
fh.addFilter(SecurityFilter())
formatter = logging.Formatter('%(asctime)s : %(message)s', '%m/%d/%Y %I:%M:%S %p')
fh.setFormatter(formatter)

# add handlers to root logger
logger = logging.getLogger('')
logger.propagate = False
if not logger.handlers:
    logger.addHandler(fh)


# CONFIG
app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://csc2033_team51:BarnBedsSitu@127.0.0.1:{server.local_bind_port}/csc2033_team51?charset=utf8mb4'

# initialise database
db = SQLAlchemy(app)


# FUNCTIONS
def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                logging.warning('SECURITY - Unauthorised access attempt [%s, %s, %s, %s]',
                                current_user.user_id,
                                current_user.email,
                                current_user.role,
                                request.remote_addr)
                # Redirect the user to an unauthorised notice!
                return render_template('errors/403.html')
            return f(*args, **kwargs)

        return wrapped

    return wrapper


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/topics')
def topics():  # put application's code here
    return render_template('charitable_acts.html')


# ERROR PAGE VIEWS
@app.errorhandler(400)
def bad_request(error):
    return render_template('errors/400.html'), 400


@app.errorhandler(403)
def page_forbidden(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(503)
def service_unavailable(error):
    return render_template('errors/503.html'), 503


if __name__ == '__main__':
    my_host = "127.0.0.1"
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind((my_host, 0))
    free_socket.listen(5)
    free_port = free_socket.getsockname()[1]
    free_socket.close()

    # avoid unauthorized user access certain pages
    login_manager = LoginManager()
    login_manager.login_view = 'users.login'
    login_manager.init_app(app)

    from models import User

    # search database and return the user matched ID
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # BLUEPRINTS
    # import blueprints
    from users.views import users_blueprint
    from post.views import post_blueprint

    from admin.views import admin_blueprint
    from contact.views import contact_blueprint
    from profiles.views import profile_blueprint
    from search.views import search_blueprint
    from quiz.views import quiz_blueprint
    from chatroom.views import chatroom_blueprint
    from settings.views import settings_blueprint

    # views blueprints with app
    app.register_blueprint(users_blueprint)
    app.register_blueprint(post_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(contact_blueprint)
    app.register_blueprint(profile_blueprint)
    app.register_blueprint(search_blueprint)
    app.register_blueprint(quiz_blueprint)
    app.register_blueprint(chatroom_blueprint)
    app.register_blueprint(settings_blueprint)

    app.run(host=my_host, port=free_port, debug=True)

    shutdown()