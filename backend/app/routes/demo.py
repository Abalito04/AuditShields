from flask import Blueprint, flash, redirect, url_for
from flask_login import login_required

from app.services.fraud_engine import run_fraud_audit
from seed.seed_demo_data import seed_demo_data


demo_bp = Blueprint("demo", __name__, url_prefix="/demo")


@demo_bp.post("/reset")
@login_required
def reset():
    seed_demo_data()
    result = run_fraud_audit()
    flash(
        "Demo recreada. "
        f"Alertas nuevas: {result.alerts_created}. "
        f"Duplicadas ignoradas: {result.duplicates_ignored}. "
        f"Casos creados: {result.cases_created}.",
        "success",
    )
    return redirect(url_for("dashboard.index"))
