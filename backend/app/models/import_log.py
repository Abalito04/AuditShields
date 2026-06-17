from app.extensions import db
from app.models.base import utc_now


class ImportLog(db.Model):
    __tablename__ = "imports"

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(20), nullable=False)
    entity_type = db.Column(db.String(80), nullable=False, index=True)
    status = db.Column(db.String(40), nullable=False, default="pending", index=True)
    total_rows = db.Column(db.Integer, nullable=False, default=0)
    imported_rows = db.Column(db.Integer, nullable=False, default=0)
    rejected_rows = db.Column(db.Integer, nullable=False, default=0)
    warnings_count = db.Column(db.Integer, nullable=False, default=0)
    errors_json = db.Column(db.JSON, nullable=True)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)

    created_by = db.relationship("User", back_populates="import_logs")

    def __repr__(self) -> str:
        return f"<ImportLog {self.file_name}>"
