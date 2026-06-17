from flask import Blueprint
from flask_login import login_required

from app.routes.placeholders import render_section


cases_bp = Blueprint("cases", __name__, url_prefix="/cases")


@cases_bp.get("/")
@login_required
def index():
    return render_section(
        "Casos de auditoria",
        "Casos creados desde alertas para revision, normalizacion y cierre.",
        "cases",
    )
