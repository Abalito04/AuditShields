from dataclasses import dataclass


@dataclass(frozen=True)
class EntitySchema:
    label: str
    sheet_name: str
    required_columns: list[str]
    optional_columns: list[str]
    example_row: dict[str, object]

    @property
    def columns(self) -> list[str]:
        return self.required_columns + self.optional_columns


ENTITY_SCHEMAS = {
    "suppliers": EntitySchema(
        label="Proveedores",
        sheet_name="proveedores",
        required_columns=["supplier_code", "name"],
        optional_columns=[
            "tax_id",
            "bank_account",
            "address",
            "phone",
            "email",
            "created_date",
            "status",
        ],
        example_row={
            "supplier_code": "PROV-001",
            "name": "Proveedor Demo SA",
            "tax_id": "30-00000000-1",
            "bank_account": "CBU0000000000000000000001",
            "address": "Av. Demo 123",
            "phone": "1122334455",
            "email": "contacto@proveedor.demo",
            "created_date": "2026-06-01",
            "status": "active",
        },
    ),
    "purchase_orders": EntitySchema(
        label="Ordenes de compra",
        sheet_name="ordenes_compra",
        required_columns=["po_number", "supplier_code", "total_amount"],
        optional_columns=[
            "requester_user_code",
            "approver_user_code",
            "order_date",
            "status",
        ],
        example_row={
            "po_number": "OC-001",
            "supplier_code": "PROV-001",
            "requester_user_code": "Ana Perez",
            "approver_user_code": "Luis Gomez",
            "order_date": "2026-06-05",
            "total_amount": 150000,
            "status": "approved",
        },
    ),
    "invoices": EntitySchema(
        label="Facturas",
        sheet_name="facturas",
        required_columns=["invoice_number", "supplier_code", "total_amount"],
        optional_columns=["po_number", "issue_date", "due_date", "status"],
        example_row={
            "invoice_number": "FAC-001",
            "supplier_code": "PROV-001",
            "po_number": "OC-001",
            "issue_date": "2026-06-06",
            "due_date": "2026-07-06",
            "total_amount": 150000,
            "status": "pending",
        },
    ),
    "payments": EntitySchema(
        label="Pagos",
        sheet_name="pagos",
        required_columns=["payment_number", "supplier_code", "amount"],
        optional_columns=[
            "invoice_number",
            "payment_date",
            "payment_method",
            "bank_account",
            "created_by_user_code",
        ],
        example_row={
            "payment_number": "PAGO-001",
            "supplier_code": "PROV-001",
            "invoice_number": "FAC-001",
            "payment_date": "2026-06-10 10:30",
            "amount": 150000,
            "payment_method": "transfer",
            "bank_account": "CBU0000000000000000000001",
            "created_by_user_code": "Ana Perez",
        },
    ),
    "products": EntitySchema(
        label="Productos",
        sheet_name="productos",
        required_columns=["sku", "name"],
        optional_columns=["category", "unit_cost", "is_active"],
        example_row={
            "sku": "SKU-001",
            "name": "Producto Demo",
            "category": "Insumos",
            "unit_cost": 2500,
            "is_active": True,
        },
    ),
    "inventory_snapshots": EntitySchema(
        label="Stock actual",
        sheet_name="stock_actual",
        required_columns=["sku", "snapshot_date", "expected_quantity", "physical_quantity"],
        optional_columns=[],
        example_row={
            "sku": "SKU-001",
            "snapshot_date": "2026-06-15",
            "expected_quantity": 100,
            "physical_quantity": 96,
        },
    ),
    "stock_movements": EntitySchema(
        label="Movimientos de stock",
        sheet_name="movimientos_stock",
        required_columns=["sku", "movement_type", "quantity", "movement_date"],
        optional_columns=["reference", "reason", "created_by_user_code"],
        example_row={
            "sku": "SKU-001",
            "movement_type": "OUT",
            "quantity": 4,
            "movement_date": "2026-06-16 18:20",
            "reference": "REM-001",
            "reason": "Venta",
            "created_by_user_code": "Ana Perez",
        },
    ),
    "operational_users": EntitySchema(
        label="Usuarios operativos",
        sheet_name="usuarios_operativos",
        required_columns=["full_name"],
        optional_columns=["role", "area", "external_code"],
        example_row={
            "full_name": "Ana Perez",
            "role": "Compras",
            "area": "Administracion",
            "external_code": "USR-001",
        },
    ),
}


def get_entity_schema(entity_type: str) -> EntitySchema:
    if entity_type not in ENTITY_SCHEMAS:
        raise ValueError("Tipo de entidad no soportado.")
    return ENTITY_SCHEMAS[entity_type]


def validate_columns(entity_type: str, columns: list[str]) -> list[str]:
    schema = get_entity_schema(entity_type)
    normalized_columns = set(columns)
    return [column for column in schema.required_columns if column not in normalized_columns]
