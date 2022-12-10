from flask import Blueprint, jsonify, redirect, render_template, request, flash, url_for, abort
from .form_fields import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from ..models.users import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from ..utils import db, mail
from flask_admin import BaseView, expose
from flask_mail import Message 

auth = Blueprint('auth', __name__)

class HelloView(BaseView): 
    @expose('/') 
    def index(self): 
        return self.render('some-template.html') 
    def is_accessible(self): 
        return current_user.is_authenticated and current_user.is_admin()

# def send_confirm_email(user):
#     token = user.get_reset_token()
#     msg = Message('Confirm Email Verification', 
#                     sender='bluescrubs254@gmail.com', 
#                     recipients=[user.email]
#                     )
#     msg.body = f"""  To finish up the registration process, please click the following link: 
#     {url_for('auth.confirm_email', token=token, _external=True)}  

#     If you did not make this request then simply ignore the email and no changes will be made.
#     """

#     mail.send(msg)


@auth.route('/signup', methods=['GET', 'POST'])
def register():
    reg_form = RegistrationForm()

    if request.method == 'POST' and reg_form.validate_on_submit():
            email = reg_form.email.data
            password = reg_form.password.data
            firstname = reg_form.first_name.data
            lastname = reg_form.last_name.data
            phone_number = reg_form.phone.data

            # check if email exists
            email_exists = User.query.filter_by(email=email).first()

            #check if phone number exists
            phone_number_exists = User.query.filter_by(phone_number=phone_number).first()

            if email_exists:
                flash('Email already exists, choose another one.', 'primary')
            
            elif phone_number_exists:
                flash('The phone number provided already exists. Please enter another one!', 'primary')

            else:
                new_user = User(
                    username = firstname + " " + lastname,
                    password = generate_password_hash(password, method='sha256'),
                    email = email,
                    phone_number = phone_number,
                    )
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('User created, you can log in with the registered credentials', 'success')

                return redirect(url_for('auth.login'))

    
    return render_template('register.html', form=reg_form)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Login successful', 'success')
        return redirect(url_for('main.user_profile', id = current_user.id))

    login_form = LoginForm()

    if request.method == 'POST' and login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        remember = login_form.remember.data


        # check if user exists
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember = remember)
                flash('Logged in!', 'success')
                return redirect(url_for('main.viewpage', id = current_user.id))
            else:
                flash('Username or Password is incorrect!', 'error')
        
        else:
            flash('Username or Password is incorrect!', 'error')

    return render_template('login.html', form = login_form, user = current_user)

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                    sender='rysesonofrome701@gmail.com', 
                    recipients=[user.email]
                    )
    msg.body = f"""  To reset your pasword, visit the following link: 
    {url_for('auth.reset_token', token=token, _external=True)}  

    If you did not make this request then simply ignore the email and no changes will be made.
    """

    mail.send(msg)

@auth.route('/reset_password', methods = ['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.user_profile', id = current_user.id))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('auth.login'))
    return render_template('reset_request.html', title = 'Reset Password', form = form)

@auth.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.user_profile', id = current_user.id))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user.password = hashed_password
        db.session.commit()
        flash('Your Password Has been updated! You can log in with the registered credentials', 'success')
        return redirect(url_for('auth.login'))
    return render_template('reset_token.html', title = 'Reset Password', form = form)


# @auth.route('/confirm_email/<token>', methods = ['GET', 'POST'])
# def confirm_email(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('main.user_profile', id = current_user.id))
#     user = User.verify_reset_token(token)
#     if user is None:
#         flash('That is an invalid or expired token', 'warning')
#         return redirect(url_for('auth.register'))

#     flash('Try logging in with the registered credentials', 'success') 
#     return redirect(url_for('auth.login'))
  