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


def label_for(mapping: dict[str, str], value: str | None) -> str:
    if not value:
        return "-"
    return mapping.get(value, value)
