from app.extensions import db
from app.models.base import utc_now


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    payment_number = db.Column(db.String(80), nullable=False, unique=True, index=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=False, index=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id"), nullable=True, index=True)
    payment_date = db.Column(db.DateTime(timezone=True), nullable=True)
    amount = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    payment_method = db.Column(db.String(80), nullable=True)
    bank_account = db.Column(db.String(120), nullable=True)
    created_by_user_code = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )

    supplier = db.relationship("Supplier", back_populates="payments")
    invoice = db.relationship("Invoice", back_populates="payments")

    __table_args__ = (
        db.Index("ix_payments_duplicate_check", "supplier_id", "invoice_id", "amount", "payment_date"),
    )

    def __repr__(self) -> str:
        return f"<Payment {self.payment_number}>"
