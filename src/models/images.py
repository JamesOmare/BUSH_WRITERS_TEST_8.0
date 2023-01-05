from ..utils import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Image(UserMixin ,db.Model):
    """User model"""

    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key = True)
    image_files = db.Column(db.Text, nullable=True, default = 'default.png')
    date_created = db.Column(db.DateTime (timezone = True), default = func.now())
    date_modified = db.Column(db.DateTime(timezone = True), nullable=False, server_default=func.now(), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'CASCADE'))
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id', ondelete = 'CASCADE'))

    def __repr__(self):
        return '<Image %r>' % self.id