from enum import unique
from ..utils import db, login_manager
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_admin.contrib.sqla import ModelView
from itsdangerous import URLSafeTimedSerializer as Serializer
from decouple import config


class User(UserMixin ,db.Model):
    """User model"""

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    phone_number = db.Column(db.Integer, unique=True, nullable = False)
    password = db.Column(db.String(350), nullable = False)
    profile_photo = db.Column(db.String(80), nullable=True, default='default_profile.gif')
    date_created = db.Column(db.DateTime (timezone = True), default = func.now())
    date_modified = db.Column(db.DateTime(timezone = True), nullable=False, server_default=func.now(), onupdate=func.now())
    active = db.Column(db.Boolean, default=True)
    profile_description = db.Column(db.String(100), default = 'Hello There 👋')
    admin = db.Column(db.Boolean(), default=False) 
    account = db.relationship('Account', backref = 'user', passive_deletes = True)
    images = db.relationship('Image', backref = 'user', passive_deletes = True )

    def get_reset_token(self):
        s = Serializer(config('SECRET_KEY'))
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec = 1800):
        s = Serializer(config('SECRET_KEY'))
        try:
            user_id = s.loads(token, expires_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return 'User %r' % self.username
