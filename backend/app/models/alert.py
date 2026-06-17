from app.extensions import db
from app.models.base import utc_now


class Alert(db.Model):
    __tablename__ = "alerts"

    id = db.Column(db.Integer, primary_key=True)
    rule_id = db.Column(db.Integer, db.ForeignKey("fraud_rules.id"), nullable=False, index=True)
    module = db.Column(db.String(80), nullable=False, index=True)
    entity_type = db.Column(db.String(80), nullable=False, index=True)
    entity_id = db.Column(db.Integer, nullable=True, index=True)
    title = db.Column(db.String(220), nullable=False)
    description = db.Column(db.Text, nullable=False)
    risk_score = db.Column(db.Integer, nullable=False, default=0)
    risk_level = db.Column(db.String(30), nullable=False, default="low", index=True)
    amount_at_risk = db.Column(db.Numeric(14, 2), nullable=True)
    evidence_json = db.Column(db.JSON, nullable=True)
    status = db.Column(db.String(40), nullable=False, default="open", index=True)
    fingerprint = db.Column(db.String(255), nullable=False, unique=True, index=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now, index=True)

    rule = db.relationship("FraudRule", back_populates="alerts")
    case = db.relationship("Case", back_populates="alert", uselist=False)

    def __repr__(self) -> str:
        return f"<Alert {self.fingerprint}>"
