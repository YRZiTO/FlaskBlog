import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Set the base directory
basedir = os.path.abspath(os.path.dirname(__file__))
# Create an instance of the Flask class
app = Flask(__name__)
# Set the secret key to protect against modifying cookies and cross-site request forgery attacks
app.config['SECRET_KEY'] = 'a968985285e687c30db75e72fb479c19'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
db = SQLAlchemy(app)


from app import routes