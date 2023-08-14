import os
import secrets
from PIL import Image
from flask import abort, render_template, url_for, flash, redirect, request
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from app.models import User, Post
from app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


# Create a route for the home page
@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template("home.html", posts=posts)


# Create a route for the about page
@app.route("/about")
def about():
    return render_template("about.html", title="About")


# Create a route for the registration page
@app.route("/register", methods=["GET","POST"])
def register():
    """Register a new user and add them to the database if the form is valid and the user doesn't already exist in the database"""
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
    """Login a user if the form is valid and the user exists in the database and redirect them to the home page if they are already logged in"""
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
    """Logout a user and redirect them to the home page"""
    logout_user()
    return redirect(url_for("home"))

def save_picture(form_picture):
    """Save the picture to the static/profile_images folder and return the picture filename"""
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
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_images/" + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form)


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect(url_for("home"))
    return render_template("create_post.html", title="New Post", form=form, legend="New Post")

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated!", "success")
        return redirect(url_for("post", post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title="Update Post", form=form, legend="Update Post")


@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("home"))
