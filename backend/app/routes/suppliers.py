from flask import Blueprint
from flask_login import login_required

from app.routes.placeholders import render_section


suppliers_bp = Blueprint("suppliers", __name__, url_prefix="/suppliers")


@suppliers_bp.get("/")
@login_required
def index():
    return render_section(
        "Proveedores",
        "Catalogo de proveedores, datos fiscales, bancarios y estado operativo.",
        "suppliers",
    )
