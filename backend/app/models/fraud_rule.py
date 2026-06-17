from app.extensions import db
from app.models.base import utc_now


class FraudRule(db.Model):
    __tablename__ = "fraud_rules"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=False, unique=True, index=True)
    name = db.Column(db.String(180), nullable=False)
    module = db.Column(db.String(80), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    risk_level_default = db.Column(db.String(30), nullable=False, default="medium")
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    config_json = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )

    alerts = db.relationship("Alert", back_populates="rule", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<FraudRule {self.code}>"
