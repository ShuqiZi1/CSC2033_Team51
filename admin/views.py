# IMPORTS
import csv
from pathlib import Path

from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required

from admin.forms import AdminEmailForm
from app import db, requires_roles
from models import User, Post


admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


# view admin
@admin_blueprint.route('/admin', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def admin():
    form = AdminEmailForm()
    # view all users
    users = User.query.all()
    # view all posts
    posts = Post.query.all()
    # get email from csv
    #  newsletter file store path
    MESSAGE_DIR = Path(__file__).resolve().parent.parent.joinpath('newsletter.csv')
    csvFile = open(MESSAGE_DIR,"r")
    reader = csv.reader(csvFile)
    for item in reader:
        form.select.data = item[0]
        form.title.data = item[1]
        form.body.data = item[2]
    # view first 10 logs
    with open("globalPartnershipNCL.log", "r") as f:
        content = f.read().splitlines()[-10:]
        content.reverse()
    return render_template('admin.html',users=users, posts=posts, logs=content, form=form)


# disable & enable function
@admin_blueprint.route('/ban_user', methods=['POST'])
@login_required
@requires_roles('admin')
def ban_user():
    users = users = User.query.all()
    # if admin input can be got
    if request.form.get("ban_input"):
        # find user from admin input
        user = User.query.filter_by(user_id=request.form.get("ban_input")).first()
        # if user exist
        if user:
            if user.ban == 0:
                user.ban = 1
            else:
                user.ban = 0
            # admin user cannot be banned
            if user.role == "admin":
                user.ban = 0
    return admin()


# handle post function
@admin_blueprint.route('/handle_post', methods=['POST'])
@login_required
@requires_roles('admin')
def handle_post():
    if request.form.get("post_input"):
        post = Post.query.filter_by(post_id=request.form.get("post_input")).delete()
        db.session.commit()
    return admin()


# handle post function
@admin_blueprint.route('/send_email', methods=['POST'])
@login_required
@requires_roles('admin')
def send_email():
    form = AdminEmailForm()
    #  newsletter file store path
    MESSAGE_DIR = Path(__file__).resolve().parent.parent.joinpath('newsletter.csv')
    f = open(MESSAGE_DIR, "w", newline="")
    writer = csv.writer(f)
    message_csv = list()
    message_csv.append(form.select.data)
    message_csv.append(form.title.data)
    message_csv.append(form.body.data)
    writer.writerow(message_csv)
    f.close()
    return admin()


