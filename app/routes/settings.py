from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db, bcrypt

settings_bp = Blueprint("settings", __name__)


@settings_bp.route("/settings", methods=["GET"])
@login_required
def settings():
    return render_template("settings/settings.html")


@settings_bp.route("/settings/update-profile", methods=["POST"])
@login_required
def update_profile():
    full_name = request.form.get("full_name", "").strip()

    if not full_name:
        flash("Full name cannot be empty.", "error")
        return redirect(url_for("settings.settings"))

    current_user.full_name = full_name
    db.session.commit()

    flash("Profile updated successfully!", "success")
    return redirect(url_for("settings.settings"))


@settings_bp.route("/settings/change-password", methods=["POST"])
@login_required
def change_password():
    current_password = request.form.get("current_password", "")
    new_password = request.form.get("new_password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not bcrypt.check_password_hash(current_user.password, current_password):
        flash("Current password is incorrect.", "error")
        return redirect(url_for("settings.settings"))

    if len(new_password) < 6:
        flash("New password must be at least 6 characters long.", "error")
        return redirect(url_for("settings.settings"))

    if new_password != confirm_password:
        flash("New passwords do not match.", "error")
        return redirect(url_for("settings.settings"))

    current_user.password = bcrypt.generate_password_hash(new_password).decode("utf-8")
    db.session.commit()

    flash("Password changed successfully!", "success")
    return redirect(url_for("settings.settings"))