from app.models import FraudRule


def run_payment_duplicate_exact(rule: FraudRule) -> list[dict]:
    return []


def run_invoice_duplicate(rule: FraudRule) -> list[dict]:
    return []


def run_shared_bank_account(rule: FraudRule) -> list[dict]:
    return []


def run_new_supplier_high_payments(rule: FraudRule) -> list[dict]:
    return []


def run_without_purchase_order(rule: FraudRule) -> list[dict]:
    return []


def run_split_purchase(rule: FraudRule) -> list[dict]:
    return []


def run_approver_same_as_requester(rule: FraudRule) -> list[dict]:
    return []


def run_supplier_concentration(rule: FraudRule) -> list[dict]:
    return []


def run_payment_outside_business_hours(rule: FraudRule) -> list[dict]:
    return []


def run_incomplete_supplier_data(rule: FraudRule) -> list[dict]:
    return []


RULE_FUNCTIONS = {
    "R001": run_payment_duplicate_exact,
    "R002": run_invoice_duplicate,
    "R003": run_shared_bank_account,
    "R004": run_new_supplier_high_payments,
    "R005": run_without_purchase_order,
    "R006": run_split_purchase,
    "R007": run_approver_same_as_requester,
    "R008": run_supplier_concentration,
    "R009": run_payment_outside_business_hours,
    "R010": run_incomplete_supplier_data,
}
