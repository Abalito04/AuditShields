from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import (
    ImportLog,
    InventorySnapshot,
    Invoice,
    Payment,
    Product,
    PurchaseOrder,
    StockMovement,
    Supplier,
)
from app.services.audit_log_service import record_audit_log
from app.services.validation_service import get_entity_schema, validate_columns
from app.utils.parsing import parse_bool, parse_decimal


ALLOWED_EXTENSIONS = {".xlsx", ".csv"}
MOVEMENT_TYPES = {"IN", "OUT", "ADJUSTMENT", "TRANSFER"}


@dataclass
class ImportResult:
    log: ImportLog
    errors: list[dict]


def import_file(entity_type: str, file_path: str | Path, original_filename: str) -> ImportResult:
    schema = get_entity_schema(entity_type)
    path = Path(file_path)
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError("Solo se permiten archivos .xlsx o .csv.")

    dataframe = _read_dataframe(path)
    dataframe = dataframe.dropna(how="all")
    dataframe.columns = [str(column).strip() for column in dataframe.columns]

    missing_columns = validate_columns(entity_type, list(dataframe.columns))
    if missing_columns:
        errors = [{"row": None, "errors": [f"Faltan columnas: {', '.join(missing_columns)}"]}]
        log = _create_import_log(
            original_filename,
            path.suffix.lower().lstrip("."),
            entity_type,
            "failed",
            int(len(dataframe.index)),
            0,
            int(len(dataframe.index)),
            errors,
        )
        db.session.commit()
        return ImportResult(log=log, errors=errors)

    imported_rows = 0
    errors: list[dict] = []
    seen_keys: set[str] = set()

    for index, row in dataframe.iterrows():
        row_number = int(index) + 2
        data = _clean_row(row.to_dict())
        row_errors = _validate_required_values(schema.required_columns, data)
        unique_key = _unique_key(entity_type, data)
        if unique_key and unique_key in seen_keys:
            row_errors.append("Registro duplicado dentro del archivo.")
        if row_errors:
            errors.append({"row": row_number, "errors": row_errors})
            continue

        try:
            with db.session.begin_nested():
                model = _build_model(entity_type, data)
                db.session.add(model)
                db.session.flush()
            if unique_key:
                seen_keys.add(unique_key)
            imported_rows += 1
        except (ValueError, IntegrityError) as exc:
            errors.append({"row": row_number, "errors": [_message_from_exception(exc)]})

    status = "completed" if not errors else "completed_with_errors"
    log = _create_import_log(
        original_filename,
        path.suffix.lower().lstrip("."),
        entity_type,
        status,
        int(len(dataframe.index)),
        imported_rows,
        len(errors),
        errors,
    )
    record_audit_log(
        "import",
        "import_log",
        None,
        new_value={
            "entity_type": entity_type,
            "file_name": original_filename,
            "imported_rows": imported_rows,
            "rejected_rows": len(errors),
        },
    )
    db.session.commit()
    return ImportResult(log=log, errors=errors)


def _read_dataframe(path: Path):
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    return pd.read_excel(path)


def _clean_row(row: dict) -> dict:
    clean = {}
    for key, value in row.items():
        if pd.isna(value):
            clean[str(key).strip()] = None
        elif isinstance(value, str):
            clean[str(key).strip()] = value.strip() or None
        else:
            clean[str(key).strip()] = value
    return clean


def _validate_required_values(required_columns: list[str], data: dict) -> list[str]:
    return [f"{column} es obligatorio." for column in required_columns if data.get(column) in (None, "")]


def _unique_key(entity_type: str, data: dict) -> str | None:
    keys = {
        "suppliers": data.get("supplier_code"),
        "purchase_orders": data.get("po_number"),
        "payments": data.get("payment_number"),
        "products": data.get("sku"),
    }
    value = keys.get(entity_type)
    return f"{entity_type}:{value}" if value else None


def _build_model(entity_type: str, data: dict):
    builders = {
        "suppliers": _build_supplier,
        "purchase_orders": _build_purchase_order,
        "invoices": _build_invoice,
        "payments": _build_payment,
        "products": _build_product,
        "inventory_snapshots": _build_inventory_snapshot,
        "stock_movements": _build_stock_movement,
    }
    if entity_type not in builders:
        raise ValueError("Esta plantilla es descargable, pero no importable todavia.")
    return builders[entity_type](data)


def _build_supplier(data: dict) -> Supplier:
    if Supplier.query.filter_by(supplier_code=str(data["supplier_code"])).first():
        raise ValueError("Ya existe un proveedor con ese supplier_code.")
    return Supplier(
        supplier_code=str(data["supplier_code"]),
        name=str(data["name"]),
        tax_id=_optional_str(data.get("tax_id")),
        bank_account=_optional_str(data.get("bank_account")),
        address=_optional_str(data.get("address")),
        phone=_optional_str(data.get("phone")),
        email=_optional_str(data.get("email")),
        created_date=_date_value(data.get("created_date")),
        status=_optional_str(data.get("status")) or "active",
    )


def _build_purchase_order(data: dict) -> PurchaseOrder:
    supplier = _supplier_by_code(data.get("supplier_code"))
    if PurchaseOrder.query.filter_by(po_number=str(data["po_number"])).first():
        raise ValueError("Ya existe una orden con ese po_number.")
    amount = parse_decimal(data.get("total_amount"))
    if amount < 0:
        raise ValueError("total_amount no puede ser negativo.")
    return PurchaseOrder(
        po_number=str(data["po_number"]),
        supplier_id=supplier.id,
        requester_user_code=_optional_str(data.get("requester_user_code")),
        approver_user_code=_optional_str(data.get("approver_user_code")),
        order_date=_date_value(data.get("order_date")),
        total_amount=amount,
        status=_optional_str(data.get("status")) or "draft",
    )


def _build_invoice(data: dict) -> Invoice:
    supplier = _supplier_by_code(data.get("supplier_code"))
    purchase_order = None
    if data.get("po_number"):
        purchase_order = PurchaseOrder.query.filter_by(po_number=str(data["po_number"])).first()
        if not purchase_order:
            raise ValueError("No existe una orden con ese po_number.")
    amount = parse_decimal(data.get("total_amount"))
    if amount < 0:
        raise ValueError("total_amount no puede ser negativo.")
    return Invoice(
        invoice_number=str(data["invoice_number"]),
        supplier_id=supplier.id,
        purchase_order_id=purchase_order.id if purchase_order else None,
        issue_date=_date_value(data.get("issue_date")),
        due_date=_date_value(data.get("due_date")),
        total_amount=amount,
        status=_optional_str(data.get("status")) or "pending",
    )


def _build_payment(data: dict) -> Payment:
    supplier = _supplier_by_code(data.get("supplier_code"))
    invoice = None
    if data.get("invoice_number"):
        invoice = (
            Invoice.query.filter_by(
                supplier_id=supplier.id,
                invoice_number=str(data["invoice_number"]),
            )
            .order_by(Invoice.id.desc())
            .first()
        )
        if not invoice:
            raise ValueError("No existe una factura para ese supplier_code e invoice_number.")
    if Payment.query.filter_by(payment_number=str(data["payment_number"])).first():
        raise ValueError("Ya existe un pago con ese payment_number.")
    amount = parse_decimal(data.get("amount"))
    if amount < 0:
        raise ValueError("amount no puede ser negativo.")
    return Payment(
        payment_number=str(data["payment_number"]),
        supplier_id=supplier.id,
        invoice_id=invoice.id if invoice else None,
        payment_date=_datetime_value(data.get("payment_date")),
        amount=amount,
        payment_method=_optional_str(data.get("payment_method")),
        bank_account=_optional_str(data.get("bank_account")),
        created_by_user_code=_optional_str(data.get("created_by_user_code")),
    )


def _build_product(data: dict) -> Product:
    if Product.query.filter_by(sku=str(data["sku"])).first():
        raise ValueError("Ya existe un producto con ese sku.")
    unit_cost = parse_decimal(data.get("unit_cost"), "0")
    if unit_cost < 0:
        raise ValueError("unit_cost no puede ser negativo.")
    return Product(
        sku=str(data["sku"]),
        name=str(data["name"]),
        category=_optional_str(data.get("category")),
        unit_cost=unit_cost,
        is_active=parse_bool(str(data.get("is_active")).lower()) if data.get("is_active") is not None else True,
    )


def _build_inventory_snapshot(data: dict) -> InventorySnapshot:
    product = _product_by_sku(data.get("sku"))
    expected = parse_decimal(data.get("expected_quantity"))
    physical = parse_decimal(data.get("physical_quantity"))
    return InventorySnapshot(
        product_id=product.id,
        snapshot_date=_date_value(data.get("snapshot_date"), required=True),
        expected_quantity=expected,
        physical_quantity=physical,
        difference_quantity=physical - expected,
    )


def _build_stock_movement(data: dict) -> StockMovement:
    product = _product_by_sku(data.get("sku"))
    movement_type = str(data["movement_type"]).strip().upper()
    if movement_type not in MOVEMENT_TYPES:
        raise ValueError("movement_type debe ser IN, OUT, ADJUSTMENT o TRANSFER.")
    quantity = parse_decimal(data.get("quantity"))
    if quantity == 0:
        raise ValueError("quantity no puede ser cero.")
    return StockMovement(
        product_id=product.id,
        movement_type=movement_type,
        quantity=quantity,
        movement_date=_datetime_value(data.get("movement_date"), required=True),
        reference=_optional_str(data.get("reference")),
        reason=_optional_str(data.get("reason")),
        created_by_user_code=_optional_str(data.get("created_by_user_code")),
    )


def _supplier_by_code(supplier_code) -> Supplier:
    supplier = Supplier.query.filter_by(supplier_code=str(supplier_code)).first()
    if not supplier:
        raise ValueError("No existe un proveedor con ese supplier_code.")
    return supplier


def _product_by_sku(sku) -> Product:
    product = Product.query.filter_by(sku=str(sku)).first()
    if not product:
        raise ValueError("No existe un producto con ese sku.")
    return product


def _optional_str(value) -> str | None:
    if value in (None, ""):
        return None
    return str(value).strip()


def _date_value(value, required: bool = False):
    if value in (None, ""):
        if required:
            raise ValueError("La fecha es obligatoria.")
        return None
    return pd.to_datetime(value).date()


def _datetime_value(value, required: bool = False):
    if value in (None, ""):
        if required:
            raise ValueError("La fecha y hora es obligatoria.")
        return None
    return pd.to_datetime(value).to_pydatetime()


def _create_import_log(
    file_name: str,
    file_type: str,
    entity_type: str,
    status: str,
    total_rows: int,
    imported_rows: int,
    rejected_rows: int,
    errors: list[dict],
) -> ImportLog:
    log = ImportLog(
        file_name=file_name,
        file_type=file_type,
        entity_type=entity_type,
        status=status,
        total_rows=total_rows,
        imported_rows=imported_rows,
        rejected_rows=rejected_rows,
        warnings_count=0,
        errors_json=errors,
        created_by_user_id=current_user.id if current_user.is_authenticated else None,
    )
    db.session.add(log)
    return log


def _message_from_exception(exc: Exception) -> str:
    if isinstance(exc, IntegrityError):
        return "El registro viola una restriccion de unicidad o relacion."
    return str(exc)
