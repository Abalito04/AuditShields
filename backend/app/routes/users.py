from flask import Blueprint
from flask_login import login_required

from app.routes.placeholders import render_section


users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.get("/")
@login_required
def index():
    return render_section(
        "Usuarios",
        "Usuarios internos, roles basicos y acceso administrativo.",
        "users",
    )
