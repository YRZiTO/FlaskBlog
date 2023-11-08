from flask import Blueprint, render_template, request
from app.models import Post

main = Blueprint("main", __name__)

# Create a route for the home page


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    # Truncate the post content to a certain length (e.g., 300 characters)
    for post in posts.items:
        if len(post.content) > 300:
            post.content = f"{post.content[:300]}..."
    return render_template("home.html", posts=posts)


# Create a route for the about page
@main.route("/about")
def about():
    return render_template("about.html", title="About")
