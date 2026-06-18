import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import create_app
from app.extensions import db
from app.models import (
    Alert,
    AuditLog,
    Case,
    CaseComment,
    CaseHistory,
    FraudRule,
    ImportLog,
    InventorySnapshot,
    Invoice,
    Payment,
    Product,
    PurchaseOrder,
    StockMovement,
    Supplier,
    User,
)
from seed.seed_users import seed_admin_user


def reset_database() -> None:
    db.session.query(CaseComment).delete(synchronize_session=False)
    db.session.query(CaseHistory).delete(synchronize_session=False)
    db.session.query(Case).delete(synchronize_session=False)
    db.session.query(Alert).delete(synchronize_session=False)
    db.session.query(FraudRule).delete(synchronize_session=False)

    db.session.query(ImportLog).delete(synchronize_session=False)
    db.session.query(AuditLog).delete(synchronize_session=False)

    db.session.query(Payment).delete(synchronize_session=False)
    db.session.query(Invoice).delete(synchronize_session=False)
    db.session.query(PurchaseOrder).delete(synchronize_session=False)
    db.session.query(Supplier).delete(synchronize_session=False)

    db.session.query(StockMovement).delete(synchronize_session=False)
    db.session.query(InventorySnapshot).delete(synchronize_session=False)
    db.session.query(Product).delete(synchronize_session=False)

    db.session.query(User).delete(synchronize_session=False)
    db.session.commit()

    seed_admin_user()
    print("Database reset complete. Only the initial admin user was recreated.")


if __name__ == "__main__":
    if "--yes" not in sys.argv:
        print("This deletes all operational data, alerts, cases, imports, logs and users.")
        print("Run again with: python seed/reset_database.py --yes")
        raise SystemExit(1)

    app = create_app()
    with app.app_context():
        reset_database()
