from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Supplier
from app.routes.crud_helpers import commit_or_flash
from app.services.audit_log_service import model_snapshot, record_audit_log
from app.utils.parsing import parse_optional_date


suppliers_bp = Blueprint("suppliers", __name__, url_prefix="/suppliers")

SUPPLIER_FIELDS = [
    "supplier_code",
    "name",
    "tax_id",
    "bank_account",
    "address",
    "phone",
    "email",
    "created_date",
    "status",
]


@suppliers_bp.get("/")
@login_required
def index():
    pagination = Supplier.query.order_by(Supplier.created_at.desc()).paginate(
        page=request.args.get("page", 1, type=int), per_page=20, error_out=False
    )
    return render_template(
        "crud/list.html",
        module="Compras",
        title="Proveedores",
        description="Catalogo de proveedores, datos fiscales, bancarios y estado operativo.",
        items=pagination.items,
        pagination=pagination,
        columns=[
            {"label": "Codigo", "attr": "supplier_code"},
            {"label": "Nombre", "attr": "name"},
            {"label": "CUIT/ID fiscal", "attr": "tax_id"},
            {"label": "Cuenta bancaria", "attr": "bank_account"},
            {"label": "Estado", "attr": "status"},
        ],
        create_endpoint="suppliers.new",
        detail_endpoint="suppliers.detail",
        edit_endpoint="suppliers.edit",
        list_endpoint="suppliers.index",
    )


@suppliers_bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    supplier = Supplier(status="active")
    if request.method == "POST":
        if _save_supplier(supplier, is_new=True):
            return redirect(url_for("suppliers.detail", item_id=supplier.id))
    return _render_supplier_form(supplier, "Nuevo proveedor")


@suppliers_bp.get("/<int:item_id>")
@login_required
def detail(item_id: int):
    supplier = Supplier.query.get_or_404(item_id)
    return render_template(
        "crud/detail.html",
        module="Compras",
        title=supplier.name,
        description="Detalle del proveedor y datos utiles para auditoria.",
        rows=[
            {"label": "Codigo", "value": supplier.supplier_code},
            {"label": "Nombre", "value": supplier.name},
            {"label": "CUIT/ID fiscal", "value": supplier.tax_id},
            {"label": "Cuenta bancaria", "value": supplier.bank_account},
            {"label": "Direccion", "value": supplier.address},
            {"label": "Telefono", "value": supplier.phone},
            {"label": "Email", "value": supplier.email},
            {"label": "Fecha de alta", "value": supplier.created_date},
            {"label": "Estado", "value": supplier.status},
        ],
        edit_url=url_for("suppliers.edit", item_id=supplier.id),
    )


@suppliers_bp.route("/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit(item_id: int):
    supplier = Supplier.query.get_or_404(item_id)
    if request.method == "POST":
        if _save_supplier(supplier, is_new=False):
            return redirect(url_for("suppliers.detail", item_id=supplier.id))
    return _render_supplier_form(supplier, "Editar proveedor")


def _render_supplier_form(supplier: Supplier, title: str):
    return render_template(
        "crud/form.html",
        module="Compras",
        title=title,
        description="Completa los datos principales del proveedor.",
        fields=[
            _field("supplier_code", "Codigo", supplier.supplier_code, required=True),
            _field("name", "Nombre", supplier.name, required=True),
            _field("tax_id", "CUIT/ID fiscal", supplier.tax_id),
            _field("bank_account", "Cuenta bancaria", supplier.bank_account),
            _field("address", "Direccion", supplier.address, wrapper_class="col-md-12"),
            _field("phone", "Telefono", supplier.phone),
            _field("email", "Email", supplier.email, field_type="email"),
            _field("created_date", "Fecha de alta", supplier.created_date, field_type="date"),
            _field("status", "Estado", supplier.status),
        ],
        cancel_url=url_for("suppliers.index"),
    )


def _save_supplier(supplier: Supplier, is_new: bool) -> bool:
    old_value = None if is_new else model_snapshot(supplier, SUPPLIER_FIELDS)
    supplier.supplier_code = request.form.get("supplier_code", "").strip()
    supplier.name = request.form.get("name", "").strip()
    supplier.tax_id = request.form.get("tax_id", "").strip() or None
    supplier.bank_account = request.form.get("bank_account", "").strip() or None
    supplier.address = request.form.get("address", "").strip() or None
    supplier.phone = request.form.get("phone", "").strip() or None
    supplier.email = request.form.get("email", "").strip() or None
    supplier.status = request.form.get("status", "active").strip() or "active"

    try:
        supplier.created_date = parse_optional_date(request.form.get("created_date"))
    except ValueError:
        flash("La fecha de alta no es valida.", "danger")
        return False

    if not supplier.supplier_code or not supplier.name:
        flash("Codigo y nombre son obligatorios.", "danger")
        return False

    if is_new:
        db.session.add(supplier)
    try:
        db.session.flush()
    except IntegrityError:
        db.session.rollback()
        flash("No se pudo guardar el proveedor. Revisa si el codigo ya existe.", "danger")
        return False
    record_audit_log(
        "create" if is_new else "update",
        "supplier",
        supplier.id,
        old_value=old_value,
        new_value=model_snapshot(supplier, SUPPLIER_FIELDS),
    )
    return commit_or_flash(
        "Proveedor guardado correctamente.",
        "No se pudo guardar el proveedor. Revisa si el codigo ya existe.",
    )


def _field(
    name: str,
    label: str,
    value=None,
    field_type: str = "text",
    required: bool = False,
    wrapper_class: str = "col-md-6",
):
    return {
        "name": name,
        "label": label,
        "value": value,
        "type": field_type,
        "required": required,
        "wrapper_class": wrapper_class,
    }
