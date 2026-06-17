from app.extensions import db
from app.models.base import utc_now


class PurchaseOrder(db.Model):
    __tablename__ = "purchase_orders"

    id = db.Column(db.Integer, primary_key=True)
    po_number = db.Column(db.String(80), nullable=False, unique=True, index=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=False, index=True)
    requester_user_code = db.Column(db.String(80), nullable=True)
    approver_user_code = db.Column(db.String(80), nullable=True)
    order_date = db.Column(db.Date, nullable=True)
    total_amount = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    status = db.Column(db.String(40), nullable=False, default="draft")
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )

    supplier = db.relationship("Supplier", back_populates="purchase_orders")
    invoices = db.relationship("Invoice", back_populates="purchase_order", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<PurchaseOrder {self.po_number}>"
