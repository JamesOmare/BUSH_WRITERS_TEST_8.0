from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField, FileField, TextAreaField, SelectField, DateField, IntegerField, MultipleFileField, HiddenField, TelField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError, Email, DataRequired, Optional, NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed
from datetime import datetime, date
import phonenumbers


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

    # phone = StringField('Phone Number', validators=[DataRequired()])
    phone = TelField('Phone', validators=[DataRequired()])

    password =  PasswordField('Password',
                validators=[InputRequired(message='Password required'), 
                Length(min=5, message='Password must not be less than five characters')])

    confirm_password = PasswordField('Confirm password',
                validators=[InputRequired(message='Password Required'), 
                EqualTo('password', message='Passwords must match')])


    accept_tos = BooleanField('I accept the TOS', [DataRequired(message='You need to check the box to continue')])

    recaptcha = RecaptchaField()

    submit = SubmitField('Create')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')


class LoginForm(FlaskForm):
    """Login Form"""

    email = EmailField('Enter Email', 
                validators=[InputRequired(message='Enter a valid email address(i.e user121@email.com)'), Email()])


    password = PasswordField('Enter Password',
                validators=[InputRequired(message='Password required')])

    remember = BooleanField('Remmember Me')
    
    submit = SubmitField('Login')


class Seller_Profile_Form(FlaskForm):
    account_name = StringField('Account Name', 
                validators=[InputRequired(message='Account name required'),
                Length(min=3, max=50, message='Account name must be between 3 and 50 characters')])

    account_brand = StringField('Account Brand', 
                validators=[InputRequired(message='Account brand name required i.e medium'),
                Length(min=2, max=50, message='Account name must be between 2 and 50 characters')])

    account_type = SelectField('Account Category', choices=[('ARTICLE_ACCOUNT', 'Article Account'), ('ACADEMIC_WRITING_ACCOUNT', 'Academic Writing Account'), ('BLOGGING_ACCOUNT', 'Blogging Account')])

    account_description = TextAreaField('Account Description', [Optional(), Length(max=200)])

    account_creation_date = DateField('Date (DD-MM-YYYY)', default=date.today(),  validators=[DataRequired("Please enter the account creation Date."), InputRequired()])

    # image = MultipleFileField('Upload Account Images ie Screenshots here', [Optional()])
    # profile = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    

    account_value = IntegerField('Account Selling Price', validators=[InputRequired(message='Account price valuation required'), NumberRange(min=1000, max = 20000)], default = 1000)

    submit = SubmitField('Update')

    def validate_account_creation_date(form, account_creation_date):
        if account_creation_date.data > date.today():
            raise ValidationError("The creation date cannot be in the future!")

class Account_Images(FlaskForm):
    # images = MultipleFileField(label='Upload Account Images i.e screenshots', validators=[NumberRange(min=0, max = 10)])
    images = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

class Update_User_Account(FlaskForm):
    profile_image = FileField('Update Account Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    email =     EmailField('Email', 
                validators=[InputRequired(message='Enter a valid email address(i.e user121@email.com)'), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Update')