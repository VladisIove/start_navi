from datetime import datetime

from apps.users.models import db 

class Post(db.Model):
    __tablename__ = 'posts_table'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False) 
    likes = db.relationship('Like', backref='post', lazy=True)

class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)    
    post_id = db.Column(db.Integer, db.ForeignKey('posts_table.id'),
        nullable=False)
    created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
