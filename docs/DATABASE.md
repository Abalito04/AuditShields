# Base de datos

AuditShields usa SQLAlchemy y migraciones Alembic/Flask-Migrate. La base principal recomendada es PostgreSQL.

## Seguridad

### users

Usuarios de la aplicacion.

Campos clave:

- `name`
- `email`
- `password_hash`
- `role`
- `is_active`

Roles:

- `admin`
- `auditor`
- `readonly`

### audit_logs

Registro de acciones criticas.

Campos clave:

- `user_id`
- `action`
- `entity_type`
- `entity_id`
- `old_value`
- `new_value`
- `created_at`

## Compras, proveedores y pagos

### suppliers

Catalogo de proveedores.

Relaciones:

- un proveedor tiene muchas ordenes;
- un proveedor tiene muchas facturas;
- un proveedor tiene muchos pagos.

Campos importantes:

- `supplier_code`
- `name`
- `tax_id`
- `bank_account`
- `address`
- `email`
- `created_date`
- `status`

### purchase_orders

Ordenes de compra.

Relaciones:

- pertenecen a un proveedor;
- pueden tener muchas facturas.

Campos importantes:

- `po_number`
- `supplier_id`
- `requester_user_code`
- `approver_user_code`
- `order_date`
- `total_amount`
- `status`

### invoices

Facturas de proveedor.

Relaciones:

- pertenecen a un proveedor;
- pueden tener una orden de compra;
- pueden tener pagos.

La orden de compra es opcional porque una factura sin orden es una senal auditable.

### payments

Pagos registrados.

Relaciones:

- pertenecen a un proveedor;
- pueden estar asociados a una factura.

La factura es opcional porque un pago sin factura es una senal auditable.

## Inventario

### products

Catalogo de productos.

Campos:

- `sku`
- `name`
- `category`
- `unit_cost`
- `is_active`

### inventory_snapshots

Conteos fisicos de inventario.

Campos:

- `product_id`
- `snapshot_date`
- `expected_quantity`
- `physical_quantity`
- `difference_quantity`

La diferencia se calcula como:

```text
physical_quantity - expected_quantity
```

### stock_movements

Movimientos de stock.

Tipos:

- `IN`
- `OUT`
- `ADJUSTMENT`
- `TRANSFER`

Campos:

- `product_id`
- `movement_type`
- `quantity`
- `movement_date`
- `reference`
- `reason`
- `created_by_user_code`

El sistema permite stock negativo temporalmente para que una regla lo detecte.

## Auditoria antifraude

### fraud_rules

Catalogo de reglas.

Campos:

- `code`
- `name`
- `module`
- `description`
- `risk_level_default`
- `is_active`
- `config_json`

### alerts

Alertas generadas por reglas.

Campos:

- `rule_id`
- `module`
- `entity_type`
- `entity_id`
- `title`
- `description`
- `risk_score`
- `risk_level`
- `amount_at_risk`
- `evidence_json`
- `status`
- `fingerprint`

El `fingerprint` evita duplicados cuando se reejecuta la auditoria.

### cases

Casos de auditoria creados automaticamente desde alertas.

Campos:

- `case_number`
- `alert_id`
- `title`
- `description`
- `risk_score`
- `risk_level`
- `status`
- `assigned_to_user_id`
- `resolution_summary`
- `normalized_at`
- `closed_at`

### case_comments

Comentarios internos del caso.

### case_history

Historial de cambios del caso.

Registra:

- accion;
- usuario;
- estado anterior;
- estado nuevo;
- fecha.

## Importaciones

### imports

Historial de cargas Excel/CSV.

Campos:

- `file_name`
- `file_type`
- `entity_type`
- `status`
- `total_rows`
- `imported_rows`
- `rejected_rows`
- `warnings_count`
- `errors_json`
- `created_by_user_id`

## Flujo de datos

```text
Carga manual o importacion
  -> validacion
  -> persistencia
  -> ejecucion de reglas
  -> alertas
  -> casos
  -> gestion y cierre
  -> reportes
```
