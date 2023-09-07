import base64
from datetime import datetime
from flask_login import UserMixin

from werkzeug.security import generate_password_hash
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes

from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    # Primary key
    user_id = db.Column(db.Integer, primary_key=True, unique=True)

    # User authentication information
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    pin_key = db.Column(db.String(100), nullable=False)

    # User activity information
    registered_on = db.Column(db.DateTime, nullable=True)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)

    # User information
    username = db.Column(db.String(100), nullable=False)
    user_img = db.Column(db.String(100), nullable=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    social_media = db.Column(db.String(100), nullable=False)

    # User setting
    ban = db.Column(db.BOOLEAN, nullable=False, default=False)
    receive_email = db.Column(db.BOOLEAN, nullable=False, default=True)

    # crypto key for user's post, chat and other information
    user_key = db.Column(db.BLOB)

    # Define the relationship to charities, company, chatroom and post
    chatroom = db.relationship('Chatroom')
    posts = db.relationship('Post')
    like = db.relationship('Like')

    def get_id(self):
        return (self.user_id)

    def get_username(self, given_id):
        user = User.query.filter_by(user_id=given_id).first()

        # if they don't have a username:
        if user.username is None:
            return "Anonymous User"

        return user.username

    def is_following(self, user):
        not_followed = not Follow.query.filter_by(follower_id=self.user_id, following_id=user.user_id).first()
        return not not_followed

    def has_liked(self, post_id):
        not_liked = not Like.query.filter_by(post_id=post_id, user_id=self.user_id).first()
        return not not_liked

    def __init__(self, email, password, pin_key, username, firstname, lastname, role):
        self.email = email
        # hash password
        self.password = generate_password_hash(password)
        self.pin_key = pin_key
        self.username = username
        self.user_img = ""
        self.firstname = firstname
        self.lastname = lastname
        self.phone = ""
        self.role = role
        self.social_media = ""
        self.ban = 0
        self.receive_email = 1
        # generate draw_key from user passwords
        self.user_key = base64.urlsafe_b64encode(scrypt(password, str(get_random_bytes(32)), 32, N=2 ** 14, r=8, p=1))
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = None


class Post(db.Model):
    __tablename__ = 'posts'

    # Primary key
    post_id = db.Column(db.Integer, primary_key=True, unique=True)

    title = db.Column(db.Text, nullable=False, default=False)
    location = db.Column(db.Text, nullable=True, default=False)
    body = db.Column(db.Text, nullable=False, default=False)
    post_time = db.Column(db.DateTime, nullable=False)
    post_img = db.Column(db.String(100), nullable=True)

    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), nullable=False)

    like = db.relationship('Like')
    # returns username of person who posted

    def get_username(self, given_id):
        user = User.query.filter_by(user_id=given_id).first()

        # if they don't have a username:
        if user.username is None:
            return "Anonymous User"

        return user.username

    def toggle_like(self, user_id):

        # if this user hasn't already liked this post
        if not Like.query.filter_by(user_id=user_id, post_id=self.post_id).first():
            # add the like to the database
            new_like = Like(user_id, self.post_id)
            db.session.add(new_like)
            db.session.commit()
        else:
            Like.query.filter_by(user_id=user_id, post_id=self.post_id).delete()
            db.session.commit()

    def get_likes(self):
        if not Like.query.filter_by(post_id=self.post_id).all():
            return 0
        else:
            likes = Like.query.filter_by(post_id=self.post_id).count()
            return likes

    def get_user(self):
        return User.query.filter_by(user_id=self.user_id).first() or {}

    def update_post(self, title, body):
        self.title = title
        self.body = body
        db.session.commit()

    def __init__(self, post_id, user_id, title, body, post_img):
        self.post_id = post_id
        self.user_id = user_id
        self.post_time = datetime.now()
        self.title = title
        self.body = body
        self.post_img = post_img


class Chatroom(db.Model):
    __tablename__ = 'chatroom'

    chat_id = db.Column(db.Integer, primary_key=True, unique=True)

    content = db.Column(db.Text, nullable=False)
    post_time = db.Column(db.DateTime, nullable=False)

    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), nullable=False)

    # returns username of person who posted chat
    def get_username(self, given_id):
        user = User.query.filter_by(user_id=given_id).first()

        # if they don't have a username:
        if user.username is None:
            return "Anonymous User"

        return user.username

    def __init__(self, chat_id, content, user_id):
        self.chat_id = chat_id
        self.content = content
        self.post_time = datetime.now()
        self.user_id = user_id


class Follow(db.Model):
    __tablename__ = 'follow'

    follower_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True, nullable=False)
    following_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True, nullable=False)

    def __init__(self, follower_id, following_id):
        self.follower_id = follower_id
        self.following_id = following_id


class Like(db.Model):
    __tablename__ = 'like'

    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(Post.post_id), primary_key=True, nullable=False)

    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id


def init_db():
    db.drop_all()
    db.create_all()
    admin = User(email='admin@email.com',
                 password='Admin1!',
                 pin_key='BFB5S34STBLZCOB22K6PPYDCMZMH46OJ',
                 username='Admin',
                 firstname='Alice',
                 lastname='Jones',
                 role='admin')
    db.session.add(admin)
    user = User(email='user1@test.com',
                password='test123',
                pin_key='BFB5S34STBLZCOB22K6PPYDCMZMH46OJ',
                username='User',
                firstname='Alice',
                lastname='Jones',
                role='user')
    db.session.add(user)
    post = Post(post_id='1',
                user_id='1',
                title='test post title',
                body='This is test content for post.',
                post_img='test img')
    db.session.add(post)
    db.session.commit()