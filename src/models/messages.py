from ..utils import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_admin.contrib.sqla import ModelView
from datetime import datetime


class Message(UserMixin ,db.Model):
    """Mesage model"""

    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key = True)
    login_password = db.Column(db.String(120) )
    login_email = db.Column(db.String(120))
    user_id = db.Column(db.String(10))
    account_id = db.Column(db.String(10))
    time_posted = db.Column(db.DateTime(timezone = True), default = func.now())
    # func.now()
    # datetime.utcnow
    def __repr__(self):
        return '<Message %r>' % self.id

