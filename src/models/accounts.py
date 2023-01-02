from ..utils import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from enum import Enum

class AccountType(Enum):
    ARTICLE_ACCOUNT = 'article_account'
    ACADEMIC_WRITING_ACCOUNT = 'academic_writing_account'
    BLOGGING_ACCOUNT = 'blogging_account'


class Account(db.Model):
    """Accounts model"""

    STATUS_AVAILABLE = 0
    STATUS_ON_PROGRESS = 1
    STATUS_VERIFICATION_STAGE = 2
    STATUS_SUCCESSFUL_STAGE = 3
    STATUS_DISPUTED_STAGE = 4
    

    __tablename__ = 'account'
    account_id = db.Column(db.Integer, primary_key = True)
    account_type = db.Column(db.Enum(AccountType), default = AccountType.ACADEMIC_WRITING_ACCOUNT)
    account_name = db.Column(db.String(80), nullable = False)
    description = db.Column(db.String(120), nullable = False)
    brand = db.Column(db.String(60), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    status = db.Column(db.SmallInteger, default=STATUS_AVAILABLE)
    account_creation_date = db.Column(db.Date, nullable = False)
    #needs to be time separately
    time_posted = db.Column(db.DateTime (timezone = True), default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'CASCADE'))
    images = db.relationship('Image', backref = 'account', passive_deletes = True, lazy='dynamic' )
    notifications = db.relationship('Notification', backref = 'account', passive_deletes = True, lazy='dynamic')
    complaints = db.relationship('Complaints', backref = 'account', passive_deletes = True, lazy='dynamic')


    def __repr__(self):
        return '<Account %r>' % self.account_name
