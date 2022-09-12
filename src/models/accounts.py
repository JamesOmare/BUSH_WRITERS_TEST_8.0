from ..utils import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from enum import Enum

class AccountType(Enum):
    ARTICLE_ACCOUNT = 'article_account'
    ACADEMIC_WRITING_ACCOUNT = 'academic_writing_account'
    BLOGGING_ACCOUNT = 'blogging_account'


class Account(UserMixin ,db.Model):
    """Accounts model"""

    __tablename__ = 'accounts'
    account_id = db.Column(db.Integer, primary_key = True)
    account_type = db.Column(db.Enum(AccountType), default = AccountType.ACADEMIC_WRITING_ACCOUNT)
    description = db.Column(db.String(120), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    date_created = db.Column(db.DateTime (timezone = True), default = func.now())

    def __repr__(self):
        return '<Accounts %r>' % self.account_type