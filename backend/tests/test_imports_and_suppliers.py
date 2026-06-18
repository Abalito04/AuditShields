from io import BytesIO

from app.models import ImportLog, Supplier
from tests.conftest import login


def test_create_supplier(client, admin_user):
    login(client, "admin@test.local", "admin123")
    response = client.post(
        "/suppliers/new",
        data={
            "supplier_code": "SUP-TEST-001",
            "name": "Proveedor Test",
            "status": "active",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert Supplier.query.filter_by(supplier_code="SUP-TEST-001").first() is not None


def test_import_missing_columns_fails(client, admin_user):
    login(client, "admin@test.local", "admin123")
    csv_content = b"wrong_column\nvalue\n"
    response = client.post(
        "/imports/upload",
        data={
            "entity_type": "suppliers",
            "file": (BytesIO(csv_content), "bad_suppliers.csv"),
        },
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert response.status_code == 200
    import_log = ImportLog.query.order_by(ImportLog.id.desc()).first()
    assert import_log is not None
    assert import_log.status == "failed"
    assert import_log.imported_rows == 0
    assert import_log.rejected_rows == 1
