from flask import Blueprint
from flask_login import login_required

from app.routes.placeholders import render_section


reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


@reports_bp.get("/")
@login_required
def index():
    return render_section(
        "Reportes",
        "Exportaciones Excel para alertas, casos y resumen ejecutivo de riesgo.",
        "reports",
    )
