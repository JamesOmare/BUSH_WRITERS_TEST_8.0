from flask import Flask, session, abort
from os import path
from .config.config import Config
from .auth.views import auth
from .main.views import main
from.utils import db, migrate, login_manager, admin, moment
from .models.users import User
from .models.accounts import Account



# class AccountModelView(ModelView):
#     _status_choices = [(choice, label) for choice, label in [
#         (Account.STATUS_AVAILABLE, 'Available'),
#         (Account.STATUS_ON_PROGRESS, 'On_Progress'),
#         (Account.STATUS_VERIFICATION_STAGE, 'Verification_Stage'),
#         (Account.STATUS_SUCCESSFUL_STAGE, 'Successful_Stage'),
#         (Account.STATUS_DISPUTED_STAGE, 'Disputed_Stage'),
#     ]]
#     column_choices = {
#     'status': _status_choices,
#     }

#     column_list = ['account_id', 'account_type', 'account_name', 'description', 'brand', 'price', 'status', 'account_creation_date', 'time_posted']
    

# class UserModelView(ModelView):
#     column_list = ['id', 'username', 'email', 'phone_number', 'profile_photo', 'active', 'date_created']


DB_NAME = 'bushwriters.db'

def create_app(config = Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    moment.init_app(app)
    

    # Flask and Flask-SQLAlchemy initialization here
    # admin = Admin(app, name='Bushwriters Admin Portal', template_mode='bootstrap4') 

    
    admin.init_app(app)
    # admin.add_view(UserModelView(User, db.session))
    # admin.add_view(AccountModelView(Account, db.session))


    # Add the admin panel
    from src.admin import admin_ as admin_bp
    app.register_blueprint(admin_bp)
    


    #register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(main)

  

    create_database(app)

    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(id):
       return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('src/config/'+DB_NAME):
        db.create_all(app = app)
        print('created database')

# class SecureModelView(ModelView):
#     def is_accessible(self):
#         if "logged_in" in session:
#             return True
        
#         else:
#             abort(403)

# class NotificationsViews(BaseView):
#     @expose("/")
#     def index(self):
#         return self.render("admin/notify.html")

# class LogoutViews(BaseView):
#     @expose("/")
#     def index(self):
#         return self.render("admin/logout.html")