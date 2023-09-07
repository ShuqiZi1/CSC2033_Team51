from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

from users.forms import character_check


class ContactForm(FlaskForm):
    name = StringField(validators=[DataRequired(),character_check])
    email = StringField(validators=[DataRequired(), Email()])
    message = StringField(validators=[DataRequired(), Length(min=0, max=65534, message='Character Count exceeded')])