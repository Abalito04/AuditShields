from tests.conftest import login


def test_app_creates(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_dashboard_requires_login(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code in {302, 401}


def test_login_success(client, admin_user):
    response = login(client, "admin@test.local", "admin123")
    assert response.status_code == 200
    assert b"Dashboard" in response.data


def test_login_failure(client, admin_user):
    response = client.post(
        "/login",
        data={"email": "admin@test.local", "password": "bad"},
    )
    assert response.status_code == 401


def test_readonly_cannot_create_supplier(client, readonly_user):
    login(client, "readonly@test.local", "readonly123")
    response = client.post(
        "/suppliers/new",
        data={"supplier_code": "T-001", "name": "Proveedor Test"},
    )
    assert response.status_code == 403
