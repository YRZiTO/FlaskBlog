import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

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

from app import routes