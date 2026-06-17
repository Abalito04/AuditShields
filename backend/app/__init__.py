from flask import Flask, abort, request
from importlib import import_module

from app.config import DevelopmentConfig
from app.extensions import db, login_manager, migrate
from app.models.user import ROLE_READONLY
from app.routes.auth import auth_bp
from app.routes.dashboard import dashboard_bp


def create_app(config_object: str | None = None) -> Flask:
    app = Flask(__name__)

    if config_object:
        app.config.from_object(config_object)
    else:
        app.config.from_object(DevelopmentConfig)

    register_extensions(app)
    register_blueprints(app)
    register_security_hooks(app)

    return app


def register_extensions(app: Flask) -> None:
    db.init_app(app)
    import_module("app.models")

    migrate.init_app(app, db)
    login_manager.init_app(app)


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)


def register_security_hooks(app: Flask) -> None:
    @app.before_request
    def block_readonly_write_methods():
        from flask_login import current_user

        if request.endpoint in {"auth.login", "auth.logout"}:
            return None
        if (
            current_user.is_authenticated
            and current_user.role == ROLE_READONLY
            and request.method in {"POST", "PUT", "PATCH", "DELETE"}
        ):
            abort(403)
        return None
