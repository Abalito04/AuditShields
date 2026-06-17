from flask import Blueprint, flash, redirect, url_for
from flask_login import login_required

from app.services.fraud_engine import run_fraud_audit


audit_bp = Blueprint("audit", __name__, url_prefix="/audit")


@audit_bp.post("/run")
@login_required
def run():
    result = run_fraud_audit()
    if result.errors:
        flash(
            "Auditoria ejecutada con errores parciales: "
            + "; ".join(result.errors[:3]),
            "warning",
        )
    else:
        flash(
            "Auditoria ejecutada. "
            f"Reglas: {result.rules_executed}. "
            f"Alertas nuevas: {result.alerts_created}. "
            f"Duplicadas ignoradas: {result.duplicates_ignored}. "
            f"Casos creados: {result.cases_created}.",
            "success",
        )
    return redirect(url_for("dashboard.index"))
