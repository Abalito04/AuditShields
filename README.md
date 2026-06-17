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

Railway uses [backend/railway.json](backend/railway.json) to start the app with Gunicorn:

```bash
gunicorn run:app --bind 0.0.0.0:$PORT
```

If Railway is configured from the repository root instead, the root-level [railway.json](railway.json), [requirements.txt](requirements.txt), and [Procfile](Procfile) point Railpack to the backend app.
