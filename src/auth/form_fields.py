from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField, FileField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError, Email, DataRequired, FileAllowed


class RegistrationForm(FlaskForm):
    """Registration Form"""
    
    first_name = StringField('Firstname', 
                validators=[InputRequired(message='Firstname required'),
                Length(min=3, max=25, message='First name must be between 3 and 25 characters')])

    last_name = StringField('Lastname', 
                validators=[InputRequired(message='Username required'),
                Length(min=3, max=25, message='Last name must be between 3 and 25 characters')])

    email =     EmailField('Email', 
                validators=[InputRequired(message='Enter a valid email address(i.e user121@email.com)'), Email()])

    password =  PasswordField('Password',
                validators=[InputRequired(message='Password required'), 
                Length(min=5, message='Password must not be less than five characters')])

    confirm_password = PasswordField('Confirm password',
                validators=[InputRequired(message='Password Required'), 
                EqualTo('password', message='Passwords must match')])

    accept_tos = BooleanField('I accept the TOS', [DataRequired(message='You need to check the box to continue')])

    recaptcha = RecaptchaField()

    submit = SubmitField('Create')


class LoginForm(FlaskForm):
    """Login Form"""

    email = EmailField('Enter Email', 
                validators=[InputRequired(message='Enter a valid email address(i.e user121@email.com)'), Email()])


    password = PasswordField('Enter Password',
                validators=[InputRequired(message='Password required')])

    remember = BooleanField('Remmember Me')
    
    submit = SubmitField('Login')


# class Seller_Profile_Form(FlaskForm):
#     username = StringField('Username',
#                            validators=[DataRequired(), Length(min=2, max=20)])
#     email = StringField('Email',
#                         validators=[DataRequired(), Email()])
#     picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
#     submit = SubmitField('Update')

    
