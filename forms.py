from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, RadioField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=4, max=32)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=4, max=32)])
    emailid = EmailField('Email ID', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6, max=20), EqualTo('password')])
    submit = SubmitField('Register')

class ResetForm(FlaskForm):
    username = StringField('Username')
    emailid = EmailField('Email ID', validators=[DataRequired()])
    password = PasswordField('Password')
    submit = SubmitField('Reset')

class SetPreferencesForm(FlaskForm):
    preferred_category_1 = BooleanField('Bollywood')
    preferred_category_2 = BooleanField('Hollywood')
    preferred_category_3 = BooleanField('Video Songs')
    adultpreference = BooleanField('Adult Content')
    submit = SubmitField('Set Preferences')