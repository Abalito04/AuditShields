from flask import Blueprint
from flask_login import login_required

from app.routes.placeholders import render_section


purchases_bp = Blueprint("purchases", __name__)


@purchases_bp.get("/purchase-orders")
@login_required
def purchase_orders():
    return render_section(
        "Ordenes de compra",
        "Ordenes, solicitantes, aprobadores, montos y estados de aprobacion.",
        "purchases",
    )


@purchases_bp.get("/invoices")
@login_required
def invoices():
    return render_section(
        "Facturas",
        "Facturas de proveedores, vencimientos, montos y vinculo con ordenes.",
        "invoices",
    )


@purchases_bp.get("/payments")
@login_required
def payments():
    return render_section(
        "Pagos",
        "Pagos registrados, metodos, cuentas y relacion con facturas.",
        "payments",
    )
