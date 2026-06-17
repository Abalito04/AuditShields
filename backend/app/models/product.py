from app.extensions import db
from app.models.base import utc_now


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(80), nullable=False, unique=True, index=True)
    name = db.Column(db.String(180), nullable=False)
    category = db.Column(db.String(120), nullable=True)
    unit_cost = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )

    inventory_snapshots = db.relationship(
        "InventorySnapshot", back_populates="product", lazy="dynamic"
    )
    stock_movements = db.relationship("StockMovement", back_populates="product", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<Product {self.sku}>"
