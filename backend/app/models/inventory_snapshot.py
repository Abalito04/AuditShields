from app.extensions import db
from app.models.base import utc_now


class InventorySnapshot(db.Model):
    __tablename__ = "inventory_snapshots"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False, index=True)
    snapshot_date = db.Column(db.Date, nullable=False, index=True)
    expected_quantity = db.Column(db.Numeric(14, 3), nullable=False, default=0)
    physical_quantity = db.Column(db.Numeric(14, 3), nullable=False, default=0)
    difference_quantity = db.Column(db.Numeric(14, 3), nullable=False, default=0)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)

    product = db.relationship("Product", back_populates="inventory_snapshots")

    def __repr__(self) -> str:
        return f"<InventorySnapshot product_id={self.product_id} date={self.snapshot_date}>"
