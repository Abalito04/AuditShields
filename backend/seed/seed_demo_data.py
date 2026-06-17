import sys
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import create_app
from app.extensions import db
from app.models import InventorySnapshot, Invoice, Payment, Product, PurchaseOrder, StockMovement, Supplier


DEMO_SUPPLIERS = [
    {
        "supplier_code": "DEMO-PROV-001",
        "name": "Insumos Norte SA",
        "tax_id": "30-11111111-1",
        "bank_account": "CBU-DEMO-0001",
        "address": "Av. Control 1200",
        "phone": "1144441001",
        "email": "administracion@insumosnorte.demo",
        "created_date": date.today() - timedelta(days=180),
        "status": "active",
    },
    {
        "supplier_code": "DEMO-PROV-002",
        "name": "Logistica Delta SRL",
        "tax_id": "30-22222222-2",
        "bank_account": "CBU-DEMO-COMPARTIDA",
        "address": "Ruta 8 Km 42",
        "phone": "1144441002",
        "email": "facturacion@logisticadelta.demo",
        "created_date": date.today() - timedelta(days=120),
        "status": "active",
    },
    {
        "supplier_code": "DEMO-PROV-003",
        "name": "Servicios Prisma",
        "tax_id": "30-33333333-3",
        "bank_account": "CBU-DEMO-COMPARTIDA",
        "address": "Calle Auditoria 455",
        "phone": "1144441003",
        "email": "contacto@prisma.demo",
        "created_date": date.today() - timedelta(days=90),
        "status": "active",
    },
    {
        "supplier_code": "DEMO-PROV-004",
        "name": "Proveedor Express Nuevo",
        "tax_id": "30-44444444-4",
        "bank_account": "CBU-DEMO-0004",
        "address": "Pasaje Riesgo 77",
        "phone": "1144441004",
        "email": "ventas@expressnuevo.demo",
        "created_date": date.today() - timedelta(days=8),
        "status": "active",
    },
    {
        "supplier_code": "DEMO-PROV-005",
        "name": "Proveedor Incompleto",
        "tax_id": None,
        "bank_account": None,
        "address": None,
        "phone": "1144441005",
        "email": None,
        "created_date": date.today() - timedelta(days=15),
        "status": "active",
    },
]

DEMO_PRODUCTS = [
    {"sku": "DEMO-SKU-001", "name": "Tornillo industrial", "category": "Ferreteria", "unit_cost": Decimal("120.00"), "is_active": True},
    {"sku": "DEMO-SKU-002", "name": "Guante nitrilo", "category": "Seguridad", "unit_cost": Decimal("850.00"), "is_active": True},
    {"sku": "DEMO-SKU-003", "name": "Repuesto critico A", "category": "Repuestos", "unit_cost": Decimal("45000.00"), "is_active": True},
]


def reset_demo_data() -> None:
    supplier_ids = [supplier.id for supplier in Supplier.query.filter(Supplier.supplier_code.like("DEMO-%")).all()]
    product_ids = [product.id for product in Product.query.filter(Product.sku.like("DEMO-%")).all()]

    if supplier_ids:
        payment_ids = [payment.id for payment in Payment.query.filter(Payment.supplier_id.in_(supplier_ids)).all()]
        invoice_ids = [invoice.id for invoice in Invoice.query.filter(Invoice.supplier_id.in_(supplier_ids)).all()]
        order_ids = [order.id for order in PurchaseOrder.query.filter(PurchaseOrder.supplier_id.in_(supplier_ids)).all()]
        if payment_ids:
            Payment.query.filter(Payment.id.in_(payment_ids)).delete(synchronize_session=False)
        if invoice_ids:
            Invoice.query.filter(Invoice.id.in_(invoice_ids)).delete(synchronize_session=False)
        if order_ids:
            PurchaseOrder.query.filter(PurchaseOrder.id.in_(order_ids)).delete(synchronize_session=False)
        Supplier.query.filter(Supplier.id.in_(supplier_ids)).delete(synchronize_session=False)

    if product_ids:
        StockMovement.query.filter(StockMovement.product_id.in_(product_ids)).delete(synchronize_session=False)
        InventorySnapshot.query.filter(InventorySnapshot.product_id.in_(product_ids)).delete(synchronize_session=False)
        Product.query.filter(Product.id.in_(product_ids)).delete(synchronize_session=False)

    db.session.commit()


def seed_suppliers() -> dict[str, Supplier]:
    suppliers = {}
    for data in DEMO_SUPPLIERS:
        supplier = Supplier(**data)
        db.session.add(supplier)
        suppliers[supplier.supplier_code] = supplier
    db.session.flush()
    return suppliers


def seed_purchases(suppliers: dict[str, Supplier]) -> None:
    orders = [
        PurchaseOrder(
            po_number="DEMO-OC-001",
            supplier=suppliers["DEMO-PROV-001"],
            requester_user_code="Ana Perez",
            approver_user_code="Luis Gomez",
            order_date=date.today() - timedelta(days=20),
            total_amount=Decimal("180000.00"),
            status="approved",
        ),
        PurchaseOrder(
            po_number="DEMO-OC-002",
            supplier=suppliers["DEMO-PROV-002"],
            requester_user_code="Carlos Ruiz",
            approver_user_code="Carlos Ruiz",
            order_date=date.today() - timedelta(days=12),
            total_amount=Decimal("480000.00"),
            status="approved",
        ),
        PurchaseOrder(
            po_number="DEMO-OC-003",
            supplier=suppliers["DEMO-PROV-002"],
            requester_user_code="Carlos Ruiz",
            approver_user_code="Marta Silva",
            order_date=date.today() - timedelta(days=11),
            total_amount=Decimal("475000.00"),
            status="approved",
        ),
        PurchaseOrder(
            po_number="DEMO-OC-004",
            supplier=suppliers["DEMO-PROV-002"],
            requester_user_code="Carlos Ruiz",
            approver_user_code="Marta Silva",
            order_date=date.today() - timedelta(days=10),
            total_amount=Decimal("490000.00"),
            status="approved",
        ),
        PurchaseOrder(
            po_number="DEMO-OC-005",
            supplier=suppliers["DEMO-PROV-004"],
            requester_user_code="Ana Perez",
            approver_user_code="Luis Gomez",
            order_date=date.today() - timedelta(days=5),
            total_amount=Decimal("950000.00"),
            status="draft",
        ),
    ]
    db.session.add_all(orders)
    db.session.flush()

    order_by_number = {order.po_number: order for order in orders}
    invoices = [
        Invoice(
            invoice_number="DEMO-FAC-001",
            supplier=suppliers["DEMO-PROV-001"],
            purchase_order=order_by_number["DEMO-OC-001"],
            issue_date=date.today() - timedelta(days=18),
            due_date=date.today() + timedelta(days=12),
            total_amount=Decimal("180000.00"),
            status="pending",
        ),
        Invoice(
            invoice_number="DEMO-FAC-DUP",
            supplier=suppliers["DEMO-PROV-002"],
            purchase_order=order_by_number["DEMO-OC-002"],
            issue_date=date.today() - timedelta(days=9),
            due_date=date.today() + timedelta(days=21),
            total_amount=Decimal("480000.00"),
            status="pending",
        ),
        Invoice(
            invoice_number="DEMO-FAC-DUP",
            supplier=suppliers["DEMO-PROV-002"],
            purchase_order=order_by_number["DEMO-OC-003"],
            issue_date=date.today() - timedelta(days=8),
            due_date=date.today() + timedelta(days=22),
            total_amount=Decimal("480000.00"),
            status="pending",
        ),
        Invoice(
            invoice_number="DEMO-FAC-SIN-OC",
            supplier=suppliers["DEMO-PROV-003"],
            purchase_order=None,
            issue_date=date.today() - timedelta(days=7),
            due_date=date.today() + timedelta(days=23),
            total_amount=Decimal("260000.00"),
            status="pending",
        ),
        Invoice(
            invoice_number="DEMO-FAC-NUEVO",
            supplier=suppliers["DEMO-PROV-004"],
            purchase_order=None,
            issue_date=date.today() - timedelta(days=4),
            due_date=date.today() + timedelta(days=26),
            total_amount=Decimal("1250000.00"),
            status="pending",
        ),
    ]
    db.session.add_all(invoices)
    db.session.flush()

    invoice_by_number = {}
    for invoice in invoices:
        invoice_by_number.setdefault(invoice.invoice_number, invoice)

    payments = [
        Payment(
            payment_number="DEMO-PAGO-001",
            supplier=suppliers["DEMO-PROV-001"],
            invoice=invoice_by_number["DEMO-FAC-001"],
            payment_date=datetime.now() - timedelta(days=15),
            amount=Decimal("180000.00"),
            payment_method="transfer",
            bank_account="CBU-DEMO-0001",
            created_by_user_code="Ana Perez",
        ),
        Payment(
            payment_number="DEMO-PAGO-DUP-1",
            supplier=suppliers["DEMO-PROV-002"],
            invoice=invoice_by_number["DEMO-FAC-DUP"],
            payment_date=datetime.now() - timedelta(days=6),
            amount=Decimal("480000.00"),
            payment_method="transfer",
            bank_account="CBU-DEMO-COMPARTIDA",
            created_by_user_code="Carlos Ruiz",
        ),
        Payment(
            payment_number="DEMO-PAGO-DUP-2",
            supplier=suppliers["DEMO-PROV-002"],
            invoice=invoice_by_number["DEMO-FAC-DUP"],
            payment_date=datetime.now() - timedelta(days=6, minutes=-30),
            amount=Decimal("480000.00"),
            payment_method="transfer",
            bank_account="CBU-DEMO-COMPARTIDA",
            created_by_user_code="Carlos Ruiz",
        ),
        Payment(
            payment_number="DEMO-PAGO-SIN-FACTURA",
            supplier=suppliers["DEMO-PROV-003"],
            invoice=None,
            payment_date=datetime.now() - timedelta(days=3),
            amount=Decimal("260000.00"),
            payment_method="cash",
            bank_account=None,
            created_by_user_code="Marta Silva",
        ),
        Payment(
            payment_number="DEMO-PAGO-FUERA-HORARIO",
            supplier=suppliers["DEMO-PROV-004"],
            invoice=invoice_by_number["DEMO-FAC-NUEVO"],
            payment_date=datetime.now().replace(hour=23, minute=40, second=0, microsecond=0),
            amount=Decimal("1250000.00"),
            payment_method="transfer",
            bank_account="CBU-DEMO-0004",
            created_by_user_code="Ana Perez",
        ),
    ]
    db.session.add_all(payments)


def seed_inventory() -> None:
    products = {}
    for data in DEMO_PRODUCTS:
        product = Product(**data)
        db.session.add(product)
        products[product.sku] = product
    db.session.flush()

    movements = [
        StockMovement(
            product=products["DEMO-SKU-001"],
            movement_type="IN",
            quantity=Decimal("500"),
            movement_date=datetime.now() - timedelta(days=20),
            reference="DEMO-REM-001",
            reason="Compra inicial",
            created_by_user_code="Ana Perez",
        ),
        StockMovement(
            product=products["DEMO-SKU-001"],
            movement_type="OUT",
            quantity=Decimal("120"),
            movement_date=datetime.now() - timedelta(days=10),
            reference="DEMO-EGR-001",
            reason="Consumo produccion",
            created_by_user_code="Ana Perez",
        ),
        StockMovement(
            product=products["DEMO-SKU-002"],
            movement_type="ADJUSTMENT",
            quantity=Decimal("-35"),
            movement_date=datetime.now() - timedelta(days=7),
            reference="DEMO-AJ-001",
            reason="Ajuste manual",
            created_by_user_code="Carlos Ruiz",
        ),
        StockMovement(
            product=products["DEMO-SKU-002"],
            movement_type="ADJUSTMENT",
            quantity=Decimal("-42"),
            movement_date=datetime.now() - timedelta(days=5),
            reference="DEMO-AJ-002",
            reason="Ajuste manual",
            created_by_user_code="Carlos Ruiz",
        ),
        StockMovement(
            product=products["DEMO-SKU-002"],
            movement_type="ADJUSTMENT",
            quantity=Decimal("-28"),
            movement_date=datetime.now() - timedelta(days=3),
            reference="DEMO-AJ-003",
            reason=None,
            created_by_user_code="Carlos Ruiz",
        ),
        StockMovement(
            product=products["DEMO-SKU-003"],
            movement_type="OUT",
            quantity=Decimal("12"),
            movement_date=datetime.now() - timedelta(days=2),
            reference=None,
            reason="Egreso sin documento",
            created_by_user_code="Marta Silva",
        ),
        StockMovement(
            product=products["DEMO-SKU-003"],
            movement_type="OUT",
            quantity=Decimal("6"),
            movement_date=datetime.now().replace(hour=22, minute=15, second=0, microsecond=0),
            reference="DEMO-EGR-FH",
            reason="Movimiento fuera de horario",
            created_by_user_code="Marta Silva",
        ),
    ]
    db.session.add_all(movements)

    snapshots = [
        InventorySnapshot(
            product=products["DEMO-SKU-001"],
            snapshot_date=date.today() - timedelta(days=1),
            expected_quantity=Decimal("380"),
            physical_quantity=Decimal("378"),
            difference_quantity=Decimal("-2"),
        ),
        InventorySnapshot(
            product=products["DEMO-SKU-002"],
            snapshot_date=date.today() - timedelta(days=1),
            expected_quantity=Decimal("200"),
            physical_quantity=Decimal("95"),
            difference_quantity=Decimal("-105"),
        ),
        InventorySnapshot(
            product=products["DEMO-SKU-003"],
            snapshot_date=date.today() - timedelta(days=1),
            expected_quantity=Decimal("-18"),
            physical_quantity=Decimal("-18"),
            difference_quantity=Decimal("0"),
        ),
    ]
    db.session.add_all(snapshots)


def seed_demo_data() -> None:
    reset_demo_data()
    suppliers = seed_suppliers()
    seed_purchases(suppliers)
    seed_inventory()
    db.session.commit()
    print("Demo data ready.")
    print("Suppliers: DEMO-PROV-001..005")
    print("Products: DEMO-SKU-001..003")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_demo_data()
