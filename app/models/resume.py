from datetime import datetime
from app.extensions import db


class Resume(db.Model):
    __tablename__ = "resumes"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    original_filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False)   # unique name saved on disk
    file_type = db.Column(db.String(10), nullable=False)          # 'pdf' or 'docx'
    file_size_kb = db.Column(db.Integer, nullable=True)

    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Future fields for analysis (filled later by ATS/parser modules)
    ats_score = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), default="uploaded")  # uploaded / analyzed / failed
    extracted_text = db.Column(db.Text, nullable=True)

    matched_keywords = db.Column(db.Text, nullable=True)   # comma-separated
    missing_keywords = db.Column(db.Text, nullable=True)   # comma-separated

    user = db.relationship("User", backref=db.backref("resumes", lazy=True))

    def __repr__(self):
        return f"<Resume {self.original_filename} - User {self.user_id}>"