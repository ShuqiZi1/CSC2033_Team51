import re
from wtforms import StringField, SubmitField, PasswordField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import Required, Email, Length, EqualTo, ValidationError
import re


# input filtering for first name and last name
def character_check(form, field):
    excluded_chars = "*?!'^+%&/()=}][{$#@<>"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(
                f"Character {char} is not allowed.")


class RegisterForm(FlaskForm):
    username = StringField(validators=[Required(), character_check])
    firstname = StringField(validators=[Required(), character_check])
    lastname = StringField(validators=[Required(), character_check])
    email = StringField(validators=[Required(), Email()])
    role = SelectField(choices=[("Personal", "Personal"), ("Company", "Company"), ("Charity", "Charity")],
                       validators=[Required()])
    password = PasswordField(validators=[Required(), Length(min=6, max=12, message='Password must be between 6 and 12 '
                                                                                   'characters in length.')])
    confirm_password = PasswordField(validators=[Required(), EqualTo('password', message='Both password fields must '
                                                                                         'be equal!')])
    pin_key = StringField(validators=[Required(), Length(min=32, max=32, message='PIN Key must be exactly 32 '
                                                                                 'characters in length.')])
    submit = SubmitField()


# pattern matching for password
def validate_password(self, password):
    p = re.compile(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W)')
    if not p.match(self.password.data):
        raise ValidationError("Password must contain at least 1 digit, 1 lowercase, 1 uppercase and 1 special "
                              "character.")


class LoginForm(FlaskForm):
    username = StringField(validators=[Required(), Email()])
    password = PasswordField(validators=[Required()])
    # add PIN
    pin_key = StringField(validators=[Required(), Length(min=6, max=6, message='PIN must be 6 digits in length.')])

    submit = SubmitField()


# pattern matching for pinkey
def validate_pinkey(self, pin_key):
    p = re.compile(r'\d{6}')
    if not p.match(self.pin_key.data):
        raise ValidationError("PIN must be digits.")

# check the excluded characters
# form as a parameter in character check
# discuss specifications for password, including length and validations.
