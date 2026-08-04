from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Database
db = SQLAlchemy()

# Password Hashing
bcrypt = Bcrypt()

# User Authentication
login_manager = LoginManager()

# Login Page
login_manager.login_view = "auth.login"

# Message Type
login_manager.login_message_category = "info"