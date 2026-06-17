from decimal import Decimal, InvalidOperation


def money_format(value) -> str:
    if value in (None, ""):
        return "-"
    try:
        amount = Decimal(str(value)).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        return str(value)

    formatted = f"{amount:,.2f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")
