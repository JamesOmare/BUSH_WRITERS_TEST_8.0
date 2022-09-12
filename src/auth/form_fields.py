from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError, Email, DataRequired


class RegistrationForm(FlaskForm):
    """Registration Form"""
    
    first_name = StringField('firstname_', 
                validators=[InputRequired(message='Firstname required'),
                Length(min=3, max=25, message='First name must be between 3 and 25 characters')])

    last_name = StringField('lastname_', 
                validators=[InputRequired(message='Username required'),
                Length(min=3, max=25, message='Last name must be between 3 and 25 characters')])

    email =     EmailField('email_', 
                validators=[InputRequired(message='Enter a valid email address(i.e user121@email.com)'), Email()])

    password =  PasswordField('password_',
                validators=[InputRequired(message='Password required'), 
                Length(min=5, message='Password must not be less than five characters')])

    confirm_password = PasswordField('confirm_pass',
                validators=[InputRequired(message='Password Required'), 
                EqualTo('password', message='Passwords must match')])

    accept_tos = BooleanField('I accept the TOS', [DataRequired()])

    recaptcha = RecaptchaField()

    submit = SubmitField('Create')


class LoginForm(FlaskForm):
    """Login Form"""

    email = StringField('username_', 
                validators=[InputRequired(message='Username required')])

    password = PasswordField('password_',
                validators=[InputRequired(message='Password required')])
    remmember = BooleanField('Remmember Me')
    submit_btn = SubmitField('Login')