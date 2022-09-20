from ..utils import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Image(UserMixin ,db.Model):
    """User model"""

    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key = True)
    image_file = db.Column(db.String(100), nullable=True)
    date_created = db.Column(db.DateTime (timezone = True), default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'CASCADE'))

    def __repr__(self):
        return '<Image %r>' % self.image_file