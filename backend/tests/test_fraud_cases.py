from datetime import date, datetime
from decimal import Decimal

from app.extensions import db
from app.models import Alert, Case, CaseHistory, Invoice, Payment, Supplier
from app.services.fraud_engine import run_fraud_audit
from tests.conftest import login


def test_duplicate_payment_rule_creates_alert_and_case(app, admin_user):
    supplier = Supplier(
        supplier_code="SUP-DUP-001",
        name="Proveedor Duplicado",
        tax_id="30-99999999-9",
        bank_account="CBU-TEST",
        address="Calle Test 1",
        email="proveedor@test.local",
        created_date=date.today(),
        status="active",
    )
    db.session.add(supplier)
    db.session.flush()

    invoice = Invoice(
        invoice_number="FAC-DUP-001",
        supplier_id=supplier.id,
        issue_date=date.today(),
        total_amount=Decimal("1000.00"),
        status="pending",
    )
    db.session.add(invoice)
    db.session.flush()

    db.session.add_all(
        [
            Payment(
                payment_number="PAY-DUP-001",
                supplier_id=supplier.id,
                invoice_id=invoice.id,
                payment_date=datetime(2026, 6, 17, 10, 0),
                amount=Decimal("1000.00"),
                payment_method="transfer",
            ),
            Payment(
                payment_number="PAY-DUP-002",
                supplier_id=supplier.id,
                invoice_id=invoice.id,
                payment_date=datetime(2026, 6, 17, 10, 30),
                amount=Decimal("1000.00"),
                payment_method="transfer",
            ),
        ]
    )
    db.session.commit()

    result = run_fraud_audit()

    assert result.alerts_created >= 1
    duplicate_alert = Alert.query.filter(Alert.fingerprint.like("R001:%")).first()
    assert duplicate_alert is not None
    assert duplicate_alert.case is not None


def test_case_status_change_creates_history(client, admin_user):
    supplier = Supplier(supplier_code="SUP-CASE-001", name="Proveedor Caso", status="active")
    db.session.add(supplier)
    db.session.commit()
    run_fraud_audit()

    audit_case = Case.query.first()
    assert audit_case is not None

    login(client, "admin@test.local", "admin123")
    response = client.post(
        f"/cases/{audit_case.id}/status",
        data={"status": "in_review", "resolution_summary": "Revision inicial"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert Case.query.get(audit_case.id).status == "in_review"
    assert (
        CaseHistory.query.filter_by(case_id=audit_case.id, action="status_changed").first()
        is not None
    )
