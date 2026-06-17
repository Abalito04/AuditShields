from datetime import datetime
from decimal import Decimal, InvalidOperation


def parse_optional_date(value: str | None):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def parse_optional_datetime(value: str | None):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%dT%H:%M")


def parse_decimal(value: str | None, default: str = "0") -> Decimal:
    raw_value = value if value not in (None, "") else default
    try:
        return Decimal(str(raw_value))
    except InvalidOperation as exc:
        raise ValueError("El valor numerico no es valido.") from exc


def parse_optional_int(value: str | None):
    if not value:
        return None
    return int(value)


def parse_bool(value: str | None) -> bool:
    return value in {"1", "true", "on", "yes"}
