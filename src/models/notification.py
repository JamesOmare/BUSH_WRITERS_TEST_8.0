from ..utils import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_admin.contrib.sqla import ModelView
from datetime import datetime


class Notification(UserMixin ,db.Model):
    """Notification model"""
    ACCOUNT_DETAILS_CONFIRMED_ALERT = 0
    ACCOUNT_DETAILS_REJECTED_ALERT = 1
    ACCOUNT_CREDENTIALS_ALERT = 2
    SUCCESSFUL_PURCHASE_ALERT = 3
    FAILED_PURCHASE_ALERT = 4
    FULLY_COMPLETED_PURCHASE_ALERT = 5
    REQUEST_FINAL_CREDENTIALS_ALERT = 6

    
   

    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key = True)
    buyer_id = db.Column(db.String(10))
    seller_id = db.Column(db.String(10))
    type = db.Column(db.SmallInteger, default = ACCOUNT_DETAILS_CONFIRMED_ALERT)
    intent_message = db.Column(db.Boolean, default=False)
    purchase_verification_message  = db.Column(db.Boolean, default=False)
    successful_purchase = db.Column(db.Boolean, default=False)
    failed_purchase = db.Column(db.Boolean, default=False)
    login_password = db.Column(db.String(120))
    login_email = db.Column(db.String(120))
    time_posted = db.Column(db.DateTime(timezone = True), default = func.now())
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id', ondelete = 'CASCADE'))
    
    def __repr__(self):
        return '<Notification %r>' % self.id