import os
import uuid

from app.services.report import generate_resume_report
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models.resume import Resume
from app.utils.validators import allowed_file, get_file_extension
from app.services.parser import extract_text, basic_clean_text
from app.services.scoring import calculate_ats_score

resume_bp = Blueprint("resume", __name__)


@resume_bp.route("/resume/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
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

        original_filename = secure_filename(file.filename)
        file_ext = get_file_extension(original_filename)
        stored_filename = f"{uuid.uuid4().hex}.{file_ext}"

        upload_folder = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, stored_filename)
        file.save(file_path)

        file_size_kb = round(os.path.getsize(file_path) / 1024)

        raw_text = extract_text(file_path, file_ext)
        cleaned_text = basic_clean_text(raw_text) if raw_text else None

        new_resume = Resume(
            user_id=current_user.id,
            original_filename=original_filename,
            stored_filename=stored_filename,
            file_type=file_ext,
            file_size_kb=file_size_kb,
            status="uploaded" if cleaned_text else "failed",
            extracted_text=cleaned_text
        )

        db.session.add(new_resume)
        db.session.commit()

        if cleaned_text:
            flash("Resume uploaded and parsed successfully!", "success")
        else:
            flash("Resume uploaded, but text extraction failed. The file may be image-based or corrupted.", "error")

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

    if resume.user_id != current_user.id:
        flash("Unauthorized action.", "error")
        return redirect(url_for("resume.history"))

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    file_path = os.path.join(upload_folder, resume.stored_filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    db.session.delete(resume)
    db.session.commit()

    flash("Resume deleted successfully.", "success")
    return redirect(url_for("resume.history"))


@resume_bp.route("/resume/view/<int:resume_id>")
@login_required
def view(resume_id):
    resume = Resume.query.get_or_404(resume_id)

    if resume.user_id != current_user.id:
        flash("Unauthorized action.", "error")
        return redirect(url_for("resume.history"))

    return render_template("dashboard/analysis.html", resume=resume)


@resume_bp.route("/resume/analyze/<int:resume_id>")
@login_required
def analyze(resume_id):
    resume = Resume.query.get_or_404(resume_id)

    if resume.user_id != current_user.id:
        flash("Unauthorized action.", "error")
        return redirect(url_for("resume.history"))

    if not resume.extracted_text:
        flash("Cannot analyze this resume — text extraction failed earlier.", "error")
        return redirect(url_for("resume.history"))

    result = calculate_ats_score(resume.extracted_text)

    resume.ats_score = result["score"]
    resume.matched_keywords = ", ".join(result["matched_keywords"])
    resume.missing_keywords = ", ".join(result["missing_keywords"])
    resume.status = "analyzed"

    db.session.commit()

    return render_template(
        "dashboard/analysis.html",
        resume=resume,
        result=result
    )
@resume_bp.route("/resume/download-report/<int:resume_id>")
@login_required
def download_report(resume_id):
    from flask import send_file
    from app.services.scoring import calculate_ats_score

    resume = Resume.query.get_or_404(resume_id)

    if resume.user_id != current_user.id:
        flash("Unauthorized action.", "error")
        return redirect(url_for("resume.history"))

    if resume.ats_score is None or not resume.extracted_text:
        flash("Please analyze this resume before downloading the report.", "error")
        return redirect(url_for("resume.history"))

    result = calculate_ats_score(resume.extracted_text)

    reports_folder = os.path.join(os.getcwd(), "reports")
    os.makedirs(reports_folder, exist_ok=True)

    report_path = os.path.join(reports_folder, f"CVPilot_Report_{resume.id}.pdf")
    generate_resume_report(resume, result, report_path)

    return send_file(
        report_path,
        as_attachment=True,
        download_name=f"{resume.original_filename}_ATS_Report.pdf"
    )