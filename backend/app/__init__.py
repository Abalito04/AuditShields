from importlib import import_module
from os import getenv

from flask import Flask, abort, render_template, request

from app.config import DevelopmentConfig, ProductionConfig
from app.extensions import db, login_manager, migrate
from app.models.user import ROLE_READONLY
from app.routes.alerts import alerts_bp
from app.routes.audit import audit_bp
from app.routes.auth import auth_bp
from app.routes.cases import cases_bp
from app.routes.dashboard import dashboard_bp
from app.routes.demo import demo_bp
from app.routes.imports import imports_bp
from app.routes.inventory import inventory_bp
from app.routes.purchases import purchases_bp
from app.routes.reports import reports_bp
from app.routes.suppliers import suppliers_bp
from app.routes.users import users_bp
from app.utils.formatting import money_format


def create_app(config_object: str | None = None) -> Flask:
    app = Flask(__name__)

    if config_object:
        app.config.from_object(config_object)
    elif getenv("FLASK_ENV") == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    register_extensions(app)
    register_template_filters(app)
    register_blueprints(app)
    register_security_hooks(app)
    register_error_handlers(app)

    return app


def register_extensions(app: Flask) -> None:
    db.init_app(app)
    import_module("app.models")

    migrate.init_app(app, db)
    login_manager.init_app(app)


def register_template_filters(app: Flask) -> None:
    app.jinja_env.filters["money_format"] = money_format


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(auth_bp)
    app.register_blueprint(audit_bp)
    app.register_blueprint(demo_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(imports_bp)
    app.register_blueprint(suppliers_bp)
    app.register_blueprint(purchases_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(alerts_bp)
    app.register_blueprint(cases_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(users_bp)


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


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(413)
    def file_too_large(error):
        return render_template("errors/413.html"), 413

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        app.logger.exception("Unhandled application error: %s", error)
        return render_template("errors/500.html"), 500
