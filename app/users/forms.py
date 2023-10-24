from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User


# Create a class for the registration form
class RegistrationForm(FlaskForm):  # Inherit from FlaskForm
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), Length(min=8), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """Check if the username is already taken"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is already taken! Please choose a different one.")

    def validate_email(self, email):
        """Check if the email is already taken"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email address is already registered!")

# Create a class for the login form


class LoginForm(FlaskForm):  # Inherit from FlaskForm
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):  # Inherit from FlaskForm
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField("Update Profile Picture", validators=[
                        FileAllowed(["jpg", "jpeg", "png", "gif"])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        """Check if the username is already taken"""
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "That username is already taken! Please choose a different one.")

    def validate_email(self, email):
        """Check if the email is already taken"""
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("That email address is already taken!")


class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        """Check if the email is already taken"""
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                "Email address not found. Please check your email or sign up for an account.")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), Length(min=8), EqualTo('password')])
    submit = SubmitField("Reset Password")
