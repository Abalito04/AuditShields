from flask import Blueprint, render_template, send_file
from flask_login import login_required

from app.services.report_service import (
    build_alerts_report,
    build_cases_report,
    build_risk_summary_report,
)


reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


@reports_bp.get("/")
@login_required
def index():
    return render_template("reports/index.html")


@reports_bp.get("/cases.xlsx")
@login_required
def cases_xlsx():
    output, filename = build_cases_report()
    return _xlsx_response(output, filename)


@reports_bp.get("/alerts.xlsx")
@login_required
def alerts_xlsx():
    output, filename = build_alerts_report()
    return _xlsx_response(output, filename)


@reports_bp.get("/risk-summary.xlsx")
@login_required
def risk_summary_xlsx():
    output, filename = build_risk_summary_report()
    return _xlsx_response(output, filename)


def _xlsx_response(output, filename: str):
    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
