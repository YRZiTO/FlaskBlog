from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Post
from app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from app.users.utils import save_picture, send_reset_email


users = Blueprint("users", __name__)

# Create a route for the registration page


@users.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user and add them to the database if the form is valid and the user doesn't already exist in the database"""
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        # Create a new user
        # user = User(username=form.username.data.lower(), email=form.email.data.lower(), password=hashed_password)
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)  # Add the user to the database
        db.session.commit()  # Commit the changes to the database
        flash("Your account has been created! You are now able to login.", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)


# Create a route for the login page
@users.route("/login", methods=["GET", "POST"])
def login():
    """Login a user if the form is valid and the user exists in the database and redirect them to the home page if they are already logged in"""
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(email=form.email.data.lower()).first()
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login Unsuccessful. Please check your email and password!", "danger")
    return render_template("login.html", title="Login", form=form)


# Create a route for the logout
@users.route("/logout")
def logout():
    """Logout a user and redirect them to the home page"""
    logout_user()
    return redirect(url_for("main.home"))


# Create a route for the account
@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """Update the account information if the form is valid and redirect the user to the account page if they are already logged in"""
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        # Redirect to the account page, this is to prevent the form from resubmitting when the page is refreshed
        # This is called a POST-GET redirect pattern and is a common practice in web development to prevent duplicate submissions of the form
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        "static", filename="profile_images/" + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form)


# Create a route for the user's posts
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template("user_posts.html", posts=posts, user=user)


# Create a route for the reset password
@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.", "info")
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", title="Reset Password", form=form)

# Create a route for the reset password token


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if not user:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()  # Commit the changes to the database
        flash("Your password has been updated! You are now able to login.", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title="Reset Password", form=form)
