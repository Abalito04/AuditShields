from datetime import datetime, timezone

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Case, CaseComment, CaseHistory, User
from app.services.audit_log_service import model_snapshot, record_audit_log
from app.utils.labels import CASE_ACTION_LABELS, CASE_STATUS_LABELS, RISK_LEVEL_LABELS


cases_bp = Blueprint("cases", __name__, url_prefix="/cases")

CASE_STATUSES = [
    "new",
    "in_review",
    "requires_documentation",
    "observed",
    "in_correction",
    "normalized",
    "false_positive",
    "confirmed",
    "escalated",
    "closed",
]
CASE_FIELDS = [
    "status",
    "assigned_to_user_id",
    "resolution_summary",
    "normalized_at",
    "closed_at",
]


@cases_bp.get("/")
@login_required
def index():
    query = Case.query
    risk_level = request.args.get("risk_level") or ""
    status = request.args.get("status") or ""

    if risk_level:
        query = query.filter(Case.risk_level == risk_level)
    if status:
        query = query.filter(Case.status == status)

    pagination = query.order_by(Case.created_at.desc()).paginate(
        page=request.args.get("page", 1, type=int), per_page=20, error_out=False
    )
    return render_template(
        "cases/index.html",
        pagination=pagination,
        filters={"risk_level": risk_level, "status": status},
        risk_levels=_distinct_values(Case.risk_level),
        statuses=CASE_STATUSES,
        risk_level_labels=RISK_LEVEL_LABELS,
        case_status_labels=CASE_STATUS_LABELS,
    )


@cases_bp.get("/<int:item_id>")
@login_required
def detail(item_id: int):
    audit_case = Case.query.get_or_404(item_id)
    users = User.query.filter_by(is_active=True).order_by(User.name.asc()).all()
    comments = audit_case.comments.order_by(CaseComment.created_at.asc()).all()
    history = audit_case.history.order_by(CaseHistory.created_at.desc()).all()
    return render_template(
        "cases/detail.html",
        audit_case=audit_case,
        statuses=CASE_STATUSES,
        users=users,
        comments=comments,
        history=history,
        risk_level_labels=RISK_LEVEL_LABELS,
        case_status_labels=CASE_STATUS_LABELS,
        case_action_labels=CASE_ACTION_LABELS,
    )


@cases_bp.post("/<int:item_id>/status")
@login_required
def update_status(item_id: int):
    audit_case = Case.query.get_or_404(item_id)
    new_status = request.form.get("status", "")
    resolution_summary = request.form.get("resolution_summary", "").strip() or None

    if new_status not in CASE_STATUSES:
        flash("Estado de caso no valido.", "danger")
        return redirect(url_for("cases.detail", item_id=audit_case.id))

    old_value = model_snapshot(audit_case, CASE_FIELDS)
    old_status = audit_case.status
    audit_case.status = new_status
    if resolution_summary is not None:
        audit_case.resolution_summary = resolution_summary
    if new_status == "normalized" and audit_case.normalized_at is None:
        audit_case.normalized_at = datetime.now(timezone.utc)
    if new_status == "closed" and audit_case.closed_at is None:
        audit_case.closed_at = datetime.now(timezone.utc)

    db.session.add(
        CaseHistory(
            case_id=audit_case.id,
            user_id=current_user.id,
            action="status_changed",
            from_status=old_status,
            to_status=new_status,
        )
    )
    record_audit_log(
        "case_status_changed",
        "case",
        audit_case.id,
        old_value=old_value,
        new_value=model_snapshot(audit_case, CASE_FIELDS),
    )
    db.session.commit()
    flash("Estado del caso actualizado.", "success")
    return redirect(url_for("cases.detail", item_id=audit_case.id))


@cases_bp.post("/<int:item_id>/comments")
@login_required
def add_comment(item_id: int):
    audit_case = Case.query.get_or_404(item_id)
    comment = request.form.get("comment", "").strip()
    if not comment:
        flash("El comentario no puede estar vacio.", "danger")
        return redirect(url_for("cases.detail", item_id=audit_case.id))

    db.session.add(CaseComment(case_id=audit_case.id, user_id=current_user.id, comment=comment))
    db.session.add(
        CaseHistory(
            case_id=audit_case.id,
            user_id=current_user.id,
            action="comment_added",
            from_status=audit_case.status,
            to_status=audit_case.status,
        )
    )
    record_audit_log(
        "case_comment_added",
        "case",
        audit_case.id,
        new_value={"comment": comment},
    )
    db.session.commit()
    flash("Comentario agregado.", "success")
    return redirect(url_for("cases.detail", item_id=audit_case.id))


@cases_bp.post("/<int:item_id>/assign")
@login_required
def assign(item_id: int):
    audit_case = Case.query.get_or_404(item_id)
    assigned_to_user_id = request.form.get("assigned_to_user_id") or None
    old_value = model_snapshot(audit_case, CASE_FIELDS)

    if assigned_to_user_id:
        user = User.query.get_or_404(int(assigned_to_user_id))
        audit_case.assigned_to_user_id = user.id
    else:
        audit_case.assigned_to_user_id = None

    db.session.add(
        CaseHistory(
            case_id=audit_case.id,
            user_id=current_user.id,
            action="assigned",
            from_status=audit_case.status,
            to_status=audit_case.status,
        )
    )
    record_audit_log(
        "case_assigned",
        "case",
        audit_case.id,
        old_value=old_value,
        new_value=model_snapshot(audit_case, CASE_FIELDS),
    )
    db.session.commit()
    flash("Responsable actualizado.", "success")
    return redirect(url_for("cases.detail", item_id=audit_case.id))


def _distinct_values(column):
    values = [row[0] for row in Case.query.with_entities(column).distinct().order_by(column).all()]
    return [value for value in values if value]
