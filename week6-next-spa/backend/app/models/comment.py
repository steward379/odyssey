from datetime import datetime
from app import db

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), nullable=False)
    like_count = db.Column(db.Integer, nullable=False, default=0)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    member_id = db.Column(db.BigInteger, db.ForeignKey('members.id'), nullable=False)
