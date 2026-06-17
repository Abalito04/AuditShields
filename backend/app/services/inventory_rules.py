from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal

from app.models import FraudRule, InventorySnapshot, Product, StockMovement


def run_repeated_manual_adjustments(rule: FraudRule) -> list[dict]:
    window_days = int(_config(rule, "window_days", 15))
    min_adjustments = int(_config(rule, "min_adjustments", 3))
    cutoff = date.today() - timedelta(days=window_days)
    adjustments_by_product = defaultdict(list)

    for movement in StockMovement.query.filter_by(movement_type="ADJUSTMENT").all():
        if movement.movement_date.date() >= cutoff:
            adjustments_by_product[movement.product_id].append(movement)

    alerts = []
    for product_id, movements in adjustments_by_product.items():
        if len(movements) < min_adjustments:
            continue
        product = movements[0].product
        movement_ids = sorted(movement.id for movement in movements)
        total_adjusted = sum((movement.quantity for movement in movements), Decimal("0"))
        alerts.append(
            _candidate(
                rule,
                module="inventory",
                entity_type="product",
                entity_id=product_id,
                title=f"Ajustes manuales repetidos en {product.name}",
                description=(
                    f"El producto tiene {len(movements)} ajustes manuales en los ultimos "
                    f"{window_days} dias. Conviene revisar motivos y responsables."
                ),
                risk_score=62,
                amount_at_risk=_stock_value(product, abs(total_adjusted)),
                evidence_json={
                    "product_id": product_id,
                    "sku": product.sku,
                    "movement_ids": movement_ids,
                    "total_adjusted_quantity": _quantity(total_adjusted),
                },
                fingerprint=f"{rule.code}:product:{product_id}:movements:{'-'.join(map(str, movement_ids))}",
            )
        )
    return alerts


def run_negative_stock(rule: FraudRule) -> list[dict]:
    alerts = []
    for product in Product.query.filter_by(is_active=True).all():
        stock = _calculated_stock(product)
        if stock >= 0:
            continue
        alerts.append(
            _candidate(
                rule,
                module="inventory",
                entity_type="product",
                entity_id=product.id,
                title=f"Stock negativo en {product.name}",
                description=(
                    f"El stock calculado del producto queda en {_quantity(stock)}. "
                    "Esto puede indicar egresos sin respaldo, carga incompleta o conteo incorrecto."
                ),
                risk_score=82,
                amount_at_risk=_stock_value(product, abs(stock)),
                evidence_json={
                    "product_id": product.id,
                    "sku": product.sku,
                    "calculated_stock": _quantity(stock),
                    "unit_cost": _money(product.unit_cost),
                },
                fingerprint=f"{rule.code}:product:{product.id}",
            )
        )
    return alerts


def run_inventory_difference(rule: FraudRule) -> list[dict]:
    threshold = Decimal(str(_config(rule, "quantity_threshold", 20)))
    alerts = []
    for snapshot in InventorySnapshot.query.all():
        difference = Decimal(str(snapshot.difference_quantity))
        if abs(difference) <= threshold:
            continue
        product = snapshot.product
        alerts.append(
            _candidate(
                rule,
                module="inventory",
                entity_type="inventory_snapshot",
                entity_id=snapshot.id,
                title=f"Diferencia relevante de inventario en {product.name}",
                description=(
                    "La diferencia entre stock esperado y fisico supera el umbral configurado. "
                    "Debe revisarse conteo, movimientos pendientes o posibles mermas."
                ),
                risk_score=65,
                amount_at_risk=_stock_value(product, abs(difference)),
                evidence_json={
                    "snapshot_id": snapshot.id,
                    "product_id": product.id,
                    "sku": product.sku,
                    "expected_quantity": _quantity(snapshot.expected_quantity),
                    "physical_quantity": _quantity(snapshot.physical_quantity),
                    "difference_quantity": _quantity(difference),
                    "threshold": _quantity(threshold),
                },
                fingerprint=f"{rule.code}:snapshot:{snapshot.id}",
            )
        )
    return alerts


def run_movement_outside_business_hours(rule: FraudRule) -> list[dict]:
    start_hour = int(_config(rule, "start_hour", 8))
    end_hour = int(_config(rule, "end_hour", 19))
    alerts = []
    for movement in StockMovement.query.all():
        movement_date = movement.movement_date
        outside_hours = movement_date.hour < start_hour or movement_date.hour >= end_hour
        weekend = movement_date.weekday() >= 5
        if not outside_hours and not weekend:
            continue
        alerts.append(
            _candidate(
                rule,
                module="inventory",
                entity_type="stock_movement",
                entity_id=movement.id,
                title=f"Movimiento fuera de horario en {movement.product.name}",
                description=(
                    "El movimiento de stock fue registrado fuera del horario laboral o en dia no laboral. "
                    "Debe validarse si corresponde al proceso normal."
                ),
                risk_score=52,
                amount_at_risk=_stock_value(movement.product, abs(movement.quantity)),
                evidence_json={
                    "movement_id": movement.id,
                    "product_id": movement.product_id,
                    "sku": movement.product.sku,
                    "movement_type": movement.movement_type,
                    "quantity": _quantity(movement.quantity),
                    "movement_date": _datetime_text(movement.movement_date),
                    "outside_hours": outside_hours,
                    "weekend": weekend,
                },
                fingerprint=f"{rule.code}:movement:{movement.id}",
            )
        )
    return alerts


def run_excessive_shrinkage(rule: FraudRule) -> list[dict]:
    threshold = Decimal(str(_config(rule, "quantity_threshold", 50)))
    alerts = []
    for movement in StockMovement.query.all():
        shrinkage_quantity = _shrinkage_quantity(movement)
        if shrinkage_quantity <= threshold:
            continue
        alerts.append(
            _candidate(
                rule,
                module="inventory",
                entity_type="stock_movement",
                entity_id=movement.id,
                title=f"Merma o salida excesiva en {movement.product.name}",
                description=(
                    "El movimiento representa una salida o ajuste negativo superior al umbral. "
                    "Debe revisarse soporte documental y motivo operativo."
                ),
                risk_score=72,
                amount_at_risk=_stock_value(movement.product, shrinkage_quantity),
                evidence_json={
                    "movement_id": movement.id,
                    "product_id": movement.product_id,
                    "sku": movement.product.sku,
                    "movement_type": movement.movement_type,
                    "quantity": _quantity(movement.quantity),
                    "threshold": _quantity(threshold),
                    "reason": movement.reason,
                    "reference": movement.reference,
                },
                fingerprint=f"{rule.code}:movement:{movement.id}",
            )
        )
    return alerts


def run_unreconciled_transfer(rule: FraudRule) -> list[dict]:
    groups = defaultdict(list)
    for movement in StockMovement.query.filter_by(movement_type="TRANSFER").all():
        reference = (movement.reference or "").strip().lower()
        if reference:
            groups[reference].append(movement)
        else:
            groups[f"sin_referencia_{movement.id}"].append(movement)

    alerts = []
    for reference, movements in groups.items():
        if len(movements) >= 2:
            continue
        movement = movements[0]
        alerts.append(
            _candidate(
                rule,
                module="inventory",
                entity_type="stock_movement",
                entity_id=movement.id,
                title=f"Transferencia no conciliada en {movement.product.name}",
                description=(
                    "La transferencia no tiene contraparte con la misma referencia. "
                    "Debe verificarse si la salida y entrada fueron conciliadas."
                ),
                risk_score=58,
                amount_at_risk=_stock_value(movement.product, abs(movement.quantity)),
                evidence_json={
                    "movement_id": movement.id,
                    "reference": movement.reference,
                    "reference_key": reference,
                    "quantity": _quantity(movement.quantity),
                },
                fingerprint=f"{rule.code}:movement:{movement.id}",
            )
        )
    return alerts


def run_user_with_too_many_adjustments(rule: FraudRule) -> list[dict]:
    min_adjustments = int(_config(rule, "min_adjustments", 3))
    adjustments_by_user = defaultdict(list)
    for movement in StockMovement.query.filter_by(movement_type="ADJUSTMENT").all():
        user_code = (movement.created_by_user_code or "").strip()
        if user_code:
            adjustments_by_user[user_code].append(movement)

    alerts = []
    for user_code, movements in adjustments_by_user.items():
        if len(movements) < min_adjustments:
            continue
        movement_ids = sorted(movement.id for movement in movements)
        total_value = sum(
            (_stock_value(movement.product, abs(movement.quantity)) for movement in movements),
            Decimal("0"),
        )
        alerts.append(
            _candidate(
                rule,
                module="inventory",
                entity_type="stock_movement",
                entity_id=movement_ids[0],
                title=f"Operador con demasiados ajustes: {user_code}",
                description=(
                    f"El operador registra {len(movements)} ajustes de stock. "
                    "Debe revisarse si existe patron recurrente o falta de documentacion."
                ),
                risk_score=60,
                amount_at_risk=total_value,
                evidence_json={
                    "created_by_user_code": user_code,
                    "movement_ids": movement_ids,
                    "adjustment_count": len(movements),
                    "estimated_value": _money(total_value),
                },
                fingerprint=f"{rule.code}:user:{user_code.lower()}",
            )
        )
    return alerts


def run_critical_product_without_movement(rule: FraudRule) -> list[dict]:
    days_without_movement = int(_config(rule, "days_without_movement", 30))
    cutoff = date.today() - timedelta(days=days_without_movement)
    alerts = []
    for product in Product.query.filter_by(is_active=True).all():
        last_movement = (
            product.stock_movements.order_by(StockMovement.movement_date.desc()).first()
        )
        if last_movement and last_movement.movement_date.date() >= cutoff:
            continue
        alerts.append(
            _candidate(
                rule,
                module="inventory",
                entity_type="product",
                entity_id=product.id,
                title=f"Producto activo sin movimientos recientes: {product.name}",
                description=(
                    f"El producto activo no registra movimientos en los ultimos {days_without_movement} dias. "
                    "Puede requerir revision de demanda, obsolescencia o stock inmovilizado."
                ),
                risk_score=35,
                amount_at_risk=None,
                evidence_json={
                    "product_id": product.id,
                    "sku": product.sku,
                    "last_movement_date": _datetime_text(last_movement.movement_date)
                    if last_movement
                    else None,
                },
                fingerprint=f"{rule.code}:product:{product.id}",
            )
        )
    return alerts


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


def _candidate(
    rule: FraudRule,
    module: str,
    entity_type: str,
    entity_id: int | None,
    title: str,
    description: str,
    risk_score: int,
    amount_at_risk,
    evidence_json: dict,
    fingerprint: str,
) -> dict:
    return {
        "rule_code": rule.code,
        "module": module,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "title": title,
        "description": description,
        "risk_score": risk_score,
        "risk_level": _risk_level(risk_score),
        "amount_at_risk": _money(amount_at_risk) if amount_at_risk is not None else None,
        "evidence_json": evidence_json,
        "fingerprint": fingerprint,
    }


def _calculated_stock(product: Product) -> Decimal:
    stock = Decimal("0")
    for movement in product.stock_movements:
        quantity = Decimal(str(movement.quantity))
        if movement.movement_type == "IN":
            stock += abs(quantity)
        elif movement.movement_type == "OUT":
            stock -= abs(quantity)
        else:
            stock += quantity
    return stock


def _shrinkage_quantity(movement: StockMovement) -> Decimal:
    quantity = Decimal(str(movement.quantity))
    if movement.movement_type == "OUT":
        return abs(quantity)
    if movement.movement_type == "ADJUSTMENT" and quantity < 0:
        return abs(quantity)
    return Decimal("0")


def _stock_value(product: Product, quantity) -> Decimal:
    return Decimal(str(product.unit_cost)) * Decimal(str(quantity))


def _config(rule: FraudRule, key: str, default):
    return (rule.config_json or {}).get(key, default)


def _risk_level(score: int) -> str:
    if score >= 80:
        return "critical"
    if score >= 60:
        return "high"
    if score >= 30:
        return "medium"
    return "low"


def _money(value) -> str:
    return str(Decimal(str(value)).quantize(Decimal("0.01")))


def _quantity(value) -> str:
    return str(Decimal(str(value)).quantize(Decimal("0.001")))


def _datetime_text(value) -> str | None:
    return value.isoformat() if value else None
