from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import InventorySnapshot, Product, StockMovement
from app.routes.crud_helpers import commit_or_flash
from app.services.audit_log_service import model_snapshot, record_audit_log
from app.utils.parsing import parse_bool, parse_decimal, parse_optional_date, parse_optional_datetime


inventory_bp = Blueprint("inventory", __name__)

PRODUCT_FIELDS = ["sku", "name", "category", "unit_cost", "is_active"]
SNAPSHOT_FIELDS = [
    "product_id",
    "snapshot_date",
    "expected_quantity",
    "physical_quantity",
    "difference_quantity",
]
MOVEMENT_FIELDS = [
    "product_id",
    "movement_type",
    "quantity",
    "movement_date",
    "reference",
    "reason",
    "created_by_user_code",
]
MOVEMENT_TYPES = ["IN", "OUT", "ADJUSTMENT", "TRANSFER"]


@inventory_bp.get("/products")
@login_required
def products():
    pagination = Product.query.order_by(Product.created_at.desc()).paginate(
        page=request.args.get("page", 1, type=int), per_page=20, error_out=False
    )
    return render_template(
        "crud/list.html",
        module="Inventario",
        title="Productos",
        description="Catalogo de productos, SKU, categorias, costos y estado.",
        items=pagination.items,
        pagination=pagination,
        columns=[
            {"label": "SKU", "attr": "sku"},
            {"label": "Nombre", "attr": "name"},
            {"label": "Categoria", "attr": "category"},
            {"label": "Costo", "attr": "unit_cost"},
            {"label": "Activo", "formatter": lambda item: "Si" if item.is_active else "No"},
        ],
        create_endpoint="inventory.new_product",
        detail_endpoint="inventory.product_detail",
        edit_endpoint="inventory.edit_product",
        list_endpoint="inventory.products",
    )


@inventory_bp.route("/products/new", methods=["GET", "POST"])
@login_required
def new_product():
    product = Product(is_active=True)
    if request.method == "POST" and _save_product(product, is_new=True):
        return redirect(url_for("inventory.product_detail", item_id=product.id))
    return _render_product_form(product, "Nuevo producto")


@inventory_bp.get("/products/<int:item_id>")
@login_required
def product_detail(item_id: int):
    product = Product.query.get_or_404(item_id)
    snapshots = product.inventory_snapshots.order_by(
        InventorySnapshot.snapshot_date.desc(), InventorySnapshot.id.desc()
    ).limit(10)
    movements = product.stock_movements.order_by(
        StockMovement.movement_date.desc(), StockMovement.id.desc()
    ).limit(20)
    return render_template(
        "inventory/product_detail.html",
        module="Inventario",
        title=product.name,
        description="Detalle del producto con historial de stock y movimientos.",
        rows=[
            {"label": "SKU", "value": product.sku},
            {"label": "Nombre", "value": product.name},
            {"label": "Categoria", "value": product.category},
            {"label": "Costo unitario", "value": product.unit_cost},
            {"label": "Activo", "value": "Si" if product.is_active else "No"},
        ],
        edit_url=url_for("inventory.edit_product", item_id=product.id),
        snapshots=snapshots,
        movements=movements,
    )


@inventory_bp.route("/products/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_product(item_id: int):
    product = Product.query.get_or_404(item_id)
    if request.method == "POST" and _save_product(product, is_new=False):
        return redirect(url_for("inventory.product_detail", item_id=product.id))
    return _render_product_form(product, "Editar producto")


@inventory_bp.get("/stock")
@login_required
def stock():
    pagination = InventorySnapshot.query.order_by(
        InventorySnapshot.snapshot_date.desc(), InventorySnapshot.id.desc()
    ).paginate(page=request.args.get("page", 1, type=int), per_page=20, error_out=False)
    return render_template(
        "crud/list.html",
        module="Inventario",
        title="Stock",
        description="Snapshots fisicos, stock esperado y diferencias de inventario.",
        items=pagination.items,
        pagination=pagination,
        columns=[
            {"label": "Producto", "formatter": lambda item: item.product.name},
            {"label": "Fecha", "attr": "snapshot_date"},
            {"label": "Esperado", "attr": "expected_quantity"},
            {"label": "Fisico", "attr": "physical_quantity"},
            {"label": "Diferencia", "attr": "difference_quantity"},
        ],
        create_endpoint="inventory.new_snapshot",
        detail_endpoint="inventory.snapshot_detail",
        edit_endpoint="inventory.edit_snapshot",
        list_endpoint="inventory.stock",
    )


@inventory_bp.route("/stock/snapshots/new", methods=["GET", "POST"])
@login_required
def new_snapshot():
    snapshot = InventorySnapshot()
    if request.method == "POST" and _save_snapshot(snapshot, is_new=True):
        return redirect(url_for("inventory.snapshot_detail", item_id=snapshot.id))
    return _render_snapshot_form(snapshot, "Nuevo snapshot de stock")


@inventory_bp.get("/stock/snapshots/<int:item_id>")
@login_required
def snapshot_detail(item_id: int):
    snapshot = InventorySnapshot.query.get_or_404(item_id)
    return render_template(
        "crud/detail.html",
        module="Inventario",
        title=f"Snapshot {snapshot.product.sku}",
        description="Detalle del conteo fisico de inventario.",
        rows=[
            {"label": "Producto", "value": snapshot.product.name},
            {"label": "Fecha", "value": snapshot.snapshot_date},
            {"label": "Cantidad esperada", "value": snapshot.expected_quantity},
            {"label": "Cantidad fisica", "value": snapshot.physical_quantity},
            {"label": "Diferencia", "value": snapshot.difference_quantity},
        ],
        edit_url=url_for("inventory.edit_snapshot", item_id=snapshot.id),
    )


@inventory_bp.route("/stock/snapshots/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_snapshot(item_id: int):
    snapshot = InventorySnapshot.query.get_or_404(item_id)
    if request.method == "POST" and _save_snapshot(snapshot, is_new=False):
        return redirect(url_for("inventory.snapshot_detail", item_id=snapshot.id))
    return _render_snapshot_form(snapshot, "Editar snapshot de stock")


@inventory_bp.get("/stock/movements")
@login_required
def stock_movements():
    pagination = StockMovement.query.order_by(
        StockMovement.movement_date.desc(), StockMovement.id.desc()
    ).paginate(page=request.args.get("page", 1, type=int), per_page=20, error_out=False)
    return render_template(
        "crud/list.html",
        module="Inventario",
        title="Movimientos de stock",
        description="Entradas, salidas, ajustes, transferencias y motivos asociados.",
        items=pagination.items,
        pagination=pagination,
        columns=[
            {"label": "Producto", "formatter": lambda item: item.product.name},
            {"label": "Tipo", "attr": "movement_type"},
            {"label": "Cantidad", "attr": "quantity"},
            {"label": "Fecha", "attr": "movement_date"},
            {"label": "Referencia", "attr": "reference"},
        ],
        create_endpoint="inventory.new_movement",
        detail_endpoint="inventory.movement_detail",
        edit_endpoint="inventory.edit_movement",
        list_endpoint="inventory.stock_movements",
    )


@inventory_bp.route("/stock/movements/new", methods=["GET", "POST"])
@login_required
def new_movement():
    movement = StockMovement()
    if request.method == "POST" and _save_movement(movement, is_new=True):
        return redirect(url_for("inventory.movement_detail", item_id=movement.id))
    return _render_movement_form(movement, "Nuevo movimiento de stock")


@inventory_bp.get("/stock/movements/<int:item_id>")
@login_required
def movement_detail(item_id: int):
    movement = StockMovement.query.get_or_404(item_id)
    return render_template(
        "crud/detail.html",
        module="Inventario",
        title=f"{movement.movement_type} - {movement.product.sku}",
        description="Detalle del movimiento de stock.",
        rows=[
            {"label": "Producto", "value": movement.product.name},
            {"label": "Tipo", "value": movement.movement_type},
            {"label": "Cantidad", "value": movement.quantity},
            {"label": "Fecha", "value": movement.movement_date},
            {"label": "Referencia", "value": movement.reference},
            {"label": "Motivo", "value": movement.reason},
            {"label": "Usuario operativo", "value": movement.created_by_user_code},
        ],
        edit_url=url_for("inventory.edit_movement", item_id=movement.id),
    )


@inventory_bp.route("/stock/movements/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_movement(item_id: int):
    movement = StockMovement.query.get_or_404(item_id)
    if request.method == "POST" and _save_movement(movement, is_new=False):
        return redirect(url_for("inventory.movement_detail", item_id=movement.id))
    return _render_movement_form(movement, "Editar movimiento de stock")


def _save_product(product: Product, is_new: bool) -> bool:
    old_value = None if is_new else model_snapshot(product, PRODUCT_FIELDS)
    try:
        product.sku = request.form.get("sku", "").strip()
        product.name = request.form.get("name", "").strip()
        product.category = request.form.get("category", "").strip() or None
        product.unit_cost = parse_decimal(request.form.get("unit_cost"))
        product.is_active = parse_bool(request.form.get("is_active"))
    except ValueError as exc:
        flash(str(exc), "danger")
        return False

    if not product.sku or not product.name:
        flash("SKU y nombre son obligatorios.", "danger")
        return False
    if product.unit_cost < 0:
        flash("El costo unitario no puede ser negativo.", "danger")
        return False

    return _commit_with_audit(
        product,
        is_new,
        "product",
        PRODUCT_FIELDS,
        old_value,
        "Producto guardado correctamente.",
        "No se pudo guardar el producto. Revisa si el SKU ya existe.",
    )


def _save_snapshot(snapshot: InventorySnapshot, is_new: bool) -> bool:
    old_value = None if is_new else model_snapshot(snapshot, SNAPSHOT_FIELDS)
    try:
        snapshot.product_id = int(request.form.get("product_id", ""))
        snapshot.snapshot_date = parse_optional_date(request.form.get("snapshot_date"))
        snapshot.expected_quantity = parse_decimal(request.form.get("expected_quantity"))
        snapshot.physical_quantity = parse_decimal(request.form.get("physical_quantity"))
    except ValueError as exc:
        flash(str(exc), "danger")
        return False

    if not snapshot.product_id or not snapshot.snapshot_date:
        flash("Producto y fecha son obligatorios.", "danger")
        return False
    snapshot.difference_quantity = snapshot.physical_quantity - snapshot.expected_quantity

    return _commit_with_audit(
        snapshot,
        is_new,
        "inventory_snapshot",
        SNAPSHOT_FIELDS,
        old_value,
        "Snapshot de stock guardado correctamente.",
        "No se pudo guardar el snapshot. Revisa los datos cargados.",
    )


def _save_movement(movement: StockMovement, is_new: bool) -> bool:
    old_value = None if is_new else model_snapshot(movement, MOVEMENT_FIELDS)
    try:
        movement.product_id = int(request.form.get("product_id", ""))
        movement.movement_type = request.form.get("movement_type", "").strip()
        movement.quantity = parse_decimal(request.form.get("quantity"))
        movement.movement_date = parse_optional_datetime(request.form.get("movement_date"))
        movement.reference = request.form.get("reference", "").strip() or None
        movement.reason = request.form.get("reason", "").strip() or None
        movement.created_by_user_code = (
            request.form.get("created_by_user_code", "").strip() or None
        )
    except ValueError as exc:
        flash(str(exc), "danger")
        return False

    if not movement.product_id or not movement.movement_type or not movement.movement_date:
        flash("Producto, tipo y fecha son obligatorios.", "danger")
        return False
    if movement.movement_type not in MOVEMENT_TYPES:
        flash("El tipo de movimiento no es valido.", "danger")
        return False
    if movement.quantity == 0:
        flash("La cantidad del movimiento no puede ser cero.", "danger")
        return False

    return _commit_with_audit(
        movement,
        is_new,
        "stock_movement",
        MOVEMENT_FIELDS,
        old_value,
        "Movimiento de stock guardado correctamente.",
        "No se pudo guardar el movimiento. Revisa los datos cargados.",
    )


def _commit_with_audit(
    model,
    is_new: bool,
    entity_type: str,
    fields: list[str],
    old_value: dict | None,
    success_message: str,
    error_message: str,
) -> bool:
    if is_new:
        db.session.add(model)
    try:
        db.session.flush()
    except IntegrityError:
        db.session.rollback()
        flash(error_message, "danger")
        return False
    record_audit_log(
        "create" if is_new else "update",
        entity_type,
        model.id,
        old_value=old_value,
        new_value=model_snapshot(model, fields),
    )
    return commit_or_flash(success_message, error_message)


def _render_product_form(product: Product, title: str):
    return render_template(
        "crud/form.html",
        module="Inventario",
        title=title,
        description="Completa los datos principales del producto.",
        fields=[
            _field("sku", "SKU", product.sku, required=True),
            _field("name", "Nombre", product.name, required=True),
            _field("category", "Categoria", product.category),
            _field("unit_cost", "Costo unitario", product.unit_cost, field_type="number", step="0.01"),
            {
                "name": "is_active",
                "label": "Producto activo",
                "value": product.is_active,
                "type": "checkbox",
                "wrapper_class": "col-md-6",
            },
        ],
        cancel_url=url_for("inventory.products"),
    )


def _render_snapshot_form(snapshot: InventorySnapshot, title: str):
    return render_template(
        "crud/form.html",
        module="Inventario",
        title=title,
        description="Registra un conteo fisico. La diferencia se calcula automaticamente.",
        fields=[
            _select("product_id", "Producto", snapshot.product_id, _product_options(), required=True),
            _field("snapshot_date", "Fecha", snapshot.snapshot_date, field_type="date", required=True),
            _field("expected_quantity", "Cantidad esperada", snapshot.expected_quantity, field_type="number", step="0.001"),
            _field("physical_quantity", "Cantidad fisica", snapshot.physical_quantity, field_type="number", step="0.001"),
        ],
        cancel_url=url_for("inventory.stock"),
    )


def _render_movement_form(movement: StockMovement, title: str):
    return render_template(
        "crud/form.html",
        module="Inventario",
        title=title,
        description="Registra entradas, salidas, ajustes o transferencias de stock.",
        fields=[
            _select("product_id", "Producto", movement.product_id, _product_options(), required=True),
            _select(
                "movement_type",
                "Tipo",
                movement.movement_type,
                [{"value": value, "label": value} for value in MOVEMENT_TYPES],
                required=True,
            ),
            _field("quantity", "Cantidad", movement.quantity, field_type="number", step="0.001"),
            _field(
                "movement_date",
                "Fecha y hora",
                _datetime_value(movement.movement_date),
                field_type="datetime-local",
                required=True,
            ),
            _field("reference", "Referencia", movement.reference),
            _field("reason", "Motivo", movement.reason),
            _field("created_by_user_code", "Usuario operativo", movement.created_by_user_code),
        ],
        cancel_url=url_for("inventory.stock_movements"),
    )


def _product_options():
    return [
        {"value": product.id, "label": f"{product.sku} - {product.name}"}
        for product in Product.query.order_by(Product.name.asc()).all()
    ]


def _field(
    name: str,
    label: str,
    value=None,
    field_type: str = "text",
    required: bool = False,
    step: str | None = None,
):
    return {
        "name": name,
        "label": label,
        "value": value,
        "type": field_type,
        "required": required,
        "step": step,
        "wrapper_class": "col-md-6",
    }


def _select(
    name: str,
    label: str,
    value,
    options: list[dict],
    required: bool = False,
    empty_label: str = "Seleccionar",
):
    return {
        "name": name,
        "label": label,
        "value": value,
        "type": "select",
        "options": options,
        "required": required,
        "empty_label": empty_label,
        "wrapper_class": "col-md-6",
    }


def _datetime_value(value):
    return value.strftime("%Y-%m-%dT%H:%M") if value else None
