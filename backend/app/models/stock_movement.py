from app.extensions import db
from app.models.base import utc_now


class StockMovement(db.Model):
    __tablename__ = "stock_movements"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False, index=True)
    movement_type = db.Column(db.String(30), nullable=False)
    quantity = db.Column(db.Numeric(14, 3), nullable=False)
    movement_date = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    reference = db.Column(db.String(120), nullable=True)
    reason = db.Column(db.String(255), nullable=True)
    created_by_user_code = db.Column(db.String(80), nullable=True, index=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)

    product = db.relationship("Product", back_populates="stock_movements")

    def __repr__(self) -> str:
        return f"<StockMovement {self.movement_type} product_id={self.product_id}>"
