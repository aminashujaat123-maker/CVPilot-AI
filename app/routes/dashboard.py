from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.models.resume import Resume

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    total_resumes = Resume.query.filter_by(user_id=current_user.id).count()

    latest_resume = Resume.query.filter_by(user_id=current_user.id)\
        .order_by(Resume.uploaded_at.desc()).first()

    analyzed_count = Resume.query.filter_by(
        user_id=current_user.id, status="analyzed"
    ).count()

    return render_template(
        "dashboard/dashboard.html",
        user=current_user,
        total_resumes=total_resumes,
        latest_resume=latest_resume,
        analyzed_count=analyzed_count
    )