from ..utils import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_admin.contrib.sqla import ModelView
from datetime import datetime


class Account_Credentials(UserMixin ,db.Model):
    """Account_Credentials model"""

    __tablename__ = 'account_credentials'
    id = db.Column(db.Integer, primary_key = True)
    seller_id = db.Column(db.Integer)
    buyer_id = db.Column(db.Integer)
    account_id = db.Column(db.Integer)
    account_email = db.Column(db.String(100))
    account_url = db.Column(db.String(250))
    account_passphrase = db.Column(db.String(250))
    time_posted = db.Column(db.DateTime(timezone = True), default = func.now())
    date_modified = db.Column(db.DateTime(timezone = True), nullable=False, server_default=func.now(), onupdate=func.now())
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id', ondelete = 'CASCADE'))
    notifications = db.relationship('Notification', backref = 'account_credentials', passive_deletes = True, lazy='dynamic')

    def __repr__(self):
        return '<Account_Credentials %r>' % self.id

