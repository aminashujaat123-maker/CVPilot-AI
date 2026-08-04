import os
from flask import Flask

from config import Config
from app.extensions import db, bcrypt, login_manager



def create_app():
    basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    app = Flask(
        __name__,
        template_folder=os.path.join(basedir, 'templates'),
        static_folder=os.path.join(basedir, 'static')
    )

    app.config.from_object(Config)

    app.config["MAX_CONTENT_LENGTH"] = Config.MAX_CONTENT_LENGTH

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"          # NAYA — agar login required page pe unauthenticated user aaye to yahan redirect hoga
    login_manager.login_message_category = "error"    # NAYA — flash message ka style

    from app.models.user import User
    from app.models.resume import Resume

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    # Register blueprints — NAYA
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.resume import resume_bp
    app.register_blueprint(resume_bp)

    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)
    from app.routes.settings import settings_bp
    app.register_blueprint(settings_bp)

    return app