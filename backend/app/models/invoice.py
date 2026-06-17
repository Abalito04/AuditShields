from app.extensions import db
from app.models.base import utc_now


class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(80), nullable=False, index=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=False, index=True)
    purchase_order_id = db.Column(
        db.Integer, db.ForeignKey("purchase_orders.id"), nullable=True, index=True
    )
    issue_date = db.Column(db.Date, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    total_amount = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    status = db.Column(db.String(40), nullable=False, default="pending")
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )

    supplier = db.relationship("Supplier", back_populates="invoices")
    purchase_order = db.relationship("PurchaseOrder", back_populates="invoices")
    payments = db.relationship("Payment", back_populates="invoice", lazy="dynamic")

    __table_args__ = (
        db.Index("ix_invoices_supplier_number_amount", "supplier_id", "invoice_number", "total_amount"),
    )

    def __repr__(self) -> str:
        return f"<Invoice {self.invoice_number}>"
