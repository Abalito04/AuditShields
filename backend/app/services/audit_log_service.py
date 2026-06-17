from flask_login import current_user

from app.extensions import db
from app.models import AuditLog


def model_snapshot(model, fields: list[str]) -> dict:
    snapshot = {}
    for field in fields:
        value = getattr(model, field)
        snapshot[field] = str(value) if value is not None else None
    return snapshot


def record_audit_log(
    action: str,
    entity_type: str,
    entity_id: int | None = None,
    old_value: dict | None = None,
    new_value: dict | None = None,
) -> None:
    user_id = current_user.id if current_user.is_authenticated else None
    db.session.add(
        AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            old_value=old_value,
            new_value=new_value,
        )
    )
