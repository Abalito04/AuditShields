from flask import Blueprint, render_template
from flask_login import login_required

from app.models import FraudRule
from app.services.dashboard_service import get_dashboard_metrics
from app.utils.labels import CASE_STATUS_LABELS, MODULE_LABELS, RISK_LEVEL_LABELS


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/")
@dashboard_bp.get("/dashboard")
@login_required
def index():
    metrics = get_dashboard_metrics()
    top_rules = []
    for rule_id, count in metrics["top_rules"]:
        rule = FraudRule.query.get(rule_id)
        if rule:
            top_rules.append({"rule": rule, "count": count})
    return render_template(
        "dashboard/index.html",
        metrics=metrics,
        top_rules=top_rules,
        case_status_labels=CASE_STATUS_LABELS,
        module_labels=MODULE_LABELS,
        risk_level_labels=RISK_LEVEL_LABELS,
    )
