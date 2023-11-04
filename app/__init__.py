from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config

# Create an instance of the SQLAlchemy class
db = SQLAlchemy()
# Create an instance of the Bcrypt class
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"  # We pass the function name of the route
login_manager.login_message_category = "info"
mail = Mail()


def create_app(config_class=Config):
    # Create an instance of the Flask class
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.main.routes import main
    from app.posts.routes import posts
    from app.users.routes import users
    from app.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
