from flask import Flask,url_for

from flask_jwt_extended import JWTManager

from apps.users.models import db
from apps.users.views import login, signup
from apps.posts.views import createPost, likePost, unlikePost, analiticLikes
from apps.events.views import userActivity


def config_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://star_navi:star_navi@localhost:5432/star_navi'
    db.init_app(app)
    db.app = app
    db.create_all()
    return app 

def config_JWT(app):
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    jwt = JWTManager(app)   
    return app

def add_router(app):
    app.view_functions['signup'] = signup
    app.view_functions['login'] = login
    app.view_functions['createPost'] = createPost
    app.view_functions['likePost'] = likePost
    app.view_functions['analiticLikes'] = analiticLikes
    app.view_functions['userActivity'] = userActivity
    app.view_functions['unlikePost'] = unlikePost
    
    
    app.add_url_rule('/login', 'login', login)
    app.add_url_rule('/signup', 'signup', signup)
    app.add_url_rule('/createPost', 'createPost', createPost)
    app.add_url_rule('/likePost', 'likePost', likePost)
    app.add_url_rule('/unlikePost', 'unlikePost', unlikePost)
    app.add_url_rule('/analiticLikes', 'analiticLikes', analiticLikes)
    app.add_url_rule('/userActivity', 'userActivity', userActivity)
    return app 


app = Flask(__name__)
app.config['DEBUG'] = True
app = config_db(app)
app = config_JWT(app)
app = add_router(app)
app.run()
