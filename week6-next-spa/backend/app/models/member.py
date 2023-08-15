from datetime import datetime
from app import db

class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    follower_count = db.Column(db.Integer, nullable=False, default=0)
    time = db.Column(db.DateTime, default=datetime.utcnow) 
    comments = db.relationship('Comment', backref='member', lazy=True)