from functools import wraps

from flask import abort, request
from flask_login import current_user

from app.models.user import ROLE_READONLY


def roles_required(*roles: str):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.role not in roles:
                abort(403)
            return view_func(*args, **kwargs)

        return wrapped_view

    return decorator


def readonly_blocked_for_writes(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if (
            current_user.is_authenticated
            and current_user.role == ROLE_READONLY
            and request.method in {"POST", "PUT", "PATCH", "DELETE"}
        ):
            abort(403)
        return view_func(*args, **kwargs)

    return wrapped_view
