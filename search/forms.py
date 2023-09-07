from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class SearchForm(FlaskForm):
    search = StringField(validators=[DataRequired(), Length(min=0, max=65534, message='Character Count exceeded')])
    submit = SubmitField()
