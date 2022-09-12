from crypt import methods
from flask import Blueprint, jsonify, redirect, render_template, request, flash, url_for, current_app
from .form_fields import RegistrationForm, LoginForm
from ..models.users import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from ..utils import db

auth = Blueprint('auth', __name__)

posts = [
    {
        'author': 'john faulk',
        'title': 'little birds',
        'content': 'Wait wait wait for me, please wait around i\'ll see you when i fall asleep',
        'date_posted': '12 March 2005'
    },

    {
        'author': 'peter faulk',
        'title': 'A quiet place',
        'content': 'Wait wait wait for me, please wait around i\'ll see you when i fall asleep',
        'date_posted': '18 Julu 1896'
    },

    {
        'author': 'authur faulk',
        'title': 'dawn on a ridge',
        'content': 'Wait wait wait for me, please wait around i\'ll see you when i fall asleep',
        'date_posted': '12 September 1995'
    },

    {
        'author': 'Melo Dy',
        'title': 'dawn on a ridge',
        'content': 'Wait wait wait for me, please wait around i\'ll see you when i fall asleep',
        'date_posted': '12 September 1995'
    },

    {
        'author': 'Melo Dy',
        'title': 'dawn on a ridge',
        'content': 'Wait wait wait for me, please wait around i\'ll see you when i fall asleep',
        'date_posted': '12 September 1995'
    },

    {
        'author': 'Melo Dy',
        'title': 'dawn on a ridge',
        'content': 'Wait wait wait for me, please wait around i\'ll see you when i fall asleep',
        'date_posted': '12 September 1995'
    },

    {
        'author': 'Melo Dy',
        'title': 'dawn on a ridge',
        'content': 'Wait wait wait for me, please wait around i\'ll see you when i fall asleep',
        'date_posted': '12 September 1995'
    },

    {
        'author': 'Melo Dy',
        'title': 'dawn on a ridge',
        'content': 'Wait wait wait for me, please wait around i\'ll see you when i fall asleep',
        'date_posted': '12 September 1995'
    },
]


@auth.route('/home')
def home():
    return render_template('home.html', posts=posts)


@auth.route('/', methods=['GET', 'POST'])
def register():
    reg_form = RegistrationForm()

    if request.method == 'POST' and reg_form.validate():
        email = reg_form.email.data
        password = reg_form.password.data
        firstname = reg_form.first_name.data
        lastname = reg_form.last_name.data

        # check if user exists
        email_exists = User.query.filter_by(email=email).first()

        if email_exists:
            flash('Email already exists, choose another one.', 'primary')

        else:
            new_user = User(
                username = firstname + " " + lastname,
                password = generate_password_hash(password, method='sha256'),
                email = email 
                )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash(
                'User created, you can log in with the registered credentials', 'success')

            return redirect(url_for('auth.login'))

    return render_template('register.html', form=reg_form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')
