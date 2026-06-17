import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import create_app
from app.extensions import db
from app.models import User
from app.models.user import ROLE_ADMIN


ADMIN_EMAIL = "admin@auditshields.local"
ADMIN_PASSWORD = "admin123"


def seed_admin_user() -> None:
    user = User.query.filter_by(email=ADMIN_EMAIL).first()
    if user:
        user.name = "Admin AuditShields"
        user.role = ROLE_ADMIN
        user.is_active = True
        user.set_password(ADMIN_PASSWORD)
    else:
        user = User(
            name="Admin AuditShields",
            email=ADMIN_EMAIL,
            role=ROLE_ADMIN,
            is_active=True,
        )
        user.set_password(ADMIN_PASSWORD)
        db.session.add(user)

    db.session.commit()
    print(f"Admin user ready: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_admin_user()
