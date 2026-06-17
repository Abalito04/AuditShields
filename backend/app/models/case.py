from app.extensions import db
from app.models.base import utc_now


class Case(db.Model):
    __tablename__ = "cases"

    id = db.Column(db.Integer, primary_key=True)
    case_number = db.Column(db.String(80), nullable=False, unique=True, index=True)
    alert_id = db.Column(db.Integer, db.ForeignKey("alerts.id"), nullable=False, unique=True)
    title = db.Column(db.String(220), nullable=False)
    description = db.Column(db.Text, nullable=False)
    risk_score = db.Column(db.Integer, nullable=False, default=0)
    risk_level = db.Column(db.String(30), nullable=False, default="low", index=True)
    status = db.Column(db.String(60), nullable=False, default="new", index=True)
    assigned_to_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)
    resolution_summary = db.Column(db.Text, nullable=True)
    normalized_at = db.Column(db.DateTime(timezone=True), nullable=True)
    closed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )

    alert = db.relationship("Alert", back_populates="case")
    assigned_to = db.relationship("User", back_populates="assigned_cases")
    comments = db.relationship("CaseComment", back_populates="case", lazy="dynamic")
    history = db.relationship("CaseHistory", back_populates="case", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<Case {self.case_number}>"


class CaseComment(db.Model):
    __tablename__ = "case_comments"

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey("cases.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)

    case = db.relationship("Case", back_populates="comments")
    user = db.relationship("User", back_populates="case_comments")

    def __repr__(self) -> str:
        return f"<CaseComment case_id={self.case_id}>"


class CaseHistory(db.Model):
    __tablename__ = "case_history"

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey("cases.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)
    action = db.Column(db.String(120), nullable=False)
    from_status = db.Column(db.String(60), nullable=True)
    to_status = db.Column(db.String(60), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)

    case = db.relationship("Case", back_populates="history")
    user = db.relationship("User", back_populates="case_history_entries")

    def __repr__(self) -> str:
        return f"<CaseHistory case_id={self.case_id} action={self.action}>"
