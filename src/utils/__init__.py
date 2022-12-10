from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin, AdminIndexView, expose
from flask import redirect, url_for, request, g
from flask_moment import Moment
from flask_mail import Mail


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
moment = Moment()
mail = Mail()

admin = Admin(name='Bushwriters Admin Portal', template_mode='bootstrap4')