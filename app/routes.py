from flask import render_template, url_for, flash, redirect, request
from app.forms import RegistrationForm, LoginForm
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
        user = User(username=form.username.data.lower(), email=form.email.data.lower(), password=hashed_password)
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
        user = User.query.filter_by(email=form.email.data.lower()).first()
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


# Create a route for the account
@app.route("/account")
@login_required
def account():
    return render_template("account.html", title="Account")
