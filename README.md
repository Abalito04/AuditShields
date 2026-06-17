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

Future phases will add the Flask app factory, migrations, routes, models, authentication, imports, antifraud rules, alerts, audit cases, and Excel reports.
