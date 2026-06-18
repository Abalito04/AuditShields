from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user


landing_bp = Blueprint("landing", __name__)


@landing_bp.get("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    return render_template("landing/index.html")
