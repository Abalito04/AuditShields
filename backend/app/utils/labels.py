MODULE_LABELS = {
    "purchases": "Compras",
    "suppliers": "Proveedores",
    "inventory": "Inventario",
}

RISK_LEVEL_LABELS = {
    "low": "Bajo",
    "medium": "Medio",
    "high": "Alto",
    "critical": "Critico",
}

ALERT_STATUS_LABELS = {
    "open": "Abierta",
    "closed": "Cerrada",
    "dismissed": "Descartada",
}

CASE_STATUS_LABELS = {
    "new": "Nuevo",
    "in_review": "En revision",
    "requires_documentation": "Requiere documentacion",
    "observed": "Observado",
    "in_correction": "En correccion",
    "normalized": "Normalizado",
    "false_positive": "Falso positivo",
    "confirmed": "Confirmado",
    "escalated": "Escalado",
    "closed": "Cerrado",
}

CASE_ACTION_LABELS = {
    "case_created_from_alert": "Caso creado desde alerta",
    "status_changed": "Cambio de estado",
    "comment_added": "Comentario agregado",
    "assigned": "Responsable asignado",
}

ENTITY_TYPE_LABELS = {
    "supplier": "Proveedor",
    "purchase_order": "Orden de compra",
    "invoice": "Factura",
    "payment": "Pago",
    "product": "Producto",
    "inventory_snapshot": "Snapshot de inventario",
    "stock_movement": "Movimiento de stock",
}

EVIDENCE_FIELD_LABELS = {
    "adjustment_count": "Cantidad de ajustes",
    "amount": "Monto",
    "approval_limit": "Limite de aprobacion",
    "bank_account": "Cuenta bancaria",
    "calculated_stock": "Stock calculado",
    "created_by_user_code": "Operador",
    "created_date": "Fecha de alta",
    "difference_quantity": "Diferencia",
    "estimated_value": "Valor estimado",
    "expected_quantity": "Cantidad esperada",
    "invoice_id": "ID de factura",
    "invoice_ids": "IDs de facturas",
    "invoice_number": "Numero de factura",
    "last_movement_date": "Ultimo movimiento",
    "missing_fields": "Campos faltantes",
    "movement_date": "Fecha del movimiento",
    "movement_id": "ID de movimiento",
    "movement_ids": "IDs de movimientos",
    "movement_type": "Tipo de movimiento",
    "outside_hours": "Fuera de horario",
    "payment_date": "Fecha del pago",
    "payment_id": "ID de pago",
    "payment_ids": "IDs de pagos",
    "payment_number": "Numero de pago",
    "physical_quantity": "Cantidad fisica",
    "po_number": "Numero de orden",
    "product_id": "ID de producto",
    "purchase_order_id": "ID de orden",
    "purchase_order_ids": "IDs de ordenes",
    "quantity": "Cantidad",
    "reason": "Motivo",
    "reference": "Referencia",
    "sku": "SKU",
    "supplier_id": "ID de proveedor",
    "supplier_ids": "IDs de proveedores",
    "supplier_name": "Proveedor",
    "supplier_names": "Proveedores",
    "supplier_paid": "Pagado al proveedor",
    "threshold": "Umbral",
    "total_adjusted_quantity": "Cantidad ajustada total",
    "total_amount": "Monto total",
    "total_paid": "Total pagado",
    "weekend": "Fin de semana",
}


def label_for(mapping: dict[str, str], value: str | None) -> str:
    if not value:
        return "-"
    return mapping.get(value, value)
