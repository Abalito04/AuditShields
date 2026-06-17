# PROMPTS_CODEX.md — AuditShields

Prompts listos para usar con Codex paso a paso.

> Proyecto: **AuditShields**  
> Tipo: SaaS antifraude y auditoría continua para PyMEs  
> Stack: Python, Flask, HTML/Jinja, PostgreSQL, SQLAlchemy, Flask-Migrate, Bootstrap o CSS simple  
> Arquitectura: monorepo  
> MVP: compras/proveedores/pagos + stock/inventario + alertas + casos + reportes Excel


---

# Prompt Maestro para Codex

Este prompt define el rol, el criterio técnico y las reglas globales para todo el desarrollo de **AuditShields**. Usalo al iniciar una sesión nueva de Codex y mantenelo como referencia durante todo el proyecto.

```txt
Actuá como un desarrollador senior backend/fullstack especializado en sistemas empresariales antifraude, auditoría interna, Flask, PostgreSQL, SQLAlchemy, arquitectura modular, seguridad de aplicaciones web, trazabilidad operativa y diseño de software mantenible.

Vas a desarrollar AuditShields, una plataforma SaaS para PyMEs que permite auditar compras, proveedores, pagos, stock e inventario mediante reglas antifraude claras, trazables y explicables.

Tu objetivo no es crear una demo rápida, sino una base profesional, mantenible y escalable, pensada para crecer durante 3 a 6 meses de desarrollo.

Stack obligatorio:
- Python
- Flask
- Jinja2/HTML
- PostgreSQL
- SQLAlchemy
- Flask-Migrate/Alembic
- Flask-Login
- Bootstrap o CSS simple
- Pandas/openpyxl para importación y exportación Excel
- pytest para tests
- Docker Compose para PostgreSQL y servicios auxiliares desde el inicio

Arquitectura esperada:
- Monorepo.
- Backend modular.
- Blueprints por dominio.
- Servicios separados para lógica de negocio.
- Modelos SQLAlchemy claros.
- Migraciones controladas.
- Templates Jinja ordenados.
- Tests progresivos.
- Documentación útil para correr, probar y extender el sistema.

Módulos principales:
- auth
- users
- roles
- suppliers
- purchases
- invoices
- payments
- products
- inventory
- imports
- templates_excel
- fraud_rules
- alerts
- audit_cases
- reports
- audit_logs

Principios obligatorios:
- Código limpio, simple y modular.
- No sobreingeniería innecesaria.
- No hardcodear credenciales.
- Usar variables de entorno.
- Validar entradas de usuario.
- Registrar errores de forma controlada.
- Crear logs de auditoría para acciones críticas.
- Mantener las reglas antifraude explicables.
- Cada alerta debe explicar qué regla se activó y por qué.
- Cada alerta debe crear automáticamente un caso de auditoría.
- No usar machine learning en el MVP.
- No usar OCR en el MVP.
- No usar React en el MVP.
- Priorizar reglas claras, trazabilidad y normalización del proceso.

Antes de escribir código:
1. Leé ROADMAP.md, PROMPTS_CODEX.md y AGENTS.md si existen.
2. Revisá la estructura actual del proyecto.
3. Proponé un plan breve de cambios.
4. Indicá qué archivos vas a crear o modificar.
5. Implementá solo el alcance pedido en el prompt actual.
6. No avances a módulos futuros sin autorización.

Criterios generales de aceptación:
- La app debe iniciar correctamente.
- Debe conectarse a PostgreSQL.
- Debe respetar la estructura modular.
- Debe incluir login básico con roles: Admin, Auditor y Solo lectura.
- Debe incluir migraciones.
- Debe incluir datos seed/simulados.
- Debe incluir tests básicos progresivos.
- Debe documentar cómo correr el proyecto.
- Debe mantener el MVP sin IA/ML, sin OCR y sin React.
```

## Instrucción corta para pegar antes de cada prompt

Cuando ya exista el proyecto, podés iniciar cada tarea con esta instrucción corta:

```txt
Mantené el rol definido en el Prompt Maestro de AuditShields.
Leé ROADMAP.md, PROMPTS_CODEX.md y AGENTS.md antes de modificar código.
Trabajá solo sobre el alcance de esta fase.
No agregues funcionalidades futuras si no están pedidas.
Antes de cambiar archivos, explicá brevemente qué vas a tocar.
```


---

## Cómo usar estos prompts

Usá un prompt por vez. No le pidas a Codex que haga todo el sistema completo de una sola vez.

Después de cada prompt:

1. Revisá qué archivos creó o modificó.
2. Ejecutá el proyecto.
3. Corregí errores.
4. Hacé commit.
5. Pasá al siguiente prompt.

Formato recomendado de commits:

```bash
git add .
git commit -m "feat: base project structure"
```


---

## Regla obligatoria para todos los prompts de fase

Antes de pegar cualquier prompt de fase, pegá primero el **Prompt Maestro** una vez por sesión. Si el repositorio ya tiene `AGENTS.md`, pedile a Codex que lo lea y respete sus instrucciones.

Cada prompt de fase debe interpretarse con estas restricciones:

- hacer solo lo pedido en esa fase;
- no agregar IA/ML, OCR, React, multi-tenant real ni integraciones externas;
- mantener Flask + Jinja + PostgreSQL;
- crear o actualizar tests cuando corresponda;
- mantener explicabilidad y trazabilidad en reglas antifraude;
- no romper módulos anteriores.

---

## Prompt 01 — Crear estructura base del monorepo

```txt
Quiero que crees la estructura inicial de un proyecto llamado AuditShields.

Contexto del producto:
AuditShields es una plataforma web antifraude y de auditoría continua para PyMEs. El MVP debe auditar compras/proveedores/pagos y stock/inventario. El sistema debe permitir cargar datos manualmente o por Excel/CSV, validar esos datos, ejecutar reglas claras antifraude, crear alertas, convertir cada alerta automáticamente en un caso de auditoría y permitir gestionar el caso hasta su normalización o cierre.

Stack decidido:
- Backend: Python + Flask
- Frontend: HTML/Jinja
- Base de datos: PostgreSQL
- ORM: SQLAlchemy
- Migraciones: Flask-Migrate/Alembic
- Estructura: monorepo
- Reportes: Excel
- IA/ML: no incluir todavía; primero reglas claras y explicables.

Creá esta estructura:

auditshields/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── extensions.py
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
├── .gitignore
└── README.md

Requisitos:
- No implementes todavía toda la lógica del sistema.
- Dejá archivos __init__.py donde corresponda.
- Agregá un README.md con descripción del producto, stack y comandos iniciales.
- Agregá un AGENTS.md en la raíz con las instrucciones persistentes del proyecto, usando el rol senior y las reglas del Prompt Maestro.
- Agregá .gitignore para Python, entornos virtuales, archivos .env, cachés, uploads e imports/exports.
- Agregá un .env.example con variables para Flask y PostgreSQL.
- Agregá un docker-compose.yml inicial con PostgreSQL y pgAdmin opcional.
- Mantené el código ordenado y preparado para crecer.
```

---

## Prompt 02 — Crear app Flask base con PostgreSQL

```txt
Sobre el proyecto AuditShields ya creado, implementá la app Flask base.

Requisitos técnicos:
- Usar patrón application factory.
- Crear create_app() en backend/app/__init__.py.
- Configurar SQLAlchemy.
- Configurar Flask-Migrate.
- Configurar Flask-Login para usar más adelante.
- Configurar variables desde .env.
- Crear backend/app/extensions.py con db, migrate y login_manager.
- Crear backend/app/config.py con clases Config, DevelopmentConfig y TestingConfig.
- Crear backend/run.py para ejecutar la app.
- Crear una ruta inicial / que renderice un template dashboard/index.html.
- Crear template base.html con navegación simple.
- Crear dashboard/index.html extendiendo base.html.
- Agregar requirements.txt con Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login, python-dotenv, psycopg2-binary, pandas, openpyxl.

No crees todavía modelos complejos. Solo dejá la base funcionando.

Criterios de aceptación:
- Puedo ejecutar Flask localmente.
- La app se conecta a PostgreSQL.
- La ruta / carga un dashboard inicial.
- La estructura queda limpia y modular.
```

---

## Prompt 03 — Crear modelos base y migraciones

```txt
Implementá los modelos base de AuditShields con SQLAlchemy y migraciones.

Contexto:
El MVP audita compras/proveedores/pagos y stock/inventario. Cada alerta antifraude debe crear automáticamente un caso de auditoría.

Crear modelos en backend/app/models/:

1. User
Campos:
- id
- name
- email único
- password_hash
- role: admin, auditor, readonly
- is_active
- created_at
- updated_at

2. Supplier
- id
- supplier_code único
- name
- tax_id
- bank_account
- address
- phone
- email
- created_date
- status
- created_at
- updated_at

3. PurchaseOrder
- id
- po_number único
- supplier_id FK
- requester_user_code
- approver_user_code
- order_date
- total_amount
- status
- created_at
- updated_at

4. Invoice
- id
- invoice_number
- supplier_id FK
- purchase_order_id FK nullable
- issue_date
- due_date
- total_amount
- status
- created_at
- updated_at

5. Payment
- id
- payment_number único
- supplier_id FK
- invoice_id FK nullable
- payment_date
- amount
- payment_method
- bank_account
- created_by_user_code
- created_at
- updated_at

6. Product
- id
- sku único
- name
- category
- unit_cost
- is_active
- created_at
- updated_at

7. InventorySnapshot
- id
- product_id FK
- snapshot_date
- expected_quantity
- physical_quantity
- difference_quantity
- created_at

8. StockMovement
- id
- product_id FK
- movement_type: IN, OUT, ADJUSTMENT, TRANSFER
- quantity
- movement_date
- reference
- reason
- created_by_user_code
- created_at

9. FraudRule
- id
- code único
- name
- module
- description
- risk_level_default
- is_active
- config_json
- created_at
- updated_at

10. Alert
- id
- rule_id FK
- module
- entity_type
- entity_id
- title
- description
- risk_score
- risk_level
- amount_at_risk
- evidence_json
- status
- fingerprint único
- created_at

11. Case
- id
- case_number único
- alert_id FK único
- title
- description
- risk_score
- risk_level
- status
- assigned_to_user_id FK nullable
- resolution_summary
- normalized_at
- closed_at
- created_at
- updated_at

12. CaseComment
- id
- case_id FK
- user_id FK
- comment
- created_at

13. CaseHistory
- id
- case_id FK
- user_id FK nullable
- action
- from_status
- to_status
- created_at

14. ImportLog
- id
- file_name
- file_type
- entity_type
- status
- total_rows
- imported_rows
- rejected_rows
- warnings_count
- errors_json
- created_by_user_id FK nullable
- created_at

15. AuditLog
- id
- user_id FK nullable
- action
- entity_type
- entity_id
- old_value
- new_value
- created_at

Requisitos:
- Usar relaciones SQLAlchemy donde corresponda.
- Usar Numeric para montos.
- Usar DateTime con default UTC.
- Crear __repr__ útil en modelos principales.
- Exportar modelos desde models/__init__.py.
- Generar migración inicial.

Criterios de aceptación:
- flask db migrate funciona.
- flask db upgrade crea todas las tablas en PostgreSQL.
- No hay imports circulares.
```

---

## Prompt 04 — Crear autenticación básica y roles

```txt
Implementá autenticación básica en AuditShields.

Requisitos:
- Usar Flask-Login.
- Agregar métodos necesarios al modelo User.
- Agregar password hashing con werkzeug.security.
- Crear blueprint auth.
- Rutas:
  - GET /login
  - POST /login
  - POST /logout
- Crear templates:
  - auth/login.html
- Crear decorador o helper para permisos por rol.
- Roles permitidos:
  - admin
  - auditor
  - readonly
- Proteger rutas principales con login_required.
- Crear seed/seed_users.py para crear usuario inicial:
  - email: admin@auditshields.local
  - password: admin123
  - role: admin
- Mostrar usuario logueado y rol en base.html.
- No permitir que readonly acceda a acciones POST de modificación.

Criterios de aceptación:
- Puedo iniciar sesión con el usuario seed.
- Puedo cerrar sesión.
- No puedo entrar al dashboard sin login.
- Se respetan permisos básicos por rol.
```

---

## Prompt 05 — Crear layout Jinja y navegación principal

```txt
Mejorá la UI base de AuditShields usando HTML/Jinja.

Requisitos:
- Crear un base.html limpio y profesional.
- Usar Bootstrap vía CDN o CSS propio simple.
- Crear barra lateral o navbar con secciones:
  - Dashboard
  - Importaciones
  - Proveedores
  - Órdenes de compra
  - Facturas
  - Pagos
  - Productos
  - Stock
  - Alertas
  - Casos
  - Reportes
  - Usuarios
- Crear templates placeholder para cada sección.
- Crear blueprints/rutas mínimas para cada sección.
- Mostrar flash messages.
- Mostrar estado de sesión.
- Mantener diseño claro para uso empresarial.

Criterios de aceptación:
- Todas las secciones principales existen.
- Todas extienden base.html.
- La navegación permite moverse por el sistema.
- La UI se ve ordenada aunque todavía tenga datos placeholder.
```

---

## Prompt 06 — CRUD de proveedores, órdenes, facturas y pagos

```txt
Implementá CRUD básico para el módulo compras/proveedores/pagos de AuditShields.

Entidades:
- Suppliers
- PurchaseOrders
- Invoices
- Payments

Requisitos:
- Crear listados con paginación simple.
- Crear formularios de alta.
- Crear vistas de detalle.
- Crear edición básica.
- No borrar físicamente registros críticos; usar status cuando tenga sentido.
- Validar campos obligatorios.
- Validar unicidad en supplier_code, po_number y payment_number.
- Permitir relacionar órdenes/facturas/pagos con proveedores.
- Permitir factura sin orden de compra, porque eso debe poder generar alerta luego.
- Permitir pago sin factura, porque eso debe poder generar alerta luego.
- Registrar acciones importantes en AuditLog.
- Respetar roles: readonly solo puede ver.

Criterios de aceptación:
- Puedo crear proveedores.
- Puedo crear órdenes de compra asociadas a proveedores.
- Puedo crear facturas asociadas a proveedores y opcionalmente a órdenes.
- Puedo crear pagos asociados a proveedores y opcionalmente a facturas.
- Los listados muestran datos reales de la base.
```

---

## Prompt 07 — CRUD de productos, stock y movimientos

```txt
Implementá el módulo de stock/inventario de AuditShields.

Entidades:
- Product
- InventorySnapshot
- StockMovement

Requisitos:
- Crear listados.
- Crear formularios de alta.
- Crear vistas de detalle de producto.
- En el detalle de producto mostrar snapshots y movimientos asociados.
- movement_type debe permitir: IN, OUT, ADJUSTMENT, TRANSFER.
- Validar cantidades.
- Permitir stock negativo temporalmente, porque luego una regla debe detectarlo.
- Registrar acciones importantes en AuditLog.
- Respetar readonly.

Criterios de aceptación:
- Puedo crear productos.
- Puedo registrar movimientos de stock.
- Puedo registrar snapshots de inventario.
- Puedo ver historial por producto.
```

---

## Prompt 08 — Crear plantillas Excel descargables

```txt
Implementá el servicio de plantillas Excel para AuditShields.

Requisitos:
- Crear backend/app/services/template_service.py.
- Generar plantillas .xlsx usando openpyxl.
- Crear endpoint GET /templates/<entity_type>/download.
- Entidades soportadas:
  - suppliers
  - purchase_orders
  - invoices
  - payments
  - products
  - inventory_snapshots
  - stock_movements
  - operational_users
- Cada plantilla debe tener:
  - encabezados claros;
  - una fila de ejemplo;
  - hoja llamada según entidad;
  - opcional: comentarios o notas sobre campos obligatorios.

Columnas sugeridas:

suppliers:
- supplier_code
- name
- tax_id
- bank_account
- address
- phone
- email
- created_date
- status

purchase_orders:
- po_number
- supplier_code
- requester_user_code
- approver_user_code
- order_date
- total_amount
- status

invoices:
- invoice_number
- supplier_code
- po_number
- issue_date
- due_date
- total_amount
- status

payments:
- payment_number
- supplier_code
- invoice_number
- payment_date
- amount
- payment_method
- bank_account
- created_by_user_code

products:
- sku
- name
- category
- unit_cost
- is_active

inventory_snapshots:
- sku
- snapshot_date
- expected_quantity
- physical_quantity

stock_movements:
- sku
- movement_type
- quantity
- movement_date
- reference
- reason
- created_by_user_code

Criterios de aceptación:
- El usuario puede descargar cada plantilla desde la UI.
- Las plantillas se abren correctamente en Excel.
- Las columnas coinciden con lo que luego se va a importar.
```

---

## Prompt 09 — Importación Excel/CSV con validaciones

```txt
Implementá importación Excel/CSV para AuditShields.

Requisitos:
- Crear backend/app/services/import_service.py.
- Crear backend/app/services/validation_service.py.
- Crear blueprint imports.
- Crear pantalla GET /imports.
- Crear pantalla GET /imports/new.
- Crear POST /imports/upload.
- Permitir elegir entity_type.
- Aceptar .xlsx y .csv.
- Leer archivos con pandas/openpyxl.
- Validar columnas obligatorias.
- Validar tipos de datos.
- Validar montos positivos.
- Validar fechas.
- Validar relaciones por códigos externos: supplier_code, po_number, invoice_number, sku.
- Insertar solo registros válidos.
- Registrar ImportLog con resumen.
- Mostrar errores por fila en pantalla.
- Guardar archivo original en data/imports o carpeta configurable.
- Respetar roles: readonly no puede importar.

Entidades mínimas a importar:
- suppliers
- purchase_orders
- invoices
- payments
- products
- inventory_snapshots
- stock_movements

Criterios de aceptación:
- Puedo importar un Excel válido.
- Puedo importar un CSV válido.
- Si faltan columnas, el sistema lo informa.
- Si hay errores por fila, el sistema los muestra.
- Los datos válidos se guardan.
- Se registra el historial de importación.
```

---

## Prompt 10 — Seeds de datos simulados

```txt
Creá datos simulados realistas para AuditShields.

Objetivo:
Necesito una demo que permita mostrar detección de fraude y fallas de control.

Crear script seed/seed_demo_data.py que genere:
- proveedores normales;
- proveedores con datos incompletos;
- dos proveedores con mismo bank_account;
- proveedores nuevos con pagos altos;
- órdenes de compra normales;
- órdenes con requester_user_code igual a approver_user_code;
- facturas normales;
- facturas duplicadas;
- facturas sin orden de compra;
- pagos normales;
- pagos duplicados;
- pagos sin factura;
- pagos fuera de horario;
- productos normales;
- movimientos de stock normales;
- ajustes manuales repetidos;
- stock negativo;
- diferencias entre stock esperado y físico.

Requisitos:
- El script debe poder ejecutarse varias veces sin duplicar datos innecesariamente, o debe limpiar datos demo antes de insertar.
- Documentar cómo ejecutarlo.
- Usar datos ficticios, no reales.

Criterios de aceptación:
- Después de correr el seed, el sistema tiene datos suficientes para que las reglas generen alertas.
```

---

## Prompt 11 — Motor antifraude base

```txt
Implementá el motor antifraude base de AuditShields.

Arquitectura requerida:
- backend/app/services/fraud_engine.py
- backend/app/services/purchase_rules.py
- backend/app/services/inventory_rules.py
- backend/app/services/case_service.py

Requisitos:
- FraudEngine debe ejecutar reglas activas.
- Cada regla debe devolver una lista de alertas candidatas.
- Cada alerta candidata debe incluir:
  - rule_code
  - module
  - entity_type
  - entity_id
  - title
  - description
  - risk_score
  - risk_level
  - amount_at_risk
  - evidence_json
  - fingerprint
- El fingerprint debe evitar duplicados.
- Al crear una alerta, crear automáticamente un Case asociado.
- Guardar Alert y Case en base de datos.
- Crear ruta POST /audit/run para ejecutar auditoría manual.
- Mostrar resultado: cantidad de alertas nuevas, duplicadas ignoradas y casos creados.

No implementar ML. Solo reglas claras.

Criterios de aceptación:
- Ejecutar auditoría genera alertas.
- Cada alerta genera un caso.
- Reejecutar auditoría no duplica alertas ya existentes.
- Cada alerta es explicable.
```

---

## Prompt 12 — Reglas antifraude de compras/proveedores/pagos

```txt
Implementá estas reglas en backend/app/services/purchase_rules.py.

Reglas:

R001 Pago duplicado exacto:
- mismo supplier_id;
- mismo invoice_id o mismo invoice_number cuando sea posible;
- mismo amount;
- fechas iguales o cercanas.

R002 Factura duplicada:
- mismo supplier_id;
- mismo invoice_number;
- mismo total_amount.

R003 Proveedores con misma cuenta bancaria:
- suppliers distintos con mismo bank_account no vacío.

R004 Proveedor nuevo con pagos altos:
- supplier.created_date dentro de últimos 30 días;
- suma de pagos mayor a umbral configurable.

R005 Pago/factura sin orden de compra:
- invoices con purchase_order_id null;
- payments asociados a facturas sin orden o payments sin factura.

R006 Compra fraccionada:
- varias purchase_orders del mismo proveedor;
- montos justo debajo de un límite configurable;
- dentro de ventana de días configurable.

R007 Aprobador igual al solicitante:
- purchase_orders donde requester_user_code == approver_user_code.

R008 Concentración excesiva en proveedor:
- proveedor concentra más de X% del total pagado en el período.

R009 Pago fuera de horario o día no laboral:
- payment_date fuera de horario laboral o fin de semana.

R010 Proveedor con datos incompletos:
- tax_id, bank_account, email o address faltantes.

Requisitos:
- Cada regla debe tener una función separada.
- Cada regla debe producir alertas con descriptions entendibles para un auditor.
- Usar score de riesgo simple de 0 a 100.
- Usar risk_level: low, medium, high, critical.
- Incluir evidence_json con los IDs y datos relevantes.

Criterios de aceptación:
- Con datos demo se activan varias reglas.
- Las alertas son claras y no genéricas.
```

---

## Prompt 13 — Reglas antifraude de stock/inventario

```txt
Implementá estas reglas en backend/app/services/inventory_rules.py.

Reglas:

S001 Ajustes manuales repetidos:
- muchos movimientos ADJUSTMENT para el mismo producto en una ventana de días.

S002 Stock negativo:
- calcular stock a partir de movimientos y detectar productos con stock menor a cero.

S003 Diferencia entre stock esperado y stock físico:
- inventory_snapshots donde abs(difference_quantity) supere umbral.

S004 Movimientos fuera de horario:
- stock_movements realizados fuera de horario laboral o fin de semana.

S005 Merma excesiva:
- movimientos OUT o ADJUSTMENT negativos que superen umbral por producto/categoría.

S006 Transferencias no conciliadas:
- movimientos TRANSFER con referencias que no tengan contraparte esperada.

S007 Usuario con demasiados ajustes:
- created_by_user_code con cantidad de ajustes superior al umbral.

S008 Productos críticos sin movimiento esperado:
- productos activos sin movimientos durante período configurable.

Requisitos:
- Cada regla debe tener función separada.
- Cada alerta debe ser explicable.
- Generar fingerprint para evitar duplicados.
- Integrar con FraudEngine.

Criterios de aceptación:
- Con datos demo se generan alertas de inventario.
- Las alertas crean casos automáticamente.
```

---

## Prompt 14 — Gestión de alertas y casos

```txt
Implementá las pantallas y acciones para alertas y casos en AuditShields.

Alertas:
- GET /alerts
- GET /alerts/<id>
- filtros por módulo, riesgo, estado y fecha.

Casos:
- GET /cases
- GET /cases/<id>
- POST /cases/<id>/status
- POST /cases/<id>/comments
- POST /cases/<id>/assign

Estados de caso:
- Nuevo
- En revisión
- Requiere documentación
- Observado
- En corrección
- Normalizado
- Falso positivo
- Confirmado
- Escalado
- Cerrado

Requisitos:
- En detalle de caso mostrar:
  - datos del caso;
  - alerta original;
  - regla activada;
  - evidencia JSON formateada;
  - comentarios;
  - historial;
  - formulario para comentar;
  - formulario para cambiar estado;
  - responsable asignado.
- Registrar cada cambio de estado en CaseHistory.
- Registrar comentarios en CaseComment.
- Registrar acciones críticas en AuditLog.
- readonly solo puede ver.

Criterios de aceptación:
- Puedo ver casos generados.
- Puedo revisar un caso.
- Puedo comentar.
- Puedo cambiar estados.
- Puedo normalizar y cerrar un caso.
- Queda historial de todo.
```

---

## Prompt 15 — Dashboard empresarial

```txt
Implementá el dashboard principal de AuditShields.

Debe mostrar métricas reales desde la base:
- total de alertas activas;
- total de casos abiertos;
- cantidad de casos críticos;
- monto total en riesgo;
- proveedores observados;
- productos observados;
- reglas más activadas;
- últimos casos generados;
- casos por estado;
- alertas por módulo.

Requisitos UI:
- Usar tarjetas resumen.
- Usar tablas simples para últimos casos y reglas más activadas.
- Mantener estilo empresarial, sobrio y claro.
- Permitir links rápidos a alertas y casos.
- No usar gráficos complejos todavía salvo que sea simple.

Criterios de aceptación:
- El dueño/encargado entiende rápido qué está pasando.
- Las métricas se actualizan con datos reales.
- Desde el dashboard puedo ir al detalle de casos críticos.
```

---

## Prompt 16 — Reportes Excel

```txt
Implementá reportes Excel para AuditShields.

Requisitos:
- Crear backend/app/services/report_service.py.
- Usar openpyxl o pandas ExcelWriter.
- Crear rutas:
  - GET /reports
  - GET /reports/cases.xlsx
  - GET /reports/alerts.xlsx
  - GET /reports/risk-summary.xlsx
- Permitir filtros básicos por fecha, módulo, riesgo y estado cuando sea posible.

Reportes:

1. Casos:
Columnas:
- case_number
- title
- module
- risk_level
- risk_score
- status
- assigned_to
- created_at
- closed_at
- resolution_summary

2. Alertas:
Columnas:
- rule_code
- rule_name
- module
- entity_type
- entity_id
- title
- risk_level
- risk_score
- amount_at_risk
- created_at

3. Resumen de riesgo:
Hojas:
- resumen general
- casos por estado
- alertas por regla
- monto en riesgo por proveedor
- productos observados

Criterios de aceptación:
- Los reportes se descargan correctamente.
- Los archivos abren en Excel.
- La información es útil para auditoría.
```

---

## Prompt 17 — Validaciones y manejo de errores

```txt
Mejorá validaciones y manejo de errores en AuditShields.

Requisitos:
- Crear páginas de error 403, 404 y 500.
- Mejorar mensajes flash.
- Validar formularios manuales.
- Validar importaciones con mensajes por fila.
- Evitar caídas por datos mal formateados.
- Agregar logs de aplicación.
- Agregar protección básica contra archivos no permitidos.
- Limitar extensiones a .xlsx y .csv en importación.
- Validar tamaño máximo de archivo.
- Evitar exposición de stack traces en modo producción.

Criterios de aceptación:
- El sistema informa errores de forma clara.
- Un archivo malo no rompe la aplicación.
- Un usuario sin permisos ve 403.
```

---

## Prompt 18 — Tests básicos

```txt
Agregá tests básicos para AuditShields.

Requisitos:
- Usar pytest.
- Crear configuración de testing.
- Tests mínimos:
  - app crea correctamente;
  - login correcto;
  - login incorrecto;
  - usuario sin login no accede a dashboard;
  - readonly no puede crear datos;
  - creación de supplier;
  - importación con columnas faltantes falla correctamente;
  - regla de pago duplicado genera alerta;
  - alerta crea caso automáticamente;
  - cambio de estado crea historial.

Criterios de aceptación:
- pytest corre sin errores.
- Los tests cubren el flujo crítico del MVP.
```

---

## Prompt 19 — Mejorar documentación

```txt
Mejorá la documentación del proyecto AuditShields.

Crear o actualizar:
- README.md
- docs/INSTALLATION.md
- docs/USER_GUIDE.md
- docs/DATABASE.md
- docs/RULES.md
- docs/DEMO_SCRIPT.md

Contenido esperado:

README.md:
- descripción del producto;
- stack;
- estructura de carpetas;
- instalación rápida;
- comandos útiles.

INSTALLATION.md:
- requisitos;
- variables de entorno;
- levantar PostgreSQL con Docker Compose;
- crear entorno virtual;
- instalar dependencias;
- ejecutar migraciones;
- crear usuario admin;
- cargar datos demo.

USER_GUIDE.md:
- login;
- cargar datos;
- descargar plantillas;
- importar Excel;
- ejecutar auditoría;
- revisar alertas;
- gestionar casos;
- exportar reportes.

DATABASE.md:
- explicar modelos principales y relaciones.

RULES.md:
- explicar cada regla R001-R010 y S001-S008.

DEMO_SCRIPT.md:
- paso a paso para mostrar el producto.

Criterios de aceptación:
- Alguien puede instalar y probar el proyecto siguiendo la documentación.
```

---

## Prompt 20 — Preparar demo final MVP

```txt
Prepará AuditShields para una demo final de MVP.

Objetivo:
Mostrar en 5 a 10 minutos cómo una PyME puede detectar riesgos antifraude y fallas de control.

Requisitos:
- Revisar que seed_demo_data.py genere alertas interesantes.
- Crear botón o comando para resetear demo.
- Mejorar dashboard para que tenga datos visibles.
- Asegurar que /audit/run genere alertas y casos.
- Asegurar que reportes Excel funcionen.
- Crear mensajes claros en UI.
- Crear docs/DEMO_SCRIPT.md con guion:
  1. Presentar problema.
  2. Mostrar carga de datos.
  3. Ejecutar auditoría.
  4. Mostrar alertas.
  5. Abrir caso crítico.
  6. Comentar/cambiar estado.
  7. Marcar como normalizado.
  8. Exportar Excel.
  9. Cerrar con valor para la empresa.

Criterios de aceptación:
- La demo puede ejecutarse desde cero.
- El flujo se entiende sin explicar demasiado código.
- El proyecto queda presentable para portfolio, tesis o validación comercial.
```

---

# Prompts de corrección útiles

## Corregir errores sin romper arquitectura

```txt
Estoy trabajando en AuditShields, una app Flask con SQLAlchemy, PostgreSQL y Jinja. Revisá el error actual y corregilo respetando la arquitectura existente.

Reglas:
- No mezcles lógica de negocio en templates.
- No elimines modelos ni migraciones sin explicar.
- No cambies el stack.
- No agregues IA/ML.
- Mantené rutas, servicios y modelos separados.
- Si hay que cambiar la base, generá o indicá migración.
- Explicá brevemente qué cambiaste y por qué.

Error:
[PEGAR ERROR COMPLETO]
```

---

## Pedir refactor de código

```txt
Refactorizá este módulo de AuditShields para que quede más limpio y mantenible.

Objetivo:
- Separar responsabilidades.
- Mantener compatibilidad con la app actual.
- Mejorar nombres.
- Evitar duplicación.
- Mantener lógica de negocio en services.
- Mantener templates solo para presentación.

No cambies comportamiento funcional salvo que encuentres un bug evidente. Si encontrás un bug, explicalo antes de corregirlo.

Archivo o código:
[PEGAR CÓDIGO]
```

---

## Pedir una regla antifraude nueva

```txt
Agregá una nueva regla antifraude a AuditShields.

Contexto:
El sistema usa FraudEngine, reglas separadas por módulo, Alert, Case y fingerprint para evitar duplicados. Cada alerta debe crear un caso automáticamente.

Nueva regla:
[NOMBRE Y DESCRIPCIÓN]

Requisitos:
- Crear función separada.
- Generar rule_code único.
- Generar title y description explicables.
- Calcular risk_score 0-100.
- Asignar risk_level.
- Incluir evidence_json.
- Crear fingerprint estable.
- Integrarla al FraudEngine.
- Agregar datos demo si hace falta.
- Agregar test básico si ya existe estructura de tests.
```

---

## Pedir mejora visual

```txt
Mejorá la interfaz de esta pantalla de AuditShields manteniendo HTML/Jinja.

Objetivo visual:
- Estilo empresarial.
- Claro, sobrio y fácil de usar.
- Priorizar tablas, filtros y acciones visibles.
- No usar React.
- No agregar dependencias pesadas.

Pantalla:
[PEGAR TEMPLATE O DESCRIBIR RUTA]

Requisitos:
- Mantener extends de base.html.
- Mantener variables Jinja existentes.
- Mejorar layout, encabezados, botones, estados y mensajes.
- No romper rutas existentes.
```

---

# Orden recomendado de ejecución

1. Prompt 01 — Estructura.
2. Prompt 02 — Flask base.
3. Prompt 03 — Modelos y migraciones.
4. Prompt 04 — Login y roles.
5. Prompt 05 — Layout y navegación.
6. Prompt 06 — CRUD compras/proveedores/pagos.
7. Prompt 07 — CRUD stock.
8. Prompt 08 — Plantillas Excel.
9. Prompt 09 — Importación Excel/CSV.
10. Prompt 10 — Datos demo.
11. Prompt 11 — Motor antifraude.
12. Prompt 12 — Reglas compras/pagos.
13. Prompt 13 — Reglas stock.
14. Prompt 14 — Alertas y casos.
15. Prompt 15 — Dashboard.
16. Prompt 16 — Reportes Excel.
17. Prompt 17 — Validaciones y errores.
18. Prompt 18 — Tests.
19. Prompt 19 — Documentación.
20. Prompt 20 — Demo final.

---

# Recordatorio de alcance

No incluir todavía:

- Machine learning.
- OCR.
- React.
- Multi-tenant real.
- App móvil.
- APIs externas.
- Reportes PDF.
- Integraciones ERP.

Primero construir un MVP robusto, explicable y demostrable.

