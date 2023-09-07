from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import Required


class PostForm(FlaskForm):
    title = StringField(validators=[Required()])
    image = FileField()
    body = TextAreaField(validators=[Required()])
    submit = SubmitField()


class CharityPostForm(FlaskForm):
    title = StringField(validators=[Required()])
    location = StringField(validators=[Required()])
    image = FileField()
    body = TextAreaField(validators=[Required()])
    submit = SubmitField()
