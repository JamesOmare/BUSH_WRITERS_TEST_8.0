from sre_parse import FLAGS
from flask import Flask
from os import path
from .config.config import Config
from .auth.views import auth
from .main.views import main
from.utils import db, migrate, login_manager
from .models.users import User
from flask_migrate import Migrate

DB_NAME = 'bushwriters.db'

def create_app(config = Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)

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