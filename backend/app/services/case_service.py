from datetime import datetime, timezone

from flask import has_request_context
from flask_login import current_user

from app.extensions import db
from app.models import Alert, Case, CaseHistory


def create_case_for_alert(alert: Alert) -> Case:
    case = Case(
        case_number=_next_case_number(),
        alert=alert,
        title=alert.title,
        description=alert.description,
        risk_score=alert.risk_score,
        risk_level=alert.risk_level,
        status="new",
    )
    db.session.add(case)
    db.session.flush()
    db.session.add(
        CaseHistory(
            case_id=case.id,
            user_id=_current_user_id(),
            action="case_created_from_alert",
            from_status=None,
            to_status="new",
        )
    )
    return case


def _next_case_number() -> str:
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    prefix = f"AS-{today}-"
    last_case = (
        Case.query.filter(Case.case_number.like(f"{prefix}%"))
        .order_by(Case.case_number.desc())
        .first()
    )
    if not last_case:
        return f"{prefix}0001"
    last_number = int(last_case.case_number.rsplit("-", 1)[1])
    return f"{prefix}{last_number + 1:04d}"


def _current_user_id() -> int | None:
    if not has_request_context():
        return None
    return current_user.id if current_user.is_authenticated else None
