import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = "cvpilot-secret-key"

    SQLALCHEMY_DATABASE_URI = \
        "sqlite:///" + os.path.join(
            BASE_DIR,
            "database",
            "cvpilot.db"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # NAYA — Resume upload settings
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASEDIR, "reports", "uploads")
    ALLOWED_EXTENSIONS = {"pdf", "docx"}
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB limit