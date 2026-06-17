from flask import flash
from sqlalchemy.exc import IntegrityError

from app.extensions import db


def commit_or_flash(success_message: str, error_message: str) -> bool:
    try:
        db.session.commit()
        flash(success_message, "success")
        return True
    except IntegrityError:
        db.session.rollback()
        flash(error_message, "danger")
        return False
    except ValueError as exc:
        db.session.rollback()
        flash(str(exc), "danger")
        return False
