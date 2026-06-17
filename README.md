# AuditShields

AuditShields is a web platform for continuous audit and antifraud controls in small and medium-sized businesses. The MVP focuses on purchases, suppliers, payments, stock, and inventory using clear, traceable, explainable rules.

The system is intended to help owners, managers, and auditors answer where money may be leaking, which controls are failing, and which cases need correction, normalization, or closure. It does not automatically accuse people; it detects risk signals and supports an auditable review process.

## Stack

- Python
- Flask
- Jinja2 / HTML
- PostgreSQL
- SQLAlchemy
- Flask-Migrate / Alembic
- Flask-Login
- Bootstrap or simple CSS
- Pandas and openpyxl
- pytest
- Docker Compose for PostgreSQL and auxiliary services

The MVP intentionally excludes React, machine learning, OCR, external ERP integrations, mobile apps, real multi-tenancy, and PDF reports.

## Project Structure

```text
AuditShields/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── templates/
│   │   ├── static/
│   │   └── utils/
│   ├── migrations/
│   ├── tests/
│   ├── seed/
│   ├── requirements.txt
│   ├── run.py
│   └── .env.example
├── data/
│   ├── samples/
│   ├── templates/
│   ├── imports/
│   └── exports/
├── docs/
├── scripts/
├── docker-compose.yml
├── AGENTS.md
├── ROADMAP.md
├── PROMPTS_CODEX.md
└── README.md
```

## Initial Commands

Start PostgreSQL:

```bash
docker compose up -d
```

Create and activate a virtual environment from `backend/`:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy the example environment file and adjust values if needed:

```bash
copy .env.example .env
```

Future phases will add migrations, domain models, authentication, imports, antifraud rules, alerts, audit cases, and Excel reports.

## Run Flask Locally

From `backend/`, with the virtual environment active:

```bash
flask run
```

Or:

```bash
python run.py
```

The initial dashboard is available at:

```text
http://127.0.0.1:5000/
```

## Database Migrations

With `DATABASE_URL` pointing to PostgreSQL and the virtual environment active:

```bash
cd backend
flask db upgrade
```

The initial migration creates the base security, purchasing, inventory, antifraud, alert, case, import, and audit log tables.

## Importaciones y plantillas

Con la app corriendo, desde la seccion `Importaciones` se pueden descargar plantillas Excel y subir archivos `.xlsx` o `.csv`.

Rutas utiles:

```text
/imports
/imports/new
/templates/suppliers/download
/templates/purchase_orders/download
/templates/invoices/download
/templates/payments/download
/templates/products/download
/templates/inventory_snapshots/download
/templates/stock_movements/download
```

La importacion valida columnas obligatorias, tipos basicos, montos, fechas y relaciones por codigos externos como `supplier_code`, `po_number`, `invoice_number` y `sku`. Las filas invalidas se rechazan y quedan registradas en el detalle de la importacion.

## Initial Admin User

After running migrations, create the initial admin user:

```bash
cd backend
python seed/seed_users.py
```

Development credentials:

```text
Email: admin@auditshields.local
Password: admin123
Role: admin
```

## Demo Data

To load realistic demo data for the antifraud rules:

```bash
cd backend
python seed/seed_demo_data.py
```

The script recreates only records with demo prefixes such as `DEMO-PROV-` and `DEMO-SKU-`. It includes normal records and suspicious scenarios: incomplete suppliers, shared bank accounts, duplicate invoices, duplicate payments, payments without invoice, high payments to a new supplier, stock differences, repeated adjustments, negative stock and movements outside business hours.

CSV samples for testing imports are available in `data/samples`. Import them from `/imports/new` in this order:

```text
01_suppliers_demo.csv
02_purchase_orders_demo.csv
03_invoices_demo.csv
04_payments_demo.csv
05_products_demo.csv
07_stock_movements_demo.csv
06_inventory_snapshots_demo.csv
```

## Run Antifraud Audit

From the dashboard, use `Ejecutar auditoria` to run the fraud engine. The base engine creates the default rule catalog, executes active rule functions, persists new alerts, ignores duplicated fingerprints and creates one audit case per alert.

Implemented purchase and supplier rules:

- R001 duplicate payments.
- R002 duplicate invoices.
- R003 suppliers sharing bank account.
- R004 new supplier with high payments.
- R005 payment or invoice without purchase order traceability.
- R006 split purchases below approval limit.
- R007 approver equal to requester.
- R008 excessive supplier concentration.
- R009 payment outside business hours.
- R010 incomplete supplier data.

Implemented inventory rules:

- S001 repeated manual adjustments.
- S002 negative stock.
- S003 inventory difference above threshold.
- S004 movement outside business hours.
- S005 excessive shrinkage.
- S006 unreconciled transfer.
- S007 operator with too many adjustments.
- S008 active product without recent movement.

## Railway Deploy

Recommended Railway service root directory:

```text
backend
```

Add these variables to the Flask app service:

```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
SECRET_KEY=replace-with-a-long-random-secret
FLASK_APP=run.py
FLASK_ENV=production
```

If the PostgreSQL service has another name, replace `Postgres` in the `DATABASE_URL` reference.

The project pins Python 3.12 with `.python-version` so Railway installs wheels for dependencies such as pandas instead of trying to compile them from source.

Railway uses [backend/railway.json](backend/railway.json) to start the app with Gunicorn:

```bash
gunicorn run:app --bind 0.0.0.0:$PORT
```

If Railway is configured from the repository root instead, the root-level [railway.json](railway.json), [requirements.txt](requirements.txt), and [Procfile](Procfile) point Railpack to the backend app.
