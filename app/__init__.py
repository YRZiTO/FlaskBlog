import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

# Set the base directory
basedir = os.path.abspath(os.path.dirname(__file__))
# Create an instance of the Flask class
app = Flask(__name__)
# Set the secret key to protect against modifying cookies and cross-site request forgery attacks
app.config['SECRET_KEY'] = 'a968985285e687c30db75e72fb479c19'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
# Create an instance of the SQLAlchemy class
db = SQLAlchemy(app)
# Create an instance of the Bcrypt class
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login" # We pass the function name of the route
login_manager.login_message_category = "info"
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_USER")
app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_PASS")
mail = Mail(app)

from app import routes