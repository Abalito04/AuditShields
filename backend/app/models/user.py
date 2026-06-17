from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.models.base import utc_now


ROLE_ADMIN = "admin"
ROLE_AUDITOR = "auditor"
ROLE_READONLY = "readonly"
VALID_ROLES = {ROLE_ADMIN, ROLE_AUDITOR, ROLE_READONLY}


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), nullable=False, default="readonly")
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )

    assigned_cases = db.relationship("Case", back_populates="assigned_to", lazy="dynamic")
    case_comments = db.relationship("CaseComment", back_populates="user", lazy="dynamic")
    case_history_entries = db.relationship("CaseHistory", back_populates="user", lazy="dynamic")
    import_logs = db.relationship("ImportLog", back_populates="created_by", lazy="dynamic")
    audit_logs = db.relationship("AuditLog", back_populates="user", lazy="dynamic")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def has_role(self, *roles: str) -> bool:
        return self.role in roles

    @property
    def is_admin(self) -> bool:
        return self.role == ROLE_ADMIN

    @property
    def is_readonly(self) -> bool:
        return self.role == ROLE_READONLY

    def __repr__(self) -> str:
        return f"<User {self.email}>"
