from flask import Blueprint
from flask_login import login_required

from app.routes.placeholders import render_section


alerts_bp = Blueprint("alerts", __name__, url_prefix="/alerts")


@alerts_bp.get("/")
@login_required
def index():
    return render_section(
        "Alertas",
        "Alertas generadas por reglas antifraude claras y explicables.",
        "alerts",
    )
