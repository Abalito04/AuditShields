from flask import Blueprint
from flask_login import login_required

from app.routes.placeholders import render_section


inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.get("/products")
@login_required
def products():
    return render_section(
        "Productos",
        "Catalogo de productos, SKU, categorias, costos y estado.",
        "products",
    )


@inventory_bp.get("/stock")
@login_required
def stock():
    return render_section(
        "Stock",
        "Stock actual, snapshots fisicos y diferencias de inventario.",
        "inventory",
    )


@inventory_bp.get("/stock/movements")
@login_required
def stock_movements():
    return render_section(
        "Movimientos de stock",
        "Entradas, salidas, ajustes, transferencias y motivos asociados.",
        "inventory",
    )
