import os
import json

with open("/etc/configFlaskBlog.json") as config_file:
    config = json.load(config_file)

class Config:
    # Set the base directory
    # basedir = os.path.abspath(os.path.dirname(__file__))
    # Set the secret key to protect against modifying cookies and cross-site request forgery attacks
    SECRET_KEY = config.get("SECRET_KEY")
    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "site.db")
    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_DATABASE_URI = config.get("SQLALCHEMY_DATABASE_URI")
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config.get("EMAIL_USER")
    MAIL_PASSWORD = config.get("EMAIL_PASS")
