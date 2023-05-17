from flask import render_template, url_for, flash, redirect
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post
from app import app


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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


# Create a route for the login page
@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if (form.email.data == "email@gmail.com" and form.password.data == "password"):
            flash(f"You've successfully logged in!\nWelcome back {form.email.data}!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful.\nPlease check your email and password!", "danger")
    return render_template("login.html", title="Login", form=form)


