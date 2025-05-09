from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField, IntegerField
from wtforms.validators import DataRequired
import sqlalchemy


class GamerForm(FlaskForm):
    """id = StringField('Number', validators=[DataRequired()])"""
    name = StringField('Name', validators=[DataRequired()])
    email = IntegerField('Email')
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    submit = SubmitField('Войти')

class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')