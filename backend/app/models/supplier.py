from app.extensions import db
from app.models.base import utc_now


class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True)
    supplier_code = db.Column(db.String(80), nullable=False, unique=True, index=True)
    name = db.Column(db.String(180), nullable=False)
    tax_id = db.Column(db.String(80), nullable=True, index=True)
    bank_account = db.Column(db.String(120), nullable=True, index=True)
    address = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    created_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(40), nullable=False, default="active")
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )

    purchase_orders = db.relationship("PurchaseOrder", back_populates="supplier", lazy="dynamic")
    invoices = db.relationship("Invoice", back_populates="supplier", lazy="dynamic")
    payments = db.relationship("Payment", back_populates="supplier", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<Supplier {self.supplier_code}>"
