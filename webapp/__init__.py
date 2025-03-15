from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
import os
from os import path

# Initialize Database
db = SQLAlchemy()
DB_NAME = "database.db"

socketio = SocketIO() 

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24).hex() 
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Import models
    from .models import User, Patient

    # Create database tables if not exists
    with app.app_context():
        db.create_all()
        from .populate_db import populate_database
        populate_database()

    # Import and register blueprints
    from .auth import auth
    from .routes import routes
    from .dashboard import dashboard #, create_dash_app

    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(routes, url_prefix="/")
    app.register_blueprint(dashboard, url_prefix='/')

    # Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(str(user_id))
    
    socketio.init_app(app)

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')