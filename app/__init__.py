from flask import Flask, jsonify
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = 'DB.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "Hiro"  # Cookies encrypted
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    with app.app_context():
        from .views import views
        from .auth import auth
        db.create_all()

    app.register_blueprint(views, url_prefix='/wallet')
    app.register_blueprint(auth, url_prefix='/')

    from app.models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.route('/')
    def welcome():
        return jsonify("Welcome to Our Banking Application")

    return app
