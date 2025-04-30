# Full-Feature Flask Blog

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Flask-3.0.0-green.svg" alt="Flask Version">
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0.23-orange.svg" alt="SQLAlchemy Version">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</div>

<p align="center">
  A feature-rich, modular web blog application built with Flask and Python.
</p>

## 📋 Table of Contents

- [Features](#-features)
- [Technologies Used](#-technologies-used)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Usage](#-usage)
- [Future Enhancements](#-future-enhancements)
- [License](#-license)

## ✨ Features

### User Management
- **User Registration**: Create an account with username, email, and secure password
- **Authentication System**: Login with remembered sessions and secure cookies
- **Profile Management**: Update personal information and profile picture
- **Password Reset**: Recover account access via email

### Content Management
- **Create Posts**: Write and publish blog posts with rich text content
- **Update Posts**: Edit existing content with version tracking
- **Delete Posts**: Remove published content with confirmation
- **View Posts**: Read full articles with author information

### Navigation & UI
- **Responsive Design**: Optimized for all device sizes
- **Pagination**: Navigate through posts efficiently
- **User Profiles**: View all posts by a specific author
- **Error Pages**: Custom 404, 403, and 500 error pages

### Sidebar Features
- **Search**: Find posts by keywords in title or content
- **Latest Posts**: Quick access to the most recent content
- **Blog Statistics**: View post and user counts
- **Calendar**: Interactive monthly calendar widget

## 🛠 Technologies Used

- **Backend**: Python, Flask, SQLAlchemy, Flask-Bcrypt
- **Frontend**: HTML, CSS, Bootstrap 4, Jinja2 Templates
- **Database**: SQLite (easily configurable for other databases)
- **Authentication**: Flask-Login, itsdangerous for secure tokens
- **Forms**: WTForms with validation
- **Email**: Flask-Mail for password recovery
- **Image Processing**: Pillow for profile picture resizing

## 📥 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yrzito/FlaskBlog.git
   cd FlaskBlog
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate a Secret Key**:
   You need a secure secret key for the application. You can generate one using Python:
   ```python
   # In a Python terminal
   import secrets
   secrets.token_hex(16)
   # Output: '5d677f8902a7d99a760da7b95171d255' (example)
   ```
   Save this key for the next step.

5. **Configure the application**:
   Choose one of the configuration methods below (JSON file or environment variables).

6. **Initialize the database**:
   ```python
   # Run in Python shell
   from app import create_app, db
   app = create_app()
   with app.app_context():
       db.create_all()
   ```

## ⚙️ Configuration

There are two ways to configure the application: using a JSON file or environment variables. Choose the method that best fits your workflow and security requirements.

### Method 1: Using a JSON Configuration File

To configure the application using a JSON file:

```python
import os
import json

# Load configuration from an external JSON file
with open("/etc/configFlaskBlog.json") as config_file:
    config = json.load(config_file)

class Config:
    # Application settings
    SECRET_KEY = config.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = config.get("SQLALCHEMY_DATABASE_URI")
    
    # Email server settings
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config.get("EMAIL_USER")
    MAIL_PASSWORD = config.get("EMAIL_PASS")
```

**Steps to Set Up**:

1. Create a JSON file at `/etc/configFlaskBlog.json` with the following structure:
   ```json
   {
     "SECRET_KEY": "your_secure_secret_key",
     "SQLALCHEMY_DATABASE_URI": "sqlite:///site.db",
     "EMAIL_USER": "your_email@gmail.com",
     "EMAIL_PASS": "your_email_password"
   }
   ```

2. Secure the configuration file:
   ```bash
   sudo chmod 600 /etc/configFlaskBlog.json
   ```

### Method 2: Using Environment Variables

Alternatively, you can use environment variables for a more flexible and secure approach, especially in production or containerized environments:

1. **Modify the Config class** in `app/config.py`:

```python
import os

class Config:
    # Application settings
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    
    # Email server settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
```

2. **Set environment variables** before running the application:

   **For Linux/macOS**:
   ```bash
   export SECRET_KEY="your_generated_secret_key"
   export DATABASE_URL="sqlite:///site.db"
   export EMAIL_USER="your_email@gmail.com"
   export EMAIL_PASS="your_email_password"
   ```

   **For Windows (Command Prompt)**:
   ```cmd
   set SECRET_KEY=your_generated_secret_key
   set DATABASE_URL=sqlite:///site.db
   set EMAIL_USER=your_email@gmail.com
   set EMAIL_PASS=your_email_password
   ```

   **For Windows (PowerShell)**:
   ```powershell
   $env:SECRET_KEY="your_generated_secret_key"
   $env:DATABASE_URL="sqlite:///site.db"
   $env:EMAIL_USER="your_email@gmail.com"
   $env:EMAIL_PASS="your_email_password"
   ```

3. **For production environments**, consider using a `.env` file with a package like python-dotenv:

   Install the package:
   ```bash
   pip install python-dotenv
   ```

   Create a `.env` file in the project root (and add it to `.gitignore`):
   ```
   SECRET_KEY=your_generated_secret_key
   DATABASE_URL=sqlite:///site.db
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASS=your_email_password
   ```

   Then update Config class:
   ```python
   import os
   from dotenv import load_dotenv

   # Load environment variables from .env file
   load_dotenv()

   class Config:
       SECRET_KEY = os.environ.get('SECRET_KEY')
       # ... rest of your configuration ...
   ```

### Configuration Options
- `SECRET_KEY`: Used for securing sessions and tokens (generate with `secrets.token_hex()`)
- `SQLALCHEMY_DATABASE_URI` / `DATABASE_URL`: Database connection string
- `EMAIL_USER`: Email address for password reset functionality
- `EMAIL_PASS`: Email password or app password (for Gmail)
- `MAIL_SERVER`: SMTP server address (default: smtp.googlemail.com)
- `MAIL_PORT`: SMTP server port (default: 587)
- `MAIL_USE_TLS`: Whether to use TLS encryption (default: True)

### Securing Application
For production environments, never hardcode sensitive information. Use environment variables or external configuration files with restricted permissions. Make sure your secret key is:
- Sufficiently random (use `secrets.token_hex()`)
- At least 16 bytes long (32 hex characters)
- Kept confidential and not committed to version control

## 📁 Project Structure

```
FlaskBlog/
├── app/                       # Application package
│   ├── __init__.py            # Application factory
│   ├── config.py              # Configuration
│   ├── models.py              # Database models
│   ├── errors/                # Error handlers
│   ├── main/                  # Main routes blueprint
│   ├── posts/                 # Post management blueprint
│   ├── users/                 # User management blueprint
│   ├── utils/                 # Utility functions
│   ├── static/                # Static files (CSS, JS, etc.)
│   └── templates/             # Jinja2 templates
├── instance/                  # Application database
├── README.md                  # Project documentation and setup instructions
├── requirements.txt           # Python dependencies
├── LICENSE                    # MIT License file
└── run.py                     # Application entry point
```

## 🚀 Usage

1. **Start the development server**:
   ```bash
   python run.py
   ```

2. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

3. **Register an account**:
   Click "Register" and fill in your details

4. **Create your first post**:
   After logging in, click "New Post" to create content

## 🔮 Future Enhancements

- [ ] **Comments System**: Allow discussions on posts
- [ ] **Tags and Categories**: Organize content by topic
- [ ] **User Roles**: Admin, editor, and reader permissions
- [ ] **Rich Text Editor**: Enhanced post formatting options
- [ ] **Social Media Integration**: Share posts on various platforms
- [ ] **Search Enhancements**: Advanced filtering options
- [ ] **Analytics Dashboard**: Track post views and engagement
- [ ] **Favorite Posts**: Allow users to bookmark content

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<div align="center">
  <p>Developed with ❤️ by Yousif Zito</p>
  <p>
    <a href="https://github.com/yrzito">GitHub</a> •
    <a href="https://linkedin.com/in/yousifzito">LinkedIn</a> •
    <a href="mailto:yousifzito@gmail.com">Email</a>
  </p>
</div>