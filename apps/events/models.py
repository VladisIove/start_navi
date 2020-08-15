from datetime import datetime

from apps.users.models import db 

class Event(db.Model):
    __tablename__ = 'posts'

    class TypeActivity:
        Login = 1
        Request = 2

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False) 
    created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    type_active = db.Column(db.Integer)