from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal

from app.models import FraudRule, Invoice, Payment, PurchaseOrder, Supplier


def run_payment_duplicate_exact(rule: FraudRule) -> list[dict]:
    near_days = int(_config(rule, "near_days", 2))
    groups = defaultdict(list)
    for payment in Payment.query.all():
        invoice_key = payment.invoice.invoice_number if payment.invoice else "sin_factura"
        groups[(payment.supplier_id, invoice_key, _money(payment.amount))].append(payment)

    alerts = []
    for payments in groups.values():
        if len(payments) < 2:
            continue
        dated_payments = [payment for payment in payments if payment.payment_date]
        if len(dated_payments) >= 2:
            dates = [payment.payment_date.date() for payment in dated_payments]
            if (max(dates) - min(dates)).days > near_days:
                continue
        payment_ids = sorted(payment.id for payment in payments)
        supplier = payments[0].supplier
        amount = sum((payment.amount for payment in payments), Decimal("0"))
        alerts.append(
            _candidate(
                rule,
                module="purchases",
                entity_type="payment",
                entity_id=payment_ids[0],
                title=f"Posible pago duplicado a {supplier.name}",
                description=(
                    f"Se detectaron {len(payments)} pagos del mismo proveedor, "
                    "misma factura o referencia y mismo monto en fechas iguales o cercanas."
                ),
                risk_score=85,
                amount_at_risk=amount,
                evidence_json={
                    "payment_ids": payment_ids,
                    "supplier_id": supplier.id,
                    "supplier_name": supplier.name,
                    "amount": _money(payments[0].amount),
                },
                fingerprint=f"{rule.code}:payments:{'-'.join(map(str, payment_ids))}",
            )
        )
    return alerts


def run_invoice_duplicate(rule: FraudRule) -> list[dict]:
    groups = defaultdict(list)
    for invoice in Invoice.query.all():
        key = (
            invoice.supplier_id,
            (invoice.invoice_number or "").strip().lower(),
            _money(invoice.total_amount),
        )
        groups[key].append(invoice)

    alerts = []
    for invoices in groups.values():
        if len(invoices) < 2:
            continue
        invoice_ids = sorted(invoice.id for invoice in invoices)
        supplier = invoices[0].supplier
        alerts.append(
            _candidate(
                rule,
                module="purchases",
                entity_type="invoice",
                entity_id=invoice_ids[0],
                title=f"Factura duplicada de {supplier.name}",
                description=(
                    f"Existen {len(invoices)} facturas con el mismo proveedor, "
                    "numero e importe. Puede tratarse de una duplicacion de carga o pago."
                ),
                risk_score=80,
                amount_at_risk=invoices[0].total_amount,
                evidence_json={
                    "invoice_ids": invoice_ids,
                    "supplier_id": supplier.id,
                    "supplier_name": supplier.name,
                    "invoice_number": invoices[0].invoice_number,
                    "amount": _money(invoices[0].total_amount),
                },
                fingerprint=f"{rule.code}:invoices:{'-'.join(map(str, invoice_ids))}",
            )
        )
    return alerts


def run_shared_bank_account(rule: FraudRule) -> list[dict]:
    groups = defaultdict(list)
    for supplier in Supplier.query.filter(Supplier.bank_account.isnot(None)).all():
        bank_account = supplier.bank_account.strip().lower() if supplier.bank_account else ""
        if bank_account:
            groups[bank_account].append(supplier)

    alerts = []
    for suppliers in groups.values():
        if len(suppliers) < 2:
            continue
        supplier_ids = sorted(supplier.id for supplier in suppliers)
        alerts.append(
            _candidate(
                rule,
                module="suppliers",
                entity_type="supplier",
                entity_id=supplier_ids[0],
                title="Proveedores comparten cuenta bancaria",
                description=(
                    "Se detectaron proveedores distintos con la misma cuenta bancaria. "
                    "Esto puede indicar duplicacion de proveedor o desvio de pagos."
                ),
                risk_score=65,
                amount_at_risk=None,
                evidence_json={
                    "supplier_ids": supplier_ids,
                    "supplier_names": [supplier.name for supplier in suppliers],
                    "bank_account": suppliers[0].bank_account,
                },
                fingerprint=f"{rule.code}:bank:{suppliers[0].bank_account.lower()}",
            )
        )
    return alerts


def run_new_supplier_high_payments(rule: FraudRule) -> list[dict]:
    days = int(_config(rule, "days", 30))
    threshold = Decimal(str(_config(rule, "amount_threshold", 1000000)))
    cutoff = date.today() - timedelta(days=days)
    alerts = []

    for supplier in Supplier.query.all():
        if not supplier.created_date or supplier.created_date < cutoff:
            continue
        total_paid = sum((payment.amount for payment in supplier.payments), Decimal("0"))
        if total_paid <= threshold:
            continue
        alerts.append(
            _candidate(
                rule,
                module="purchases",
                entity_type="supplier",
                entity_id=supplier.id,
                title=f"Proveedor nuevo con pagos altos: {supplier.name}",
                description=(
                    f"El proveedor fue creado hace menos de {days} dias y acumula pagos "
                    f"por {_money(total_paid)}, por encima del umbral configurado."
                ),
                risk_score=75,
                amount_at_risk=total_paid,
                evidence_json={
                    "supplier_id": supplier.id,
                    "supplier_name": supplier.name,
                    "created_date": _date_text(supplier.created_date),
                    "total_paid": _money(total_paid),
                    "threshold": _money(threshold),
                },
                fingerprint=f"{rule.code}:supplier:{supplier.id}",
            )
        )
    return alerts


def run_without_purchase_order(rule: FraudRule) -> list[dict]:
    alerts = []
    for invoice in Invoice.query.filter(Invoice.purchase_order_id.is_(None)).all():
        alerts.append(
            _candidate(
                rule,
                module="purchases",
                entity_type="invoice",
                entity_id=invoice.id,
                title=f"Factura sin orden de compra: {invoice.invoice_number}",
                description=(
                    "La factura no tiene orden de compra asociada. Debe revisarse si "
                    "existe aprobacion o documentacion respaldatoria."
                ),
                risk_score=55,
                amount_at_risk=invoice.total_amount,
                evidence_json={
                    "invoice_id": invoice.id,
                    "invoice_number": invoice.invoice_number,
                    "supplier_id": invoice.supplier_id,
                    "amount": _money(invoice.total_amount),
                },
                fingerprint=f"{rule.code}:invoice:{invoice.id}",
            )
        )

    for payment in Payment.query.all():
        if payment.invoice_id and payment.invoice and payment.invoice.purchase_order_id:
            continue
        reason = "sin factura asociada" if not payment.invoice_id else "factura sin orden de compra"
        alerts.append(
            _candidate(
                rule,
                module="purchases",
                entity_type="payment",
                entity_id=payment.id,
                title=f"Pago {reason}: {payment.payment_number}",
                description=(
                    f"El pago esta {reason}. Debe revisarse si corresponde pagar "
                    "sin trazabilidad completa de compra."
                ),
                risk_score=60,
                amount_at_risk=payment.amount,
                evidence_json={
                    "payment_id": payment.id,
                    "payment_number": payment.payment_number,
                    "supplier_id": payment.supplier_id,
                    "invoice_id": payment.invoice_id,
                    "amount": _money(payment.amount),
                    "reason": reason,
                },
                fingerprint=f"{rule.code}:payment:{payment.id}",
            )
        )
    return alerts


def run_split_purchase(rule: FraudRule) -> list[dict]:
    approval_limit = Decimal(str(_config(rule, "approval_limit", 500000)))
    lower_ratio = Decimal(str(_config(rule, "lower_ratio", 0.9)))
    window_days = int(_config(rule, "window_days", 7))
    lower_limit = approval_limit * lower_ratio
    alerts = []

    for supplier in Supplier.query.all():
        orders = [
            order
            for order in supplier.purchase_orders
            if order.order_date and lower_limit <= order.total_amount < approval_limit
        ]
        orders.sort(key=lambda order: order.order_date)
        for index, order in enumerate(orders):
            window_end = order.order_date + timedelta(days=window_days)
            window = [candidate for candidate in orders[index:] if candidate.order_date <= window_end]
            if len(window) < 2:
                continue
            order_ids = sorted(item.id for item in window)
            total_amount = sum((item.total_amount for item in window), Decimal("0"))
            alerts.append(
                _candidate(
                    rule,
                    module="purchases",
                    entity_type="purchase_order",
                    entity_id=order_ids[0],
                    title=f"Posible compra fraccionada en {supplier.name}",
                    description=(
                        f"Se detectaron {len(window)} ordenes del mismo proveedor, "
                        f"dentro de {window_days} dias, con montos justo debajo del limite de aprobacion."
                    ),
                    risk_score=78,
                    amount_at_risk=total_amount,
                    evidence_json={
                        "supplier_id": supplier.id,
                        "supplier_name": supplier.name,
                        "purchase_order_ids": order_ids,
                        "approval_limit": _money(approval_limit),
                        "total_amount": _money(total_amount),
                    },
                    fingerprint=f"{rule.code}:supplier:{supplier.id}:orders:{'-'.join(map(str, order_ids))}",
                )
            )
            break
    return alerts


def run_approver_same_as_requester(rule: FraudRule) -> list[dict]:
    alerts = []
    for order in PurchaseOrder.query.all():
        requester = (order.requester_user_code or "").strip().lower()
        approver = (order.approver_user_code or "").strip().lower()
        if not requester or requester != approver:
            continue
        alerts.append(
            _candidate(
                rule,
                module="purchases",
                entity_type="purchase_order",
                entity_id=order.id,
                title=f"Aprobador igual al solicitante en {order.po_number}",
                description=(
                    "La misma persona figura como solicitante y aprobador de la orden. "
                    "Esto debilita la separacion de funciones."
                ),
                risk_score=62,
                amount_at_risk=order.total_amount,
                evidence_json={
                    "purchase_order_id": order.id,
                    "po_number": order.po_number,
                    "person": order.requester_user_code,
                    "amount": _money(order.total_amount),
                },
                fingerprint=f"{rule.code}:purchase_order:{order.id}",
            )
        )
    return alerts


def run_supplier_concentration(rule: FraudRule) -> list[dict]:
    threshold = Decimal(str(_config(rule, "share_threshold", 0.5)))
    payments = Payment.query.all()
    total_paid = sum((payment.amount for payment in payments), Decimal("0"))
    if total_paid <= 0:
        return []

    totals_by_supplier = defaultdict(Decimal)
    for payment in payments:
        totals_by_supplier[payment.supplier_id] += payment.amount

    alerts = []
    for supplier_id, amount in totals_by_supplier.items():
        share = amount / total_paid
        if share < threshold:
            continue
        supplier = Supplier.query.get(supplier_id)
        alerts.append(
            _candidate(
                rule,
                module="purchases",
                entity_type="supplier",
                entity_id=supplier_id,
                title=f"Concentracion alta de pagos en {supplier.name}",
                description=(
                    f"El proveedor concentra {float(share * 100):.1f}% del total pagado. "
                    "Conviene revisar dependencia, aprobaciones y condiciones comerciales."
                ),
                risk_score=58,
                amount_at_risk=amount,
                evidence_json={
                    "supplier_id": supplier_id,
                    "supplier_name": supplier.name,
                    "supplier_paid": _money(amount),
                    "total_paid": _money(total_paid),
                    "share": float(share),
                },
                fingerprint=f"{rule.code}:supplier:{supplier_id}",
            )
        )
    return alerts


def run_payment_outside_business_hours(rule: FraudRule) -> list[dict]:
    start_hour = int(_config(rule, "start_hour", 8))
    end_hour = int(_config(rule, "end_hour", 19))
    alerts = []
    for payment in Payment.query.filter(Payment.payment_date.isnot(None)).all():
        payment_date = payment.payment_date
        outside_hours = payment_date.hour < start_hour or payment_date.hour >= end_hour
        weekend = payment_date.weekday() >= 5
        if not outside_hours and not weekend:
            continue
        alerts.append(
            _candidate(
                rule,
                module="purchases",
                entity_type="payment",
                entity_id=payment.id,
                title=f"Pago fuera de horario: {payment.payment_number}",
                description=(
                    "El pago fue registrado fuera del horario laboral o en dia no laboral. "
                    "Debe validarse si corresponde al proceso normal."
                ),
                risk_score=50,
                amount_at_risk=payment.amount,
                evidence_json={
                    "payment_id": payment.id,
                    "payment_number": payment.payment_number,
                    "payment_date": _datetime_text(payment.payment_date),
                    "amount": _money(payment.amount),
                    "outside_hours": outside_hours,
                    "weekend": weekend,
                },
                fingerprint=f"{rule.code}:payment:{payment.id}",
            )
        )
    return alerts


def run_incomplete_supplier_data(rule: FraudRule) -> list[dict]:
    critical_fields = ["tax_id", "bank_account", "email", "address"]
    alerts = []
    for supplier in Supplier.query.all():
        missing = [field for field in critical_fields if not getattr(supplier, field)]
        if not missing:
            continue
        score = min(70, 25 + len(missing) * 10)
        alerts.append(
            _candidate(
                rule,
                module="suppliers",
                entity_type="supplier",
                entity_id=supplier.id,
                title=f"Proveedor con datos incompletos: {supplier.name}",
                description=(
                    "El proveedor tiene campos criticos incompletos. "
                    "Esto dificulta controles fiscales, bancarios y de contacto."
                ),
                risk_score=score,
                amount_at_risk=None,
                evidence_json={
                    "supplier_id": supplier.id,
                    "supplier_name": supplier.name,
                    "missing_fields": missing,
                },
                fingerprint=f"{rule.code}:supplier:{supplier.id}",
            )
        )
    return alerts


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


def _date_text(value) -> str | None:
    return value.isoformat() if value else None


def _datetime_text(value) -> str | None:
    return value.isoformat() if value else None
