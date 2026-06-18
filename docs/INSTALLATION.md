# Instalacion

Esta guia explica como correr AuditShields localmente y como dejarlo preparado en Railway.

## Requisitos

- Python 3.12
- Git
- PostgreSQL local, Docker Desktop o PostgreSQL en Railway
- Git Bash en Windows

Docker es util para PostgreSQL local, pero no es obligatorio si se usa la base de Railway.

## Variables de entorno

Copiar el archivo de ejemplo:

```bash
cd backend
copy .env.example .env
```

Variables principales:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=change-me-in-local-env
DATABASE_URL=postgresql://auditshields:auditshields_dev_password@localhost:5432/auditshields
UPLOAD_FOLDER=../data/imports
EXPORT_FOLDER=../data/exports
MAX_CONTENT_LENGTH=10485760
```

En Railway, `DATABASE_URL` debe apuntar al PostgreSQL provisionado:

```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
FLASK_ENV=production
```

## Instalacion local con Git Bash

```bash
cd ~/OneDrive/Escritorio/AuditShields/backend
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

Si ya existe el entorno virtual:

```bash
cd ~/OneDrive/Escritorio/AuditShields/backend
source .venv/Scripts/activate
```

## Base de datos

Con PostgreSQL disponible y `DATABASE_URL` configurado:

```bash
cd backend
flask db upgrade
```

Crear usuario admin:

```bash
python seed/seed_users.py
```

Credenciales:

```text
admin@auditshields.local
admin123
```

## Correr la app

```bash
flask run
```

Abrir:

```text
http://127.0.0.1:5000/
```

## Datos demo

Por comando:

```bash
python seed/seed_demo_data.py
```

Por UI:

1. Entrar a `/imports/new`.
2. Importar CSVs de `data/samples` en orden:

```text
01_suppliers_demo.csv
02_purchase_orders_demo.csv
03_invoices_demo.csv
04_payments_demo.csv
05_products_demo.csv
07_stock_movements_demo.csv
06_inventory_snapshots_demo.csv
```

## Reset completo

Para dejar la base en blanco y conservar solo el usuario admin inicial:

```bash
cd backend
python seed/reset_database.py --yes
```

Este comando borra:

- proveedores, ordenes, facturas y pagos;
- productos, snapshots y movimientos;
- importaciones;
- reglas;
- alertas;
- casos, comentarios e historial;
- logs;
- usuarios.

Luego recrea:

```text
admin@auditshields.local / admin123
```

## Tests

```bash
pytest
```

Resultado esperado actual:

```text
9 passed
```

## Railway

Configuracion recomendada del servicio:

- Source repo: `Abalito04/AuditShields`
- Root directory: `backend`
- Railway config file: `/backend/railway.json`
- Builder: Railpack

Variables:

```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
SECRET_KEY=replace-with-a-long-random-secret
FLASK_APP=run.py
FLASK_ENV=production
MAX_CONTENT_LENGTH=10485760
```

Comandos utiles en Railway shell:

```bash
flask db upgrade
python seed/seed_users.py
```

No hace falta activar `.venv` en Railway.
