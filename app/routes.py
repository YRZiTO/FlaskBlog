import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from app.models import User, Post
from app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

# Create a list of dictionaries to represent the posts
posts = [
    {
        "author": "Yousif Zito",
        "title": "Welcome to my page!",
        "content": "Veniam magna culpa consequat quis esse qui officia minim tempor ad qui reprehenderit velit. Ut in eu reprehenderit sit qui officia Lorem veniam quis commodo non ipsum minim. Duis officia aliquip culpa consectetur.",
        "date_posted": "May 4, 2023"
    },
    {
        "author": "Jane Doe",
        "title": "Welcome to Jane's page!",
        "content": "Est aliqua ad aliqua aliquip. Eiusmod tempor reprehenderit labore est ea sint sint est excepteur qui laboris. Proident fugiat exercitation nostrud amet Lorem eiusmod mollit irure consectetur id ex aliqua. Id esse dolor reprehenderit quis laborum. Ullamco fugiat pariatur voluptate ad do eiusmod qui esse amet sunt cillum. Nostrud pariatur anim qui qui eu. Est deserunt nostrud Lorem id laboris ad ea deserunt cillum esse aute consectetur veniam.",
        "date_posted": "May 5, 2023"
    },
]


# Create a route for the home page
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)


# Create a route for the about page
@app.route("/about")
def about():
    return render_template("about.html", title="About")


# Create a route for the registration page
@app.route("/register", methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        # Create a new user
        # user = User(username=form.username.data.lower(), email=form.email.data.lower(), password=hashed_password)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user) # Add the user to the database
        db.session.commit() # Commit the changes to the database
        flash("Your account has been created! You are now able to login.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


# Create a route for the login page
@app.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(email=form.email.data.lower()).first()
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check your email and password!", "danger")
    return render_template("login.html", title="Login", form=form)


# Create a route for the logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_images", picture_filename)
    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    return picture_filename

# Create a route for the account
@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
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
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_images/" + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form)
