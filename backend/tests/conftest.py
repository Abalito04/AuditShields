import pytest

from app import create_app
from app.extensions import db
from app.models import User
from app.models.user import ROLE_ADMIN, ROLE_READONLY


@pytest.fixture()
def app(tmp_path):
    flask_app = create_app("app.config.TestingConfig")
    flask_app.config.update(
        WTF_CSRF_ENABLED=False,
        SERVER_NAME="localhost",
        UPLOAD_FOLDER=str(tmp_path / "imports"),
        EXPORT_FOLDER=str(tmp_path / "exports"),
    )
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def admin_user(app):
    return create_user("Admin Test", "admin@test.local", "admin123", ROLE_ADMIN)


@pytest.fixture()
def readonly_user(app):
    return create_user("Readonly Test", "readonly@test.local", "readonly123", ROLE_READONLY)


def create_user(name: str, email: str, password: str, role: str) -> User:
    user = User(name=name, email=email, role=role, is_active=True)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def login(client, email: str, password: str):
    return client.post(
        "/login",
        data={"email": email, "password": password},
        follow_redirects=True,
    )
