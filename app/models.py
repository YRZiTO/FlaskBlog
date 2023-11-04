from datetime import datetime
from flask import current_app
from app import db, login_manager
from flask_login import UserMixin
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Create a class for the database
class User(db.Model, UserMixin):
    # Create the columns for the database
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    # Create a method to generate a token
    def get_reset_token(self):
        """Generate a token for the user to reset their password with a 30 minute expiration time"""
        s = Serializer(current_app.secret_key)
        return s.dumps({"user_id": self.id})

    # Create a static method to verify the token
    @staticmethod
    def verify_reset_token(token):
        """Verify the token to make sure it is valid and not expired before returning the user id"""
        s = Serializer(current_app.secret_key)
        try:
            user_id = s.loads(token, max_age=1800)["user_id"]
            # print(user_id)
        except:
            return None
        return User.query.get(user_id)

    # Create a method to print out the user's information
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    # Create the columns for the database
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # Create a method to print out the post's information
    def __repr__(self):
        return f"Post('{self.id}', '{self.title}', '{self.date_posted}')"
