import os
import uuid

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models.resume import Resume
from app.utils.validators import allowed_file, get_file_extension

resume_bp = Blueprint("resume", __name__)


@resume_bp.route("/resume/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        # Check if a file was actually submitted
        if "resume_file" not in request.files:
            flash("No file selected.", "error")
            return redirect(url_for("resume.upload"))

        file = request.files["resume_file"]

        if file.filename == "":
            flash("No file selected.", "error")
            return redirect(url_for("resume.upload"))

        allowed_extensions = current_app.config["ALLOWED_EXTENSIONS"]

        if not allowed_file(file.filename, allowed_extensions):
            flash("Invalid file type. Only PDF and DOCX files are allowed.", "error")
            return redirect(url_for("resume.upload"))

        # Secure the original filename (sanitizes special characters)
        original_filename = secure_filename(file.filename)
        file_ext = get_file_extension(original_filename)

        # Generate a unique stored filename to avoid collisions between users
        stored_filename = f"{uuid.uuid4().hex}.{file_ext}"

        upload_folder = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_folder, exist_ok=True)  # ensure folder exists

        file_path = os.path.join(upload_folder, stored_filename)
        file.save(file_path)

        # Get file size in KB
        file_size_kb = round(os.path.getsize(file_path) / 1024)

        # Save record in database
        new_resume = Resume(
            user_id=current_user.id,
            original_filename=original_filename,
            stored_filename=stored_filename,
            file_type=file_ext,
            file_size_kb=file_size_kb,
            status="uploaded"
        )

        db.session.add(new_resume)
        db.session.commit()

        flash("Resume uploaded successfully!", "success")
        return redirect(url_for("resume.history"))

    return render_template("dashboard/upload.html")


@resume_bp.route("/resume/history")
@login_required
def history():
    resumes = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.uploaded_at.desc()).all()
    return render_template("dashboard/history.html", resumes=resumes)


@resume_bp.route("/resume/delete/<int:resume_id>", methods=["POST"])
@login_required
def delete(resume_id):
    resume = Resume.query.get_or_404(resume_id)

    # Security check — user can only delete their own resumes
    if resume.user_id != current_user.id:
        flash("Unauthorized action.", "error")
        return redirect(url_for("resume.history"))

    # Delete the physical file
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    file_path = os.path.join(upload_folder, resume.stored_filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    db.session.delete(resume)
    db.session.commit()

    flash("Resume deleted successfully.", "success")
    return redirect(url_for("resume.history"))