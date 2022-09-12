from ..utils import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(UserMixin ,db.Model):
    """User model"""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    password = db.Column(db.String(150), nullable = False)
    date_created = db.Column(db.DateTime (timezone = True), default = func.now())

    def __repr__(self):
        return '<User %r>' % self.username