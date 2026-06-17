from app.models import FraudRule


def run_repeated_manual_adjustments(rule: FraudRule) -> list[dict]:
    return []


def run_negative_stock(rule: FraudRule) -> list[dict]:
    return []


def run_inventory_difference(rule: FraudRule) -> list[dict]:
    return []


def run_movement_outside_business_hours(rule: FraudRule) -> list[dict]:
    return []


def run_excessive_shrinkage(rule: FraudRule) -> list[dict]:
    return []


def run_unreconciled_transfer(rule: FraudRule) -> list[dict]:
    return []


def run_user_with_too_many_adjustments(rule: FraudRule) -> list[dict]:
    return []


def run_critical_product_without_movement(rule: FraudRule) -> list[dict]:
    return []


RULE_FUNCTIONS = {
    "S001": run_repeated_manual_adjustments,
    "S002": run_negative_stock,
    "S003": run_inventory_difference,
    "S004": run_movement_outside_business_hours,
    "S005": run_excessive_shrinkage,
    "S006": run_unreconciled_transfer,
    "S007": run_user_with_too_many_adjustments,
    "S008": run_critical_product_without_movement,
}
