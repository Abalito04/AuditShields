import json

from flask import Blueprint, render_template, request
from flask_login import login_required

from app.models import Alert
from app.utils.labels import (
    ALERT_STATUS_LABELS,
    ENTITY_TYPE_LABELS,
    MODULE_LABELS,
    RISK_LEVEL_LABELS,
)


alerts_bp = Blueprint("alerts", __name__, url_prefix="/alerts")


@alerts_bp.get("/")
@login_required
def index():
    query = Alert.query
    module = request.args.get("module") or ""
    risk_level = request.args.get("risk_level") or ""
    status = request.args.get("status") or ""

    if module:
        query = query.filter(Alert.module == module)
    if risk_level:
        query = query.filter(Alert.risk_level == risk_level)
    if status:
        query = query.filter(Alert.status == status)

    pagination = query.order_by(Alert.created_at.desc()).paginate(
        page=request.args.get("page", 1, type=int), per_page=20, error_out=False
    )
    return render_template(
        "alerts/index.html",
        pagination=pagination,
        filters={"module": module, "risk_level": risk_level, "status": status},
        modules=_distinct_values(Alert.module),
        risk_levels=_distinct_values(Alert.risk_level),
        statuses=_distinct_values(Alert.status),
        module_labels=MODULE_LABELS,
        risk_level_labels=RISK_LEVEL_LABELS,
        alert_status_labels=ALERT_STATUS_LABELS,
    )


@alerts_bp.get("/<int:item_id>")
@login_required
def detail(item_id: int):
    alert = Alert.query.get_or_404(item_id)
    evidence_json = json.dumps(alert.evidence_json or {}, indent=2, ensure_ascii=False)
    return render_template(
        "alerts/detail.html",
        alert=alert,
        evidence_json=evidence_json,
        module_labels=MODULE_LABELS,
        risk_level_labels=RISK_LEVEL_LABELS,
        alert_status_labels=ALERT_STATUS_LABELS,
        entity_type_labels=ENTITY_TYPE_LABELS,
    )


def _distinct_values(column):
    values = [row[0] for row in Alert.query.with_entities(column).distinct().order_by(column).all()]
    return [value for value in values if value]
