import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_database(app):
    if not os.path.exists(os.join(os.path.dirname(__file__), DB_NAME)):
        db.create_all(app=app)
        print("База данных успешно создана")


def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = "x7qkW}q}crHNxkc8/WJ34b8bWZYPpPWP%_C<QkL"
    
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    create_database(app)
    
    from . import models
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get(int(id))
    
    return app
