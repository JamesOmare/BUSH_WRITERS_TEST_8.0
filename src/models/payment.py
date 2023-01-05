from ..utils import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Payment(db.Model):
    """Payment model"""

    
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key = True)
    buyer_id = db.Column(db.Integer, nullable = False)
    seller_id = db.Column(db.Integer, nullable = False)
    product_id = db.Column(db.Integer, nullable = False)
    status = db.Column(db.String(50), nullable = False)
    payment_method = db.Column(db.String(50), nullable = False)
    transaction_id = db.Column(db.String(50), nullable = False)
    country_code = db.Column(db.String(50), nullable = False)
    gross_pay = db.Column(db.Integer, nullable = False)
    paypal_fee = db.Column(db.Integer)
    paypal_email = db.Column(db.String(250))
    payment_number = db.Column(db.String(15))
    mpesa_fee = db.Column(db.Integer)
    net_pay = db.Column(db.Integer)
    currency_paid = db.Column(db.String(80), nullable = False)
    transaction_date = db.Column(db.String(50), nullable = False)
    transaction_time = db.Column(db.String(50), nullable = False)
    date_modified = db.Column(db.DateTime(timezone = True), nullable=False, server_default=func.now(), onupdate=func.now())
    


    def __repr__(self):
        return '<Payment %r>' % self.payment_method
