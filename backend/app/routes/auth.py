from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.models import User


auth_bp = Blueprint("auth", __name__)


@auth_bp.get("/login")
def login_form():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    return render_template("auth/login.html")


@auth_bp.post("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if not email or not password:
        flash("Ingresa email y contrasena.", "warning")
        return render_template("auth/login.html"), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.is_active or not user.check_password(password):
        flash("Credenciales invalidas.", "danger")
        return render_template("auth/login.html"), 401

    login_user(user)
    flash("Sesion iniciada correctamente.", "success")
    next_url = request.args.get("next")
    return redirect(next_url or url_for("dashboard.index"))


@auth_bp.post("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesion cerrada.", "info")
    return redirect(url_for("auth.login_form"))
