from decimal import Decimal

from sqlalchemy import func

from app.models import Alert, Case


OPEN_CASE_STATUSES = {
    "new",
    "in_review",
    "requires_documentation",
    "observed",
    "in_correction",
    "confirmed",
    "escalated",
}


def get_dashboard_metrics() -> dict:
    active_alerts = Alert.query.filter(Alert.status == "open").count()
    open_cases = Case.query.filter(Case.status.in_(OPEN_CASE_STATUSES)).count()
    critical_cases = Case.query.filter(
        Case.status.in_(OPEN_CASE_STATUSES),
        Case.risk_level == "critical",
    ).count()
    amount_at_risk = (
        Alert.query.filter(Alert.status == "open")
        .with_entities(func.coalesce(func.sum(Alert.amount_at_risk), 0))
        .scalar()
        or Decimal("0")
    )

    suppliers_observed = (
        Alert.query.filter(
            Alert.status == "open",
            Alert.entity_type == "supplier",
        )
        .with_entities(func.count(func.distinct(Alert.entity_id)))
        .scalar()
        or 0
    )
    products_observed = (
        Alert.query.filter(
            Alert.status == "open",
            Alert.entity_type.in_(["product", "inventory_snapshot", "stock_movement"]),
        )
        .with_entities(func.count(Alert.id))
        .scalar()
        or 0
    )

    cases_by_status = (
        Case.query.with_entities(Case.status, func.count(Case.id))
        .group_by(Case.status)
        .order_by(func.count(Case.id).desc())
        .all()
    )
    alerts_by_module = (
        Alert.query.with_entities(Alert.module, func.count(Alert.id))
        .group_by(Alert.module)
        .order_by(func.count(Alert.id).desc())
        .all()
    )
    top_rules = (
        Alert.query.join(Alert.rule)
        .with_entities(Alert.rule_id, func.count(Alert.id))
        .group_by(Alert.rule_id)
        .order_by(func.count(Alert.id).desc())
        .limit(5)
        .all()
    )
    latest_cases = Case.query.order_by(Case.created_at.desc()).limit(8).all()

    return {
        "active_alerts": active_alerts,
        "open_cases": open_cases,
        "critical_cases": critical_cases,
        "amount_at_risk": amount_at_risk,
        "suppliers_observed": suppliers_observed,
        "products_observed": products_observed,
        "cases_by_status": cases_by_status,
        "alerts_by_module": alerts_by_module,
        "top_rules": top_rules,
        "latest_cases": latest_cases,
    }
