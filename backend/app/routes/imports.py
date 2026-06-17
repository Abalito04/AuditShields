from flask import Blueprint
from flask_login import login_required

from app.routes.placeholders import render_section


imports_bp = Blueprint("imports", __name__, url_prefix="/imports")


@imports_bp.get("/")
@login_required
def index():
    return render_section(
        "Importaciones",
        "Carga masiva Excel/CSV, validaciones por fila y trazabilidad de archivos.",
        "imports",
    )
