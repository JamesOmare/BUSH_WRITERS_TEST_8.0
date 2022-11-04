from ..utils import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_admin.contrib.sqla import ModelView
from datetime import datetime


class Complaints(UserMixin ,db.Model):
    """Complaints model"""

    __tablename__ = 'complaint'
    id = db.Column(db.Integer, primary_key = True)
    buyer_id = db.Column(db.Integer)
    seller_id = db.Column(db.Integer)
    buyer_number = db.Column(db.Integer)
    seller_number = db.Column(db.Integer)
    reason = db.Column(db.String(50))
    further_description = db.Column(db.String(250))
    time_posted = db.Column(db.DateTime(timezone = True), default = func.now())

    def __repr__(self):
        return '<Complaint %r>' % self.id

