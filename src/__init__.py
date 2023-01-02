from flask import Flask, session, abort, render_template
from os import path
from .config.config import Config
from .auth.views import auth
from .main.views import main
from.utils import db, migrate, login_manager, admin, moment, mail
from .models.users import User


DB_NAME = 'bushwriters.db'

def create_app(config = Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    moment.init_app(app)
    mail.init_app(app)

    

    # Flask and Flask-SQLAlchemy initialization here

    admin.init_app(app)
   


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

    # Invalid URL error 
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('403.html'), 403

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    return app

def create_database(app):
    if not path.exists('src/config/'+DB_NAME):
        db.create_all(app = app)
        print('created database')
