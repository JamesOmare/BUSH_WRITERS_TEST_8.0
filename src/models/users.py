from enum import unique
from ..utils import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(UserMixin ,db.Model):
    """User model"""

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    phone_number = db.Column(db.Integer, unique=True, nullable = False)
    password = db.Column(db.String(150), nullable = False)
    profile_photo = db.Column(db.String(80), nullable=True, default='default_profile.gif')
    date_created = db.Column(db.DateTime (timezone = True), default = func.now())
    account = db.relationship('Account', backref = 'user', passive_deletes = True)
    images = db.relationship('Image', backref = 'user', passive_deletes = True )

    def __repr__(self):
        return '<User %r>' % self.username