from ..utils import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Confirmation(UserMixin ,db.Model):
    """Confirmation model"""

    __tablename__ = 'confirmation'
    id = db.Column(db.Integer, primary_key = True)
    confirmation_msg = db.Column(db.String(500), unique=True, nullable = False)
    buyer_id = db.Column(db.String(120) )
    buyer_email = db.Column(db.String(120))
    seller_id = db.Column(db.String(10))
    account_id = db.Column(db.String(10))
    is_rejected = db.Column(db.Boolean, default = False)
    is_accepted = db.Column(db.Boolean, default = False)
    time_posted = db.Column(db.DateTime(timezone = True), default = func.now())
    date_modified = db.Column(db.DateTime(timezone = True), nullable=False, server_default=func.now(), onupdate=func.now())
   
    def __repr__(self):
        return '<Confirmation %r>' % self.id

