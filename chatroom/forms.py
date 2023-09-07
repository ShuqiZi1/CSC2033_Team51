from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ChatForm(FlaskForm):
    message = StringField(validators=[DataRequired(), Length(min=0, max=65534, message='Character Count exceeded')])
    submit = SubmitField()