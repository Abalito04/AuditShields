from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Alert, FraudRule
from app.services.case_service import create_case_for_alert
from app.services.inventory_rules import RULE_FUNCTIONS as INVENTORY_RULE_FUNCTIONS
from app.services.purchase_rules import RULE_FUNCTIONS as PURCHASE_RULE_FUNCTIONS
from app.services.rule_catalog import DEFAULT_RULES


RULE_FUNCTIONS = {
    **PURCHASE_RULE_FUNCTIONS,
    **INVENTORY_RULE_FUNCTIONS,
}


@dataclass
class FraudRunResult:
    rules_executed: int = 0
    alerts_created: int = 0
    duplicates_ignored: int = 0
    cases_created: int = 0
    errors: list[str] | None = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []


def run_fraud_audit() -> FraudRunResult:
    ensure_default_rules()
    result = FraudRunResult()
    active_rules = FraudRule.query.filter_by(is_active=True).order_by(FraudRule.code.asc()).all()

    for rule in active_rules:
        rule_function = RULE_FUNCTIONS.get(rule.code)
        if not rule_function:
            continue
        result.rules_executed += 1
        try:
            candidates = rule_function(rule)
        except Exception as exc:  # Defensive: one rule should not stop the full audit.
            result.errors.append(f"{rule.code}: {exc}")
            continue

        for candidate in candidates:
            _persist_candidate(rule, candidate, result)

    db.session.commit()
    return result


def ensure_default_rules() -> None:
    existing_rules = {
        rule.code: rule for rule in FraudRule.query.filter(FraudRule.code.in_([item["code"] for item in DEFAULT_RULES])).all()
    }
    for data in DEFAULT_RULES:
        rule = existing_rules.get(data["code"])
        if rule:
            rule.name = data["name"]
            rule.module = data["module"]
            rule.description = data["description"]
            rule.risk_level_default = data["risk_level_default"]
            if rule.config_json is None:
                rule.config_json = data["config_json"]
            continue
        db.session.add(
            FraudRule(
                code=data["code"],
                name=data["name"],
                module=data["module"],
                description=data["description"],
                risk_level_default=data["risk_level_default"],
                is_active=True,
                config_json=data["config_json"],
            )
        )
    db.session.flush()


def _persist_candidate(rule: FraudRule, candidate: dict, result: FraudRunResult) -> None:
    fingerprint = candidate["fingerprint"]
    if Alert.query.filter_by(fingerprint=fingerprint).first():
        result.duplicates_ignored += 1
        return

    try:
        with db.session.begin_nested():
            alert = Alert(
                rule_id=rule.id,
                module=candidate["module"],
                entity_type=candidate["entity_type"],
                entity_id=candidate.get("entity_id"),
                title=candidate["title"],
                description=candidate["description"],
                risk_score=int(candidate.get("risk_score", 0)),
                risk_level=candidate.get("risk_level") or rule.risk_level_default,
                amount_at_risk=_decimal_or_none(candidate.get("amount_at_risk")),
                evidence_json=candidate.get("evidence_json") or {},
                status="open",
                fingerprint=fingerprint,
            )
            db.session.add(alert)
            db.session.flush()
            create_case_for_alert(alert)
    except IntegrityError:
        result.duplicates_ignored += 1
        return

    result.alerts_created += 1
    result.cases_created += 1


def _decimal_or_none(value):
    if value in (None, ""):
        return None
    return Decimal(str(value))
