# AuditShields

AuditShields es una plataforma web de auditoria continua y control antifraude para PyMEs. El MVP se enfoca en compras, proveedores, pagos, stock e inventario usando reglas claras, trazables y explicables.

El objetivo no es acusar personas automaticamente. El sistema detecta senales de riesgo, genera alertas, crea casos de auditoria y permite gestionarlos hasta su correccion, normalizacion o cierre.

## Stack

- Python
- Flask
- Jinja2 / HTML
- PostgreSQL
- SQLAlchemy
- Flask-Migrate / Alembic
- Flask-Login
- Bootstrap
- Pandas y openpyxl
- pytest
- Gunicorn para deploy

El MVP excluye React, machine learning, OCR, integraciones ERP, app movil, multi-tenant real y reportes PDF.

## Funcionalidades del MVP

- Login con roles `admin`, `auditor` y `readonly`.
- CRUD de proveedores, ordenes, facturas, pagos, productos, stock y movimientos.
- Plantillas Excel descargables.
- Importacion Excel/CSV con validaciones.
- Datos demo y CSVs de ejemplo.
- Motor antifraude con reglas R001-R010 y S001-S008.
- Alertas explicables con evidencia JSON y score.
- Creacion automatica de casos por alerta.
- Gestion de casos con estados, comentarios, asignacion e historial.
- Dashboard con metricas reales.
- Reportes Excel de alertas, casos y resumen de riesgo.
- Tests basicos del flujo critico.

## Estructura

```text
AuditShields/
  backend/
    app/
      models/
      routes/
      services/
      templates/
      utils/
    migrations/
    seed/
    tests/
    requirements.txt
    run.py
  data/
    samples/
    templates/
    imports/
    exports/
  docs/
  docker-compose.yml
  AGENTS.md
  ROADMAP.md
  PROMPTS_CODEX.md
  README.md
```

## Inicio rapido local

Desde Git Bash:

```bash
cd ~/OneDrive/Escritorio/AuditShields/backend
source .venv/Scripts/activate
pip install -r requirements.txt
copy .env.example .env
flask db upgrade
python seed/seed_users.py
flask run
```

Usuario inicial:

```text
Email: admin@auditshields.local
Password: admin123
```

## Datos demo

Opcion por comando:

```bash
cd backend
python seed/seed_demo_data.py
```

Opcion desde UI:

1. Entrar a `/imports/new`.
2. Importar los CSV de `data/samples` en este orden:

```text
01_suppliers_demo.csv
02_purchase_orders_demo.csv
03_invoices_demo.csv
04_payments_demo.csv
05_products_demo.csv
07_stock_movements_demo.csv
06_inventory_snapshots_demo.csv
```

## Flujo principal

1. Iniciar sesion.
2. Cargar datos manualmente o importar Excel/CSV.
3. Ejecutar auditoria desde el dashboard.
4. Revisar alertas en `/alerts`.
5. Gestionar casos en `/cases`.
6. Exportar reportes en `/reports`.

Para una demo rapida, usar `Preparar demo` en el dashboard. Esa accion recrea datos `DEMO-*`, ejecuta auditoria y deja alertas/casos listos para presentar.

## Reportes

```text
/reports/cases.xlsx
/reports/alerts.xlsx
/reports/risk-summary.xlsx
```

## Tests

```bash
cd backend
pytest
```

Estado actual: `9 passed`.

## Deploy en Railway

Configuracion recomendada:

- Root directory del servicio: `backend`
- Railway config file: `/backend/railway.json`
- Start command: definido en `railway.json`

Variables:

```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
SECRET_KEY=replace-with-a-long-random-secret
FLASK_APP=run.py
FLASK_ENV=production
MAX_CONTENT_LENGTH=10485760
```

Luego ejecutar en Railway, si hace falta:

```bash
flask db upgrade
python seed/seed_users.py
```

## Documentacion

- [Instalacion](docs/INSTALLATION.md)
- [Guia de usuario](docs/USER_GUIDE.md)
- [Base de datos](docs/DATABASE.md)
- [Reglas antifraude](docs/RULES.md)
- [Guion de demo](docs/DEMO_SCRIPT.md)
