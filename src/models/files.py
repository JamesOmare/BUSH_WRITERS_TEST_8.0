from ..utils import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class File(UserMixin ,db.Model):
    """File model"""

    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key = True)
    doc_file = db.Column(db.Text, nullable=False, default = 'default.pdf')
    date_created = db.Column(db.DateTime (timezone = True), nullable=False, default = func.now())
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'CASCADE'))
    buyer_id = db.Column(db.String(10))
    date_modified = db.Column(db.DateTime(timezone = True), nullable=False, server_default=func.now(), onupdate=func.now())
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id', ondelete = 'CASCADE'))

    def __repr__(self):
        return '<File %r>' % self.id