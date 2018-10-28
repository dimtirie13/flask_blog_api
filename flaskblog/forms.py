from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    # RegistrationForm  username validation
    def validate_username(self, username):
        # database query to find user
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username already exists. Please choose another one')
    # RegistrationForm email validation
    def validate_email(self, email):
        # database query to find user
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email already exists. Please choose another one')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # allow users to stay logged in after browser closes using
    # a secure cookie
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')
