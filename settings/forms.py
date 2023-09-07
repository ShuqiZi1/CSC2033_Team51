from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
# from users.forms import character_check, validate_password
import re

# Checks if the characters are in the exclude chars list, if they are, a validation error is raised.


def character_check(form, field):
    excluded_chars = "£"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(
                f"Character {char} is not allowed.")

# Checks if the password contains at least a digit, an uppercase, a lowercase and a special character.


def validate_password(self, password):
    p = re.compile(r'(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*\W)')
    if not p.match(self.new_password.data):
        raise ValidationError("Password must contain at least 1 digit, an uppercase and a lowercase letter,"
                              "and a special character.")


class SettingsForm(FlaskForm):  # Don't use required or fill in user data as is in the form?
    username = StringField(validators=[DataRequired(), character_check])
    firstname = StringField(validators=[DataRequired(), character_check])
    lastname = StringField(validators=[DataRequired(), character_check])
    social_media = StringField(validators=[character_check])
    # email = StringField(validators=[DataRequired(), Email()])
    phone = StringField()
    submit = SubmitField()



class PasswordForm(FlaskForm):
    old_password = PasswordField(validators=[DataRequired()])
    new_password = PasswordField(validators=[DataRequired(), Length(min=6, max=12, message='Password must be between '
                                                                                           '6 and 12 characters in '
                                                                                           'length.'),
                                             validate_password])
    new_password_confirm = PasswordField(
        validators=[DataRequired(), EqualTo("new_password", message='Both password fields must be equal!')])
    submit = SubmitField()
