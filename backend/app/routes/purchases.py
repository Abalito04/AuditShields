from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Invoice, Payment, PurchaseOrder, Supplier
from app.routes.crud_helpers import commit_or_flash
from app.services.audit_log_service import model_snapshot, record_audit_log
from app.utils.parsing import (
    parse_decimal,
    parse_optional_date,
    parse_optional_datetime,
    parse_optional_int,
)


purchases_bp = Blueprint("purchases", __name__)

PO_FIELDS = [
    "po_number",
    "supplier_id",
    "requester_user_code",
    "approver_user_code",
    "order_date",
    "total_amount",
    "status",
]
INVOICE_FIELDS = [
    "invoice_number",
    "supplier_id",
    "purchase_order_id",
    "issue_date",
    "due_date",
    "total_amount",
    "status",
]
PAYMENT_FIELDS = [
    "payment_number",
    "supplier_id",
    "invoice_id",
    "payment_date",
    "amount",
    "payment_method",
    "bank_account",
    "created_by_user_code",
]


@purchases_bp.get("/purchase-orders")
@login_required
def purchase_orders():
    pagination = PurchaseOrder.query.order_by(PurchaseOrder.created_at.desc()).paginate(
        page=request.args.get("page", 1, type=int), per_page=20, error_out=False
    )
    return render_template(
        "crud/list.html",
        module="Compras",
        title="Ordenes de compra",
        description="Ordenes, solicitantes, aprobadores, montos y estados de aprobacion.",
        items=pagination.items,
        pagination=pagination,
        columns=[
            {"label": "Numero", "attr": "po_number"},
            {"label": "Proveedor", "formatter": lambda item: item.supplier.name},
            {"label": "Fecha", "attr": "order_date"},
            {"label": "Monto", "attr": "total_amount"},
            {"label": "Estado", "attr": "status"},
        ],
        create_endpoint="purchases.new_purchase_order",
        detail_endpoint="purchases.purchase_order_detail",
        edit_endpoint="purchases.edit_purchase_order",
        list_endpoint="purchases.purchase_orders",
    )


@purchases_bp.route("/purchase-orders/new", methods=["GET", "POST"])
@login_required
def new_purchase_order():
    order = PurchaseOrder(status="draft")
    if request.method == "POST" and _save_purchase_order(order, is_new=True):
        return redirect(url_for("purchases.purchase_order_detail", item_id=order.id))
    return _render_purchase_order_form(order, "Nueva orden de compra")


@purchases_bp.get("/purchase-orders/<int:item_id>")
@login_required
def purchase_order_detail(item_id: int):
    order = PurchaseOrder.query.get_or_404(item_id)
    return render_template(
        "crud/detail.html",
        module="Compras",
        title=order.po_number,
        description="Detalle de la orden de compra.",
        rows=[
            {"label": "Numero", "value": order.po_number},
            {"label": "Proveedor", "value": order.supplier.name},
            {"label": "Nombre y apellido del solicitante", "value": order.requester_user_code},
            {"label": "Nombre y apellido del aprobador", "value": order.approver_user_code},
            {"label": "Fecha", "value": order.order_date},
            {"label": "Monto", "value": order.total_amount},
            {"label": "Estado", "value": order.status},
        ],
        edit_url=url_for("purchases.edit_purchase_order", item_id=order.id),
    )


@purchases_bp.route("/purchase-orders/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_purchase_order(item_id: int):
    order = PurchaseOrder.query.get_or_404(item_id)
    if request.method == "POST" and _save_purchase_order(order, is_new=False):
        return redirect(url_for("purchases.purchase_order_detail", item_id=order.id))
    return _render_purchase_order_form(order, "Editar orden de compra")


@purchases_bp.get("/invoices")
@login_required
def invoices():
    pagination = Invoice.query.order_by(Invoice.created_at.desc()).paginate(
        page=request.args.get("page", 1, type=int), per_page=20, error_out=False
    )
    return render_template(
        "crud/list.html",
        module="Compras",
        title="Facturas",
        description="Facturas de proveedores, vencimientos, montos y vinculo con ordenes.",
        items=pagination.items,
        pagination=pagination,
        columns=[
            {"label": "Numero", "attr": "invoice_number"},
            {"label": "Proveedor", "formatter": lambda item: item.supplier.name},
            {
                "label": "Orden",
                "formatter": lambda item: item.purchase_order.po_number
                if item.purchase_order
                else "Sin orden",
            },
            {"label": "Fecha", "attr": "issue_date"},
            {"label": "Monto", "attr": "total_amount"},
            {"label": "Estado", "attr": "status"},
        ],
        create_endpoint="purchases.new_invoice",
        detail_endpoint="purchases.invoice_detail",
        edit_endpoint="purchases.edit_invoice",
        list_endpoint="purchases.invoices",
    )


@purchases_bp.route("/invoices/new", methods=["GET", "POST"])
@login_required
def new_invoice():
    invoice = Invoice(status="pending")
    if request.method == "POST" and _save_invoice(invoice, is_new=True):
        return redirect(url_for("purchases.invoice_detail", item_id=invoice.id))
    return _render_invoice_form(invoice, "Nueva factura")


@purchases_bp.get("/invoices/<int:item_id>")
@login_required
def invoice_detail(item_id: int):
    invoice = Invoice.query.get_or_404(item_id)
    return render_template(
        "crud/detail.html",
        module="Compras",
        title=invoice.invoice_number,
        description="Detalle de la factura de proveedor.",
        rows=[
            {"label": "Numero", "value": invoice.invoice_number},
            {"label": "Proveedor", "value": invoice.supplier.name},
            {
                "label": "Orden de compra",
                "value": invoice.purchase_order.po_number if invoice.purchase_order else "Sin orden",
            },
            {"label": "Emision", "value": invoice.issue_date},
            {"label": "Vencimiento", "value": invoice.due_date},
            {"label": "Monto", "value": invoice.total_amount},
            {"label": "Estado", "value": invoice.status},
        ],
        edit_url=url_for("purchases.edit_invoice", item_id=invoice.id),
    )


@purchases_bp.route("/invoices/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_invoice(item_id: int):
    invoice = Invoice.query.get_or_404(item_id)
    if request.method == "POST" and _save_invoice(invoice, is_new=False):
        return redirect(url_for("purchases.invoice_detail", item_id=invoice.id))
    return _render_invoice_form(invoice, "Editar factura")


@purchases_bp.get("/payments")
@login_required
def payments():
    pagination = Payment.query.order_by(Payment.created_at.desc()).paginate(
        page=request.args.get("page", 1, type=int), per_page=20, error_out=False
    )
    return render_template(
        "crud/list.html",
        module="Compras",
        title="Pagos",
        description="Pagos registrados, metodos, cuentas y relacion con facturas.",
        items=pagination.items,
        pagination=pagination,
        columns=[
            {"label": "Numero", "attr": "payment_number"},
            {"label": "Proveedor", "formatter": lambda item: item.supplier.name},
            {
                "label": "Factura",
                "formatter": lambda item: item.invoice.invoice_number
                if item.invoice
                else "Sin factura",
            },
            {"label": "Fecha", "attr": "payment_date"},
            {"label": "Monto", "attr": "amount"},
            {"label": "Metodo", "attr": "payment_method"},
        ],
        create_endpoint="purchases.new_payment",
        detail_endpoint="purchases.payment_detail",
        edit_endpoint="purchases.edit_payment",
        list_endpoint="purchases.payments",
    )


@purchases_bp.route("/payments/new", methods=["GET", "POST"])
@login_required
def new_payment():
    payment = Payment()
    if request.method == "POST" and _save_payment(payment, is_new=True):
        return redirect(url_for("purchases.payment_detail", item_id=payment.id))
    return _render_payment_form(payment, "Nuevo pago")


@purchases_bp.get("/payments/<int:item_id>")
@login_required
def payment_detail(item_id: int):
    payment = Payment.query.get_or_404(item_id)
    return render_template(
        "crud/detail.html",
        module="Compras",
        title=payment.payment_number,
        description="Detalle del pago registrado.",
        rows=[
            {"label": "Numero", "value": payment.payment_number},
            {"label": "Proveedor", "value": payment.supplier.name},
            {
                "label": "Factura",
                "value": payment.invoice.invoice_number if payment.invoice else "Sin factura",
            },
            {"label": "Fecha", "value": payment.payment_date},
            {"label": "Monto", "value": payment.amount},
            {"label": "Metodo", "value": payment.payment_method},
            {"label": "Cuenta bancaria", "value": payment.bank_account},
            {"label": "Nombre y apellido del operador", "value": payment.created_by_user_code},
        ],
        edit_url=url_for("purchases.edit_payment", item_id=payment.id),
    )


@purchases_bp.route("/payments/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_payment(item_id: int):
    payment = Payment.query.get_or_404(item_id)
    if request.method == "POST" and _save_payment(payment, is_new=False):
        return redirect(url_for("purchases.payment_detail", item_id=payment.id))
    return _render_payment_form(payment, "Editar pago")


def _save_purchase_order(order: PurchaseOrder, is_new: bool) -> bool:
    old_value = None if is_new else model_snapshot(order, PO_FIELDS)
    try:
        order.po_number = request.form.get("po_number", "").strip()
        order.supplier_id = parse_optional_int(request.form.get("supplier_id"))
        order.requester_user_code = request.form.get("requester_user_code", "").strip() or None
        order.approver_user_code = request.form.get("approver_user_code", "").strip() or None
        order.order_date = parse_optional_date(request.form.get("order_date"))
        order.total_amount = parse_decimal(request.form.get("total_amount"))
        order.status = request.form.get("status", "draft").strip() or "draft"
    except ValueError as exc:
        flash(str(exc), "danger")
        return False

    if not order.po_number or not order.supplier_id:
        flash("Numero de orden y proveedor son obligatorios.", "danger")
        return False
    if order.total_amount < 0:
        flash("El monto de la orden no puede ser negativo.", "danger")
        return False

    return _commit_with_audit(
        order,
        is_new,
        "purchase_order",
        PO_FIELDS,
        old_value,
        "Orden de compra guardada correctamente.",
        "No se pudo guardar la orden. Revisa si el numero ya existe.",
    )


def _save_invoice(invoice: Invoice, is_new: bool) -> bool:
    old_value = None if is_new else model_snapshot(invoice, INVOICE_FIELDS)
    try:
        invoice.invoice_number = request.form.get("invoice_number", "").strip()
        invoice.supplier_id = parse_optional_int(request.form.get("supplier_id"))
        invoice.purchase_order_id = parse_optional_int(request.form.get("purchase_order_id"))
        invoice.issue_date = parse_optional_date(request.form.get("issue_date"))
        invoice.due_date = parse_optional_date(request.form.get("due_date"))
        invoice.total_amount = parse_decimal(request.form.get("total_amount"))
        invoice.status = request.form.get("status", "pending").strip() or "pending"
    except ValueError as exc:
        flash(str(exc), "danger")
        return False

    if not invoice.invoice_number or not invoice.supplier_id:
        flash("Numero de factura y proveedor son obligatorios.", "danger")
        return False
    if invoice.total_amount < 0:
        flash("El monto de la factura no puede ser negativo.", "danger")
        return False

    return _commit_with_audit(
        invoice,
        is_new,
        "invoice",
        INVOICE_FIELDS,
        old_value,
        "Factura guardada correctamente.",
        "No se pudo guardar la factura. Revisa los datos cargados.",
    )


def _save_payment(payment: Payment, is_new: bool) -> bool:
    old_value = None if is_new else model_snapshot(payment, PAYMENT_FIELDS)
    try:
        payment.payment_number = request.form.get("payment_number", "").strip()
        payment.supplier_id = parse_optional_int(request.form.get("supplier_id"))
        payment.invoice_id = parse_optional_int(request.form.get("invoice_id"))
        payment.payment_date = parse_optional_datetime(request.form.get("payment_date"))
        payment.amount = parse_decimal(request.form.get("amount"))
        payment.payment_method = request.form.get("payment_method", "").strip() or None
        payment.bank_account = request.form.get("bank_account", "").strip() or None
        payment.created_by_user_code = (
            request.form.get("created_by_user_code", "").strip() or None
        )
    except ValueError as exc:
        flash(str(exc), "danger")
        return False

    if not payment.payment_number or not payment.supplier_id:
        flash("Numero de pago y proveedor son obligatorios.", "danger")
        return False
    if payment.amount < 0:
        flash("El monto del pago no puede ser negativo.", "danger")
        return False

    return _commit_with_audit(
        payment,
        is_new,
        "payment",
        PAYMENT_FIELDS,
        old_value,
        "Pago guardado correctamente.",
        "No se pudo guardar el pago. Revisa si el numero ya existe.",
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


def _render_purchase_order_form(order: PurchaseOrder, title: str):
    return render_template(
        "crud/form.html",
        module="Compras",
        title=title,
        description="Asocia la orden a un proveedor y registra aprobadores, fecha y monto.",
        fields=[
            _field("po_number", "Numero de orden", order.po_number, required=True),
            _select("supplier_id", "Proveedor", order.supplier_id, _supplier_options(), required=True),
            _field(
                "requester_user_code",
                "Nombre y apellido del solicitante",
                order.requester_user_code,
            ),
            _field(
                "approver_user_code",
                "Nombre y apellido del aprobador",
                order.approver_user_code,
            ),
            _field("order_date", "Fecha", order.order_date, field_type="date"),
            _field("total_amount", "Monto total", order.total_amount, field_type="number", step="0.01"),
            _field("status", "Estado", order.status),
        ],
        cancel_url=url_for("purchases.purchase_orders"),
    )


def _render_invoice_form(invoice: Invoice, title: str):
    return render_template(
        "crud/form.html",
        module="Compras",
        title=title,
        description="Registra la factura. La orden de compra es opcional para permitir auditoria posterior.",
        fields=[
            _field("invoice_number", "Numero de factura", invoice.invoice_number, required=True),
            _select("supplier_id", "Proveedor", invoice.supplier_id, _supplier_options(), required=True),
            _select(
                "purchase_order_id",
                "Orden de compra",
                invoice.purchase_order_id,
                _purchase_order_options(),
                empty_label="Sin orden de compra",
            ),
            _field("issue_date", "Fecha de emision", invoice.issue_date, field_type="date"),
            _field("due_date", "Fecha de vencimiento", invoice.due_date, field_type="date"),
            _field("total_amount", "Monto total", invoice.total_amount, field_type="number", step="0.01"),
            _field("status", "Estado", invoice.status),
        ],
        cancel_url=url_for("purchases.invoices"),
    )


def _render_payment_form(payment: Payment, title: str):
    return render_template(
        "crud/form.html",
        module="Compras",
        title=title,
        description="Registra el pago. La factura es opcional para permitir controles antifraude posteriores.",
        fields=[
            _field("payment_number", "Numero de pago", payment.payment_number, required=True),
            _select("supplier_id", "Proveedor", payment.supplier_id, _supplier_options(), required=True),
            _select(
                "invoice_id",
                "Factura",
                payment.invoice_id,
                _invoice_options(),
                empty_label="Sin factura",
            ),
            _field("payment_date", "Fecha y hora", _datetime_value(payment.payment_date), field_type="datetime-local"),
            _field("amount", "Monto", payment.amount, field_type="number", step="0.01"),
            _field("payment_method", "Metodo de pago", payment.payment_method),
            _field("bank_account", "Cuenta bancaria", payment.bank_account),
            _field(
                "created_by_user_code",
                "Nombre y apellido del operador",
                payment.created_by_user_code,
            ),
        ],
        cancel_url=url_for("purchases.payments"),
    )


def _supplier_options():
    return [
        {"value": supplier.id, "label": f"{supplier.supplier_code} - {supplier.name}"}
        for supplier in Supplier.query.order_by(Supplier.name.asc()).all()
    ]


def _purchase_order_options():
    return [
        {"value": order.id, "label": f"{order.po_number} - {order.supplier.name}"}
        for order in PurchaseOrder.query.order_by(PurchaseOrder.created_at.desc()).all()
    ]


def _invoice_options():
    return [
        {"value": invoice.id, "label": f"{invoice.invoice_number} - {invoice.supplier.name}"}
        for invoice in Invoice.query.order_by(Invoice.created_at.desc()).all()
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
