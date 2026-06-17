from pathlib import Path

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from flask_login import login_required
from werkzeug.utils import secure_filename

from app.models import ImportLog
from app.services.import_service import ALLOWED_EXTENSIONS, import_file
from app.services.template_service import generate_template
from app.services.validation_service import ENTITY_SCHEMAS, get_entity_schema


imports_bp = Blueprint("imports", __name__)


@imports_bp.get("/imports")
@imports_bp.get("/imports/")
@login_required
def index():
    pagination = ImportLog.query.order_by(ImportLog.created_at.desc()).paginate(
        page=request.args.get("page", 1, type=int), per_page=20, error_out=False
    )
    return render_template(
        "imports/index.html",
        pagination=pagination,
        entity_schemas=ENTITY_SCHEMAS,
    )


@imports_bp.get("/imports/new")
@login_required
def new():
    return render_template("imports/new.html", entity_schemas=ENTITY_SCHEMAS)


@imports_bp.post("/imports/upload")
@login_required
def upload():
    entity_type = request.form.get("entity_type", "")
    uploaded_file = request.files.get("file")

    try:
        get_entity_schema(entity_type)
    except ValueError:
        flash("Selecciona una entidad valida.", "danger")
        return redirect(url_for("imports.new"))

    if not uploaded_file or not uploaded_file.filename:
        flash("Selecciona un archivo .xlsx o .csv.", "danger")
        return redirect(url_for("imports.new"))

    extension = Path(uploaded_file.filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        flash("Solo se permiten archivos .xlsx o .csv.", "danger")
        return redirect(url_for("imports.new"))

    upload_dir = Path(current_app.config["UPLOAD_FOLDER"])
    upload_dir.mkdir(parents=True, exist_ok=True)
    safe_name = secure_filename(uploaded_file.filename)
    file_path = upload_dir / safe_name
    uploaded_file.save(file_path)

    try:
        result = import_file(entity_type, file_path, uploaded_file.filename)
    except ValueError as exc:
        flash(str(exc), "danger")
        return redirect(url_for("imports.new"))

    if result.errors:
        flash("Importacion finalizada con errores. Revisa el detalle.", "warning")
    else:
        flash("Importacion completada correctamente.", "success")
    return redirect(url_for("imports.detail", item_id=result.log.id))


@imports_bp.get("/imports/<int:item_id>")
@login_required
def detail(item_id: int):
    import_log = ImportLog.query.get_or_404(item_id)
    return render_template("imports/detail.html", import_log=import_log)


@imports_bp.get("/templates/<entity_type>/download")
@login_required
def download_template(entity_type: str):
    try:
        output, filename = generate_template(entity_type)
    except ValueError:
        abort(404)
    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
