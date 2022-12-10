from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField, FileField, TextAreaField, SelectField, DateField, IntegerField, MultipleFileField, HiddenField, TelField, HiddenField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError, Email, DataRequired, Optional, NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed
from datetime import datetime, date
from ..models.users import User
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

    images = MultipleFileField('Upload Account Images ie Screenshots here', [Optional()], render_kw={'multiple': True})
    # profile = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    

    account_value = IntegerField('Account Selling Price', validators=[InputRequired(message='Account price valuation required'), NumberRange(min=1000, max = 20000)], default = 1000)

    submit = SubmitField('Update')

    def validate_account_creation_date(form, account_creation_date):
        if account_creation_date.data > date.today():
            raise ValidationError("The creation date cannot be in the future!")

class Account_Images(FlaskForm):
    # images = MultipleFileField(label='Upload Account Images i.e screenshots', validators=[NumberRange(min=0, max = 10)])
    images = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])

class Update_User_Account(FlaskForm):
    first_name = StringField('Firstname', 
                validators=[InputRequired(message='Firstname required'),
                Length(min=3, max=25, message='First name must be between 3 and 25 characters')])

    last_name = StringField('Lastname', 
                validators=[InputRequired(message='Username required'),
                Length(min=3, max=25, message='Last name must be between 3 and 25 characters')])

    profile_image = FileField('Update Account Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])

    profile_details = StringField('Enter Profile Description', 
                validators=[ Length(max=100, message='The description must be less than 100 characters')])

    email = EmailField('Email', validators=[InputRequired(message='Enter a valid email address(i.e user121@email.com)'), Email()])

    phone = StringField('Phone Number', validators=[DataRequired()])

    submit = SubmitField('Update')

class RequestResetForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password =  PasswordField('Password',
                validators=[InputRequired(message='Password required'), 
                Length(min=5, message='Password must not be less than five characters')])

    confirm_password = PasswordField('Confirm password',
                validators=[InputRequired(message='Password Required'), 
                EqualTo('password', message='Passwords must match')])
    submit = SubmitField("Reset Password")

class AdminForm(FlaskForm):
    ac_login_email = EmailField('Account Login Email', validators=[InputRequired(message='Enter a valid email address(i.e user121@email.com)'), Email()])
    ac_login_pass = StringField('Account Login Password', 
                validators=[InputRequired(message='Input required'),
                Length(min=3, max=25, message='The password must be between 3 and 25 characters')])
    buyer_id = IntegerField('Buyer ID', validators=[InputRequired(message='Buyer ID required'), NumberRange(min=1)])
    account_id = IntegerField('Account ID', validators=[InputRequired(message='Account ID required'), NumberRange(min=1)])
    # type = SelectField('Account Category', choices=[('PURCHASE_INTENT', 'Purchase Intent'), ('ACCOUNT_PURCHASE_VERIFICATION', 'Account Purchase Verification'), ('SUCCESSFUL_PURCHASE', 'Successful Purchase'), ('FAILED_PURCHASE', 'Failed Purchase')])
    # intent_message = StringField('Enter Intent Message')
    # purchase_verification_message = StringField('Enter Purchase Verification Message')
    # successful_purchase = StringField('Enter Successful Account Purchase Message')
    # failed_purchase = StringField('Enter Failed Account Purchase Message')
    submit = SubmitField('Send')

class Complaint(FlaskForm):
    buyer_phone_number = IntegerField('Enter your phone number', validators=[InputRequired(message='Phone number required required')])
    seller_phone_number = IntegerField('Enter seller\'s phone number', validators=[InputRequired(message='Phone number required required')])
    reason = SelectField('Select Reason', choices=[('Account Advertised was misleading'), ('Account credentials are incorrect'), ('Account is suspended'), ("Other reasons(can expound further below)")])
    seller_id = HiddenField()
    extended_reason = TextAreaField('Further Description on the account problem(Optional)', [Optional(), Length(max=250)])
    submit = SubmitField("Reject")

class Seller_Account_Details(FlaskForm):
    account_name = StringField('Account Name', 
                validators=[InputRequired(message='Account Name required'),
                Length(min=3, max=25, message='Account Name must be between 3 and 25 characters')])
    account_type = StringField('Account Type i.e medium', 
                validators=[InputRequired(message='Account Type required'),
                Length(min=3, max=25, message='Account Type must be between 3 and 25 characters')])
    account_email = EmailField('Account Login Email', validators=[InputRequired(message='Enter a valid email address(i.e user121@email.com)'), Email()])
    account_url = StringField('Account Url', 
                validators=[InputRequired(message='Account Url required'),
                Length(min=3, max=150, message='Account Url must be between 3 and 25 characters')])
    account_passphrase = PasswordField('Enter Account Password',
                validators=[InputRequired(message='Password required')])
    buyer_id = HiddenField()
    account_id = HiddenField()
    submit = SubmitField("Submit")


class Payment_Method(FlaskForm):
    info = HiddenField()
    payment_method = SelectField('Choose Payment Method', choices=[('Paypal'), ('Mpesa')])
    submit = SubmitField("Proceed To Checkout")

class Confirmation_Form(FlaskForm):
    confirmation_msg = StringField('Enter the confirmation message', 
                validators=[InputRequired(message='Input required'),
                Length(min=3, max=100, message='The password must be between 3 and 100 characters')])
    submit = SubmitField("Send Message To Admin")

class Payment_Status(FlaskForm):
    account_id = HiddenField()
    buyer_id = HiddenField()
    seller_id = HiddenField()
    success = SubmitField("Confirm Message")
    failure = SubmitField("Reject Message")

class Search(FlaskForm):
    keyword = StringField(validators=[InputRequired(message='Search Keyword required'),
                Length(min=3, max=30, message='Search Keyword must be between 3 and 30 characters')])
    search = SubmitField()

class FilteredSearch(FlaskForm):
   article_ac =  BooleanField('Article Account')
   academic_ac = BooleanField('Academic Writing Account')
   blogging_ac = BooleanField('Blogging Account')
   date_from = DateField('From Date (DD-MM-YYYY)', default=date.today())
   date_to = DateField('To Date (DD-MM-YYYY)', default=date.today())
   price_range_a = IntegerField('Between Price: ', validators=[NumberRange(min=1000, max=50000)])
   price_range_b = IntegerField('To Price: ', validators=[NumberRange(min=1000, max=50000)])
   search = SubmitField()

   def validate_account_creation_date(form, date_from, date_to):
        if date_from.data or date_to.data > date.today():
            raise ValidationError("The searched date cannot be in the future!")

class Mpesa_Confirm(FlaskForm):
    phone_number = StringField(validators=[InputRequired(message='Phone Number required'),
                Length(min=10, max=15, message='Phone number must be at least 10 characters')])
    pay = SubmitField('Make Payment')