from flask import request, jsonify

from .models import db, User
from apps.events.models import Event
from apps.errors import NotValidData, RepeatEmail, WrongPasswordOrEmail



def login():
    data = request.get_json()

    if data is None or  None in [data.get('password',None),data.get('email', None)]:
        return jsonify({'code': NotValidData.code, 'description': NotValidData.description})
    
    user = User.query.filter_by(email=data['email']).first()
    if user is None :
        return jsonify({'code': WrongPasswordOrEmail.code, 'description': WrongPasswordOrEmail.description})
    if User.verify_password(user.password, data['password']):
        event = Event(user_id=user.id, type_active=Event.TypeActivity.Login)
        db.session.add(event)
        db.session.commit()
        token = user.get_token()
        return jsonify({
            'token': token
        }) 
    return jsonify({'code': WrongPasswordOrEmail.code, 'description': WrongPasswordOrEmail.description})
login.methods = ['POST',]

def signup():
    data = request.get_json()

    if data is None or  None in [data.get('password',None),data.get('email', None)]:
        return jsonify({'code': NotValidData.code, 'description': NotValidData.description})

    if User.query.filter_by(email=data['email']).first() is not None:
        return jsonify({'code': RepeatEmail.code, 'description': RepeatEmail.description})

    user = User(email=data['email'], password=User.hash_password(data['password']))
    token = user.get_token()
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'token': token
    })
signup.methods = ['POST',]