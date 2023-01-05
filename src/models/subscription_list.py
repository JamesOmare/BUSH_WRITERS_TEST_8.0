from ..utils import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Subscription(UserMixin ,db.Model):
    """Subscription model"""

    __tablename__ = 'subscription'
    id = db.Column(db.Integer, primary_key = True)
    client_email = db.Column(db.String(120), nullable = False )
    time_posted = db.Column(db.DateTime(timezone = True), default = func.now())
    date_modified = db.Column(db.DateTime(timezone = True), nullable=False, server_default=func.now(), onupdate=func.now())
   
    def __repr__(self):
        return '<Subscription %r>' % self.id

