from flask import request, jsonify

from flask_jwt_extended import jwt_required

from apps.errors import NotValidData
from .models import Event

@jwt_required
def userActivity():
    data = request.get_json()
    if data is None and data.get('user_id', Nine) is None:
        return jsonify({'code': NotValidData.code, 'description': NotValidData.description})
    events = Event.query.filter_by(user_id=data['user_id'])

    respone = [ {'id': event.id, 
                'user_id': event.user_id,
                'created': str(event.created), 
                'type_active': 'login' if event.type_active is Event.TypeActivity.Login else 'request'
                } for event in events]
    return jsonify(respone)
userActivity.methods=['GET']