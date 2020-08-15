from datetime import datetime

from flask import request, jsonify

from flask_jwt_extended import jwt_required

from .models import Post, Like
from apps.users.models import db, User
from apps.events.models import Event
from apps.errors import NotValidData

@jwt_required
def createPost():
    data = request.get_json()

    if (data is None or None in [data.get('text',None),data.get('author_id', None)]):
        return jsonify({'code': NotValidData.code, 'description': NotValidData.description})

    if User.query.filter_by(id=data['author_id']).first() is None:
        return jsonify({'code': NotValidData.code, 'description': NotValidData.description})
        
    post = Post(author_id=data['author_id'], text=data['text'])
    event = Event(user_id=data['author_id'], type_active=Event.TypeActivity.Request)
    db.session.add(post)
    db.session.add(event)
    db.session.commit()
    return jsonify({
        'id': post.id,
        'text': post.text,
        'author_id': post.author_id
    })
createPost.methods=['POST']   

@jwt_required
def likePost():
    data = request.get_json()

    if (data is None or  None in [data.get('post_id',None),data.get('user_id', None)]):
        return jsonify({'code': NotValidData.code, 'description': NotValidData.description})

    if User.query.filter_by(id=data['user_id']).first() is None or Post.query.filter_by(id=data['post_id']).first() is None:
        return jsonify({'code': NotValidData.code, 'description': NotValidData.description})

    like = Like(user_id=data['user_id'], post_id=data['post_id'])
    db.session.add(like)
    db.session.commit()
    return jsonify({
        'id': like.id,
        'user_id': like.user_id,
        'post_id': like.post_id,
        'date_created': like.created
    })
likePost.methods = ['POST',]

@jwt_required
def unlikePost():
    data = request.get_json()

    if (data is None or  None in [data.get('post_id',None),data.get('user_id', None), data.get('like_id')]):
        return jsonify({'code': NotValidData.code, 'description': NotValidData.description})

    if User.query.filter_by(id=data['user_id']).first() is None or Post.query.filter_by(id=data['post_id']).first() is None:
        return jsonify({'code': NotValidData.code, 'description': NotValidData.description})

    like = Like.query.filter_by(user_id=data['user_id'], post_id=data['post_id'], id=data['like_id']).first()
    if like is None:
        return jsonify({'code': NotValidData.code, 'description': NotValidData.description})
    
    db.session.delete(like)
    event = Event(user_id=data['user_id'], type_active=Event.TypeActivity.Request)
    db.session.add(event)
    db.session.commit()
    return jsonify({
        'id': like.id,
        'user_id': like.user_id,
        'post_id': like.post_id,
        'date_created': like.created
    })
unlikePost.methods = ['POST',]

@jwt_required
def analiticLikes():
    date_from = request.args.get('date_from', None)
    date_to = request.args.get('date_to', None)
    if None in [date_from, date_to]:
        return jsonify({'code': NotValidData.code, 'description': NotValidData.description})
    date_from = datetime.strptime(date_from, '%d-%m-%Y')
    date_to = datetime.strptime(date_to, '%d-%m-%Y')
    from sqlalchemy import func
    query = Like.query.with_entities(Like.created, func.sum(Like.id))\
                .filter(Like.created >= date_from)\
                .filter(Like.created <= date_to)\
                .group_by(Like.created).all()
    data = [ {'date': q[0], 'count_like': q[1]}for q in query]
    return jsonify(data)
analiticLikes.methods=['POST']
