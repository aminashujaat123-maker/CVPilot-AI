from flask import Flask

from config import Config
from app.extensions import db, bcrypt, login_manager


def create_app():
    app = Flask(__name__)

    print("Current File:", __file__)
    print("Template Folder:", app.template_folder)

    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    return app