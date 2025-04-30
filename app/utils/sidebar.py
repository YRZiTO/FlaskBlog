from app.models import Post, User
import calendar
from datetime import datetime

def sidebar_context():
    """Context processor for sidebar data to be available across all templates"""
    # Get latest 5 posts
    recent_posts = Post.query.order_by(Post.date_posted.desc()).limit(5).all()
    
    # Get total posts and users
    total_posts = Post.query.count()
    total_users = User.query.count()
    
    # Calendar data
    now = datetime.now()
    cal = calendar.monthcalendar(now.year, now.month)
    current_month_year = now.strftime("%B %Y")
    current_day = now.day
    current_week_day = now.weekday() + 1  # +1 because Python's weekday starts at 0 for Monday
    
    return dict(
        recent_posts=recent_posts,
        total_posts=total_posts,
        total_users=total_users,
        calendar_weeks=cal,
        current_month_year=current_month_year,
        current_day=current_day,
        current_week_day=current_week_day
    )