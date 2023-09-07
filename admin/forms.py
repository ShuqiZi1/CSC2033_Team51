from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required, Length
from users.forms import character_check


class AdminEmailForm(FlaskForm):
    title = StringField(validators=[Required(),character_check])
    select = SelectField(choices=[("post_email", "Post Email"), ("charitable_acts_email", "Charitable Acts Email")])
    body = StringField(validators=[Required(), Length(min=0, max=65534, message='Character Count exceeded')])
