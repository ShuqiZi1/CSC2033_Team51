from flask import Blueprint, render_template, flash, url_for
from flask_login import current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from settings.forms import SettingsForm, PasswordForm
from models import User
from app import db

settings_blueprint = Blueprint('settings', __name__, template_folder='templates')

# Checks if the users new information is already in use through a database query, if so it will display a message
    # stating this


def check_available(type, content):
    user = False
    if type == "email":
        user = User.query.filter_by(email=content).first()
    if type == "username":
        user = User.query.filter_by(username=content).first()
    if type == "phone":
        user = User.query.filter_by(phone=content).first()

    if not user:
        return True

    flash(type + "'" + content + "' is already in use by another user.")
    return False

# If the form is filled with valid data and is available then the users new data will be added to the database
    # and they will be returned to the profile page and flashed a message saying their profile has been updated


@settings_blueprint.route('/settings', methods=['GET', 'POST'])
def settings():
    user_settings = SettingsForm()
    pass_form = PasswordForm()

    uid = current_user.user_id
    if user_settings.validate_on_submit():
        User.query.filter_by(user_id=uid).update({"firstname": user_settings.firstname.data})
        User.query.filter_by(user_id=uid).update({"lastname": user_settings.lastname.data})
        User.query.filter_by(user_id=uid).update({"social_media": user_settings.social_media.data})

        if check_available("username", user_settings.username.data):
            User.query.filter_by(user_id=uid).update({"username": user_settings.username.data})

        # if check_available("email", user_settings.email.data):
            # User.query.filter_by(user_id=uid).update({"email": user_settings.email.data})

        if check_available("phone", user_settings.phone.data):
            User.query.filter_by(user_id=uid).update({"phone": user_settings.phone.data})

        user_role = User.query.filter_by(user_id=uid).first().role
        if user_role != "Company" and user_role != "Charity":
            db.session.commit()
            return redirect(url_for("profiles.profiles", username=current_user.username))

        User.query.filter_by(user_id=uid).update({"website": user_settings.website.data})
        User.query.filter_by(user_id=uid).update({"bio": user_settings.bio.data})
        User.query.filter_by(user_id=uid).update({"topic": user_settings.topic.data})
        db.session.commit()
        flash("Updated your profile!", "profile_update")
        return redirect(url_for("profiles.profiles", username=current_user.username))

    if pass_form.validate_on_submit():  # update this to reflect currently logged in user when possible
        User.query.filter_by(user_id=uid).update({"password": generate_password_hash(pass_form.new_password.data)})
        db.session.commit()
        flash("Password updated!", "password_update")
        return redirect(url_for("profiles.profiles", username=current_user.username))

    return render_template('settings.html', user_settings=user_settings, pass_form=pass_form)

# loads settings template so user can enter new information
