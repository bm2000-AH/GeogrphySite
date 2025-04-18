from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class GamerForm(FlaskForm):
    id = StringField('Number', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    strana = IntegerField('Name of country')
    work_time = StringField('time', validators=[DataRequired()])
    date = BooleanField("date")