# IMPORTS
import logging
import pyotp

from datetime import datetime
from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, requires_roles
from models import User
from users.forms import RegisterForm, LoginForm

users_blueprint = Blueprint('users', __name__, template_folder='templates')


# view user login
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    session['logins'] = 0
    # if session attribute logins does not exist create attribute logins
    if not session.get('logins'):
        session['logins'] = 0
    # if login attempts is 3 or more create an error message
    elif session.get('logins') >= 3:
        flash('Number of incorrect logins exceeded')

    # create login form object
    form = LoginForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():

        # increase login attempts by 1
        session['logins'] += 1

        user = User.query.filter_by(email=form.username.data).first()
        # login failed
        if not user or not check_password_hash(user.password, form.password.data):

            # if no match create appropriate error message based on login attempts
            if session['logins'] == 3:
                flash('Number of incorrect logins exceeded')
            elif session['logins'] == 2:
                flash('Please check your login details and try again. 1 login attempt remaining')
            else:
                flash('Please check your login details and try again. 2 login attempts remaining')

            # log for invalid login attempts
            logging.warning('SECURITY - Unauthorised login attempt [Anonymous user, %s, %s]', form.username.data,
                            request.remote_addr)

            return render_template('sign_in.html', form=form)

        # verify the PIN submitted by the user
        if pyotp.TOTP(user.pin_key).verify(form.pin_key.data):

            # if user is verified reset login attempts to 0
            session['logins'] = 0

            # register the user as logged in
            login_user(user)

            # last_logged_in is updated to current_logged_in
            user.last_logged_in = user.current_logged_in
            # current_logged_in is updated to current time
            user.current_logged_in = datetime.now()
            # update to database
            db.session.add(user)
            db.session.commit()

            # log for User log in
            logging.warning('SECURITY - Log in [%s, %s, %s]', current_user.user_id, current_user.email,
                            request.remote_addr)

            # direct to role appropriate page
            if current_user.role == 'admin':
                return redirect(url_for('admin.admin'))
            else:
                return redirect(url_for('profiles.profiles', username=user.username))

            # login successful return profile page
            # return profile()

        # 2FA token error, login unsuccessful
        else:
            flash("You have supplied an invalid 2FA token!", "danger")

    return render_template('sign_in.html', form=form)


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # create signup form object
    form = RegisterForm()


    # if request method is POST or form is valid
    if form.validate_on_submit():
        a = 4
        useremail = User.query.filter_by(email=form.email.data).first()
        username = User.query.filter_by(username=form.username.data).first()
        # if this returns a user, then the email already exists in database

        # if email already exists redirect user back to signup page with error message so user can try again
        if useremail or username:
            flash('Username/Email address already exists')
            return render_template('sign_up.html', form=form)

        # create a new user with the form data
        new_user = User(email=form.email.data,
                        username=form.username.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        password=form.password.data,
                        pin_key=form.pin_key.data,
                        role=form.role.data)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # log for User register
        logging.warning('SECURITY - User registration [%s, %s]', form.email.data, request.remote_addr)

        # return user to login page redirect
        return redirect(url_for('index'))

    # if request method is GET or form not valid re-render signup page
    return render_template('sign_up.html', form=form, user_role=get_roles(), otp=pyotp.random_base32())


# get user roles
def get_roles():
    user_role = ["Personal", "Company", "Charity"]
    return user_role