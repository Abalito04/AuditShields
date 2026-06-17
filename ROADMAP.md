# ROADMAP.md — AuditShields

> Nombre provisional: **AuditShields**  
> Tipo de producto: SaaS antifraude y auditoría continua para PyMEs  
> Stack inicial: **Python + Flask + HTML/Jinja + PostgreSQL**  
> Enfoque MVP: **compras/proveedores/pagos + stock/inventario**  
> Horizonte estimado: **3 a 6 meses**

---

## 1. Visión del producto

AuditShields será una plataforma web para ayudar a dueños, encargados y auditores de PyMEs a encontrar fraudes, errores operativos, fallas de control interno y problemas de trazabilidad.

La idea central no es acusar personas automáticamente, sino detectar **señales de riesgo**, generar **casos de auditoría**, permitir investigarlos y acompañar el proceso hasta que la situación quede **normalizada, corregida o cerrada**.

### Frase guía del producto

> “AuditShields no reemplaza al auditor: le muestra dónde mirar primero.”

---

## 2. Decisiones iniciales confirmadas

| Área | Decisión |
|---|---|
| Nombre | AuditShields, provisional |
| Tipo | SaaS, pero inicialmente para una sola PyME por instalación |
| Cliente objetivo | PyMEs de cualquier rubro que necesiten control antifraude |
| Usuarios principales | Dueño, encargado, auditor, usuario de solo lectura |
| Módulos MVP | Compras/proveedores/pagos y stock/inventario |
| Datos iniciales | Manual, Excel y CSV |
| Datos de prueba | Simulados |
| Plantillas descargables | Sí |
| Validación de archivos | Sí |
| Backend | Flask |
| Frontend | HTML/Jinja |
| Base de datos | PostgreSQL |
| Docker | Recomendado desde el inicio para PostgreSQL y servicios auxiliares |
| IA/ML | No en MVP; primero reglas claras y explicables |
| Reportes | Exportación Excel en MVP |
| Login/roles | Básico en MVP |
| Roles iniciales | Admin, Auditor, Solo lectura |
| Alertas | Cada alerta crea automáticamente un caso |
| Estructura | Monorepo |

---

## 3. Recomendación sobre Docker

Usar Docker desde el inicio, pero de forma progresiva:

### Fase inicial

- PostgreSQL en Docker Compose.
- Opcional: pgAdmin en Docker Compose.
- Flask corriendo localmente con entorno virtual.

### Fase intermedia

- Flask también dentro de Docker.
- Variables de entorno centralizadas.
- Volúmenes para archivos importados y reportes.

### Fase avanzada

- Docker Compose completo:
  - `web`
  - `postgres`
  - `pgadmin`
  - `worker`, si se agregan tareas pesadas
  - `redis`, si se agregan colas

Esta estrategia evita bloquear el avance al principio, pero deja el proyecto preparado para despliegue profesional.

---

## 4. Alcance del MVP

El MVP debe demostrar un flujo completo de auditoría:

1. El usuario inicia sesión.
2. Carga datos manualmente o mediante Excel/CSV.
3. El sistema valida los datos.
4. El sistema ejecuta reglas antifraude.
5. Se crean alertas automáticamente.
6. Cada alerta crea un caso de auditoría.
7. El auditor revisa el caso.
8. El auditor agrega comentarios, estados y acciones.
9. El caso se cierra cuando se confirma, descarta o normaliza.
10. El sistema permite exportar reportes en Excel.

---

## 5. Fuera del MVP

Estas funciones quedan para fases posteriores:

- Machine learning.
- OCR de facturas/remitos.
- Integración con ERP real.
- Multi-tenant completo.
- App móvil.
- Notificaciones por WhatsApp.
- Firma digital de casos.
- Reportes PDF avanzados.
- Dashboard con gráficos complejos.
- Integración con cámaras.
- Auditoría con IA generativa.

---

## 6. Módulos funcionales

## 6.1. Autenticación y roles

### Objetivo

Permitir acceso básico y separación de permisos.

### Roles iniciales

#### Admin

Puede:

- crear usuarios;
- cargar datos;
- ejecutar auditorías;
- ver todos los casos;
- cambiar estados;
- exportar reportes;
- administrar catálogos y reglas.

#### Auditor

Puede:

- cargar datos;
- ejecutar auditorías;
- revisar casos;
- comentar casos;
- cambiar estados de casos;
- exportar reportes.

#### Solo lectura

Puede:

- ver dashboards;
- ver alertas;
- ver casos;
- exportar reportes si se habilita;
- no puede modificar datos.

---

## 6.2. Carga de datos

### Métodos iniciales

- Carga manual desde formularios.
- Importación desde Excel.
- Importación desde CSV.

### Entidades cargables en MVP

- Proveedores.
- Facturas.
- Pagos.
- Órdenes de compra.
- Productos.
- Stock actual.
- Movimientos de stock.
- Usuarios/aprobadores operativos.

### Plantillas descargables

El sistema debe permitir descargar plantillas para:

- `proveedores.xlsx`
- `facturas.xlsx`
- `pagos.xlsx`
- `ordenes_compra.xlsx`
- `productos.xlsx`
- `stock_actual.xlsx`
- `movimientos_stock.xlsx`
- `usuarios_operativos.xlsx`

---

## 6.3. Validación de datos

### Validaciones generales

- Columnas obligatorias presentes.
- Tipos de datos correctos.
- Fechas válidas.
- Montos positivos.
- Identificadores no vacíos.
- Duplicados evidentes.
- Relaciones existentes.
- Campos críticos incompletos.

### Resultado de la validación

Cada importación debe generar un resultado:

- registros válidos;
- registros rechazados;
- errores por fila;
- advertencias;
- resumen final.

Ejemplo:

```txt
Archivo: pagos.xlsx
Registros procesados: 1.250
Importados: 1.180
Rechazados: 70
Advertencias: 43
```

---

## 6.4. Motor de reglas antifraude

### Principio clave

El MVP debe usar reglas claras, trazables y explicables. Cada alerta debe indicar qué regla se activó y por qué.

### Reglas para compras/proveedores/pagos

#### R001 — Pago duplicado exacto

Detecta pagos con:

- mismo proveedor;
- mismo número de factura;
- mismo monto;
- misma fecha o fechas cercanas.

#### R002 — Factura duplicada

Detecta facturas con:

- mismo proveedor;
- mismo número de factura;
- mismo importe.

#### R003 — Proveedor con datos bancarios compartidos

Detecta proveedores diferentes con mismo CBU/CVU/cuenta bancaria.

#### R004 — Proveedor nuevo con pagos altos

Detecta proveedores creados recientemente que reciben pagos altos en poco tiempo.

Umbral inicial sugerido:

- proveedor creado hace menos de 30 días;
- pagos acumulados mayores a un monto configurable.

#### R005 — Pago sin orden de compra asociada

Detecta pagos o facturas sin orden de compra vinculada.

#### R006 — Compra fraccionada

Detecta varias compras similares justo por debajo del límite de aprobación.

Ejemplo:

- límite de aprobación: $500.000;
- múltiples compras entre $450.000 y $499.999;
- mismo proveedor;
- período corto.

#### R007 — Aprobador igual al solicitante

Detecta órdenes donde la persona que solicita también aprueba.

#### R008 — Concentración excesiva en proveedor

Detecta proveedores que concentran un porcentaje demasiado alto del gasto.

#### R009 — Pago fuera de horario o día no laboral

Detecta pagos registrados fuera del horario normal.

#### R010 — Proveedor con datos incompletos

Detecta proveedores sin CUIT, domicilio, contacto, cuenta bancaria o documentación mínima.

---

### Reglas para stock/inventario

#### S001 — Ajustes manuales repetidos

Detecta productos con muchos ajustes manuales en poco tiempo.

#### S002 — Stock negativo

Detecta productos cuyo stock queda por debajo de cero.

#### S003 — Diferencia entre stock esperado y stock real

Detecta diferencias entre stock calculado y stock físico declarado.

#### S004 — Movimientos fuera de horario

Detecta entradas, salidas o ajustes realizados fuera de horario normal.

#### S005 — Producto con merma excesiva

Detecta productos con pérdidas superiores al umbral esperado.

#### S006 — Transferencias no conciliadas

Detecta transferencias entre depósitos/sucursales donde la salida no coincide con la entrada.

#### S007 — Usuario con demasiados ajustes

Detecta usuarios que realizan más ajustes de stock que el promedio.

#### S008 — Productos críticos sin movimiento esperado

Detecta productos que deberían moverse, pero no registran movimientos.

---

## 6.5. Scoring de riesgo

Cada alerta debe tener un score simple y explicable.

### Niveles sugeridos

| Score | Nivel |
|---:|---|
| 0 - 29 | Bajo |
| 30 - 59 | Medio |
| 60 - 79 | Alto |
| 80 - 100 | Crítico |

### Factores de score

- Monto involucrado.
- Repetición.
- Usuario involucrado.
- Antigüedad del proveedor.
- Falta de documentación.
- Impacto en stock.
- Reincidencia.
- Coincidencias con otras alertas.

---

## 6.6. Alertas y casos

### Regla de negocio confirmada

Cada alerta crea automáticamente un caso de auditoría.

### Estados de caso sugeridos

- Nuevo.
- En revisión.
- Requiere documentación.
- Observado.
- En corrección.
- Normalizado.
- Falso positivo.
- Confirmado.
- Escalado.
- Cerrado.

### Flujo recomendado

```txt
Alerta detectada
   ↓
Caso nuevo
   ↓
En revisión
   ↓
Requiere documentación / Observado / Falso positivo
   ↓
En corrección
   ↓
Normalizado
   ↓
Cerrado
```

### Información mínima del caso

- Código de caso.
- Regla que lo generó.
- Nivel de riesgo.
- Entidad afectada.
- Monto involucrado.
- Descripción.
- Evidencia.
- Estado.
- Usuario asignado.
- Comentarios.
- Historial.
- Fecha de creación.
- Fecha de cierre.

---

## 6.7. Dashboard

### Dashboard MVP

Debe mostrar:

- total de alertas activas;
- total de casos abiertos;
- casos críticos;
- monto total en riesgo;
- proveedores observados;
- productos con riesgo;
- reglas más activadas;
- últimos casos generados;
- casos por estado;
- alertas por módulo.

### Pantallas mínimas

- Login.
- Inicio/Dashboard.
- Proveedores.
- Facturas.
- Pagos.
- Órdenes de compra.
- Productos.
- Stock.
- Importaciones.
- Alertas.
- Casos.
- Detalle de caso.
- Reglas.
- Usuarios.
- Reportes.

---

## 6.8. Reportes Excel

### Reportes MVP

- Casos abiertos.
- Casos cerrados.
- Alertas por período.
- Proveedores observados.
- Productos observados.
- Pagos duplicados posibles.
- Ajustes de stock sospechosos.
- Resumen ejecutivo en Excel.

---

## 7. Modelo de datos inicial

## 7.1. Tablas de seguridad

### users

- id
- name
- email
- password_hash
- role
- is_active
- created_at
- updated_at

### audit_logs

- id
- user_id
- action
- entity_type
- entity_id
- old_value
- new_value
- created_at

---

## 7.2. Tablas de compras/proveedores/pagos

### suppliers

- id
- supplier_code
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

### purchase_orders

- id
- po_number
- supplier_id
- requester_user_code
- approver_user_code
- order_date
- total_amount
- status
- created_at
- updated_at

### invoices

- id
- invoice_number
- supplier_id
- purchase_order_id
- issue_date
- due_date
- total_amount
- status
- created_at
- updated_at

### payments

- id
- payment_number
- supplier_id
- invoice_id
- payment_date
- amount
- payment_method
- bank_account
- created_by_user_code
- created_at
- updated_at

---

## 7.3. Tablas de stock/inventario

### products

- id
- sku
- name
- category
- unit_cost
- is_active
- created_at
- updated_at

### inventory_snapshots

- id
- product_id
- snapshot_date
- expected_quantity
- physical_quantity
- difference_quantity
- created_at

### stock_movements

- id
- product_id
- movement_type
- quantity
- movement_date
- reference
- reason
- created_by_user_code
- created_at

---

## 7.4. Tablas de auditoría antifraude

### fraud_rules

- id
- code
- name
- module
- description
- risk_level_default
- is_active
- config_json
- created_at
- updated_at

### alerts

- id
- rule_id
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
- created_at

### cases

- id
- case_number
- alert_id
- title
- description
- risk_score
- risk_level
- status
- assigned_to_user_id
- resolution_summary
- normalized_at
- closed_at
- created_at
- updated_at

### case_comments

- id
- case_id
- user_id
- comment
- created_at

### case_history

- id
- case_id
- user_id
- action
- from_status
- to_status
- created_at

### imports

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
- created_by_user_id
- created_at

---

## 8. Estructura de carpetas recomendada

```txt
auditshields/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── extensions.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── supplier.py
│   │   │   ├── purchase_order.py
│   │   │   ├── invoice.py
│   │   │   ├── payment.py
│   │   │   ├── product.py
│   │   │   ├── stock_movement.py
│   │   │   ├── fraud_rule.py
│   │   │   ├── alert.py
│   │   │   ├── case.py
│   │   │   └── import_log.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── dashboard.py
│   │   │   ├── imports.py
│   │   │   ├── suppliers.py
│   │   │   ├── purchases.py
│   │   │   ├── inventory.py
│   │   │   ├── alerts.py
│   │   │   ├── cases.py
│   │   │   ├── reports.py
│   │   │   └── users.py
│   │   ├── services/
│   │   │   ├── import_service.py
│   │   │   ├── validation_service.py
│   │   │   ├── template_service.py
│   │   │   ├── fraud_engine.py
│   │   │   ├── purchase_rules.py
│   │   │   ├── inventory_rules.py
│   │   │   ├── case_service.py
│   │   │   ├── report_service.py
│   │   │   └── audit_log_service.py
│   │   ├── templates/
│   │   │   ├── base.html
│   │   │   ├── auth/
│   │   │   ├── dashboard/
│   │   │   ├── imports/
│   │   │   ├── suppliers/
│   │   │   ├── purchases/
│   │   │   ├── inventory/
│   │   │   ├── alerts/
│   │   │   ├── cases/
│   │   │   └── reports/
│   │   ├── static/
│   │   │   ├── css/
│   │   │   ├── js/
│   │   │   └── img/
│   │   └── utils/
│   │       ├── dates.py
│   │       ├── money.py
│   │       └── files.py
│   ├── migrations/
│   ├── tests/
│   ├── seed/
│   │   ├── seed_users.py
│   │   ├── seed_rules.py
│   │   └── seed_demo_data.py
│   ├── requirements.txt
│   ├── run.py
│   └── .env.example
├── data/
│   ├── samples/
│   ├── templates/
│   ├── imports/
│   └── exports/
├── docs/
│   ├── ROADMAP.md
│   ├── PROMPTS_CODEX.md
│   ├── DATABASE.md
│   ├── RULES.md
│   └── USER_FLOWS.md
├── scripts/
│   ├── init_db.sh
│   └── reset_demo_data.sh
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 9. Rutas Flask sugeridas

### Auth

- `GET /login`
- `POST /login`
- `POST /logout`

### Dashboard

- `GET /`
- `GET /dashboard`

### Importaciones

- `GET /imports`
- `GET /imports/new`
- `POST /imports/upload`
- `GET /imports/<id>`
- `GET /templates/<entity_type>/download`

### Compras/proveedores/pagos

- `GET /suppliers`
- `GET /suppliers/new`
- `POST /suppliers`
- `GET /suppliers/<id>`
- `GET /purchase-orders`
- `GET /invoices`
- `GET /payments`

### Inventario

- `GET /products`
- `GET /stock`
- `GET /stock/movements`
- `GET /stock/snapshots`

### Auditoría

- `POST /audit/run`
- `GET /alerts`
- `GET /alerts/<id>`
- `GET /cases`
- `GET /cases/<id>`
- `POST /cases/<id>/status`
- `POST /cases/<id>/comments`
- `POST /cases/<id>/assign`

### Reportes

- `GET /reports`
- `GET /reports/cases.xlsx`
- `GET /reports/alerts.xlsx`
- `GET /reports/risk-summary.xlsx`

---

## 10. Roadmap por fases

## Fase 0 — Definición y preparación técnica

Duración estimada: 1 semana.

### Objetivo

Dejar clara la visión, la arquitectura y el entorno base.

### Tareas

- Crear repositorio Git.
- Crear estructura monorepo.
- Crear `README.md` inicial.
- Crear `docker-compose.yml` con PostgreSQL.
- Crear `.env.example`.
- Crear entorno Flask.
- Configurar SQLAlchemy.
- Configurar Flask-Migrate/Alembic.
- Crear layout base HTML/Jinja.
- Crear navegación principal.

### Criterios de aceptación

- El proyecto levanta localmente.
- PostgreSQL corre con Docker Compose.
- Flask se conecta a PostgreSQL.
- Existe una página inicial funcional.
- Existe documentación mínima en `/docs`.

---

## Fase 1 — Usuarios, roles y base administrativa

Duración estimada: 2 semanas.

### Objetivo

Tener login básico, roles y protección de rutas.

### Tareas

- Crear modelo `User`.
- Crear roles: Admin, Auditor, Solo lectura.
- Implementar login/logout.
- Hashear contraseñas.
- Crear usuario admin inicial por seed.
- Proteger rutas por login.
- Crear decoradores de permisos por rol.
- Crear CRUD básico de usuarios.
- Crear audit log básico.

### Criterios de aceptación

- Un usuario puede iniciar sesión.
- Un usuario puede cerrar sesión.
- Las rutas privadas no son visibles sin login.
- Admin puede crear usuarios.
- Solo lectura no puede modificar datos.
- Las acciones críticas se registran en auditoría.

---

## Fase 2 — Modelo de datos de compras/proveedores/pagos

Duración estimada: 2 a 3 semanas.

### Objetivo

Construir el núcleo de datos del primer módulo antifraude.

### Tareas

- Crear modelos:
  - Supplier.
  - PurchaseOrder.
  - Invoice.
  - Payment.
- Crear migraciones.
- Crear vistas/listados.
- Crear formularios de alta manual.
- Crear detalle por proveedor.
- Crear detalle por factura.
- Crear detalle por pago.
- Crear filtros simples.
- Crear datos simulados.

### Criterios de aceptación

- Se pueden crear proveedores manualmente.
- Se pueden crear órdenes, facturas y pagos.
- Las relaciones quedan correctamente guardadas.
- Se puede navegar desde proveedor a facturas/pagos.
- Existe dataset demo cargable.

---

## Fase 3 — Importación Excel/CSV y plantillas

Duración estimada: 3 semanas.

### Objetivo

Permitir carga masiva de datos con validaciones robustas.

### Tareas

- Crear servicio de plantillas Excel.
- Crear plantilla para proveedores.
- Crear plantilla para órdenes de compra.
- Crear plantilla para facturas.
- Crear plantilla para pagos.
- Crear pantalla de importación.
- Procesar Excel/CSV con Pandas/OpenPyXL.
- Validar columnas obligatorias.
- Validar tipos de datos.
- Validar relaciones.
- Registrar importaciones.
- Mostrar errores por fila.
- Permitir descargar reporte de errores.

### Criterios de aceptación

- El usuario puede descargar plantillas.
- El usuario puede subir Excel/CSV.
- El sistema valida datos antes de insertarlos.
- El sistema informa errores por fila.
- Los registros válidos se importan.
- Los registros inválidos no rompen el proceso.

---

## Fase 4 — Motor de reglas para compras/proveedores/pagos

Duración estimada: 3 a 4 semanas.

### Objetivo

Detectar alertas antifraude explicables en compras, proveedores y pagos.

### Tareas

- Crear modelo `FraudRule`.
- Crear modelo `Alert`.
- Crear servicio `fraud_engine.py`.
- Crear reglas R001 a R010.
- Crear score de riesgo básico.
- Crear descripción explicable por alerta.
- Crear pantalla de alertas.
- Crear ejecución manual de auditoría.
- Evitar duplicación de alertas ya existentes.

### Criterios de aceptación

- El usuario puede ejecutar auditoría.
- El sistema genera alertas reales sobre datos demo.
- Cada alerta indica regla, motivo, entidad y score.
- Las alertas quedan persistidas.
- No se duplican alertas innecesariamente.

---

## Fase 5 — Casos de auditoría y normalización

Duración estimada: 3 semanas.

### Objetivo

Convertir alertas en casos gestionables hasta su cierre.

### Tareas

- Crear modelo `Case`.
- Crear modelo `CaseComment`.
- Crear modelo `CaseHistory`.
- Crear caso automáticamente por cada alerta.
- Crear listado de casos.
- Crear detalle de caso.
- Cambiar estado del caso.
- Agregar comentarios.
- Asignar responsable.
- Registrar historial.
- Permitir marcar como normalizado.
- Permitir cerrar caso.

### Criterios de aceptación

- Cada alerta crea un caso automáticamente.
- El auditor puede revisar el caso.
- El auditor puede cambiar estados.
- El auditor puede agregar comentarios.
- El historial queda registrado.
- El caso puede cerrarse solo después de una resolución.

---

## Fase 6 — Módulo de stock/inventario

Duración estimada: 4 semanas.

### Objetivo

Agregar auditoría de inventario, ajustes y movimientos sospechosos.

### Tareas

- Crear modelos:
  - Product.
  - InventorySnapshot.
  - StockMovement.
- Crear formularios manuales.
- Crear plantillas Excel.
- Crear importación de productos.
- Crear importación de stock actual.
- Crear importación de movimientos.
- Crear reglas S001 a S008.
- Integrar alertas de stock con casos.
- Crear vistas de productos observados.

### Criterios de aceptación

- Se pueden cargar productos.
- Se puede cargar stock actual.
- Se pueden cargar movimientos.
- El sistema detecta diferencias y ajustes sospechosos.
- Las alertas de stock crean casos.

---

## Fase 7 — Dashboard y reportes Excel

Duración estimada: 2 a 3 semanas.

### Objetivo

Dar visibilidad clara al dueño/encargado/auditor.

### Tareas

- Crear dashboard principal.
- Crear métricas:
  - casos abiertos;
  - alertas críticas;
  - monto en riesgo;
  - proveedores observados;
  - productos observados;
  - casos por estado;
  - reglas más activadas.
- Crear exportación Excel de casos.
- Crear exportación Excel de alertas.
- Crear exportación Excel de resumen de riesgo.
- Crear filtros por fecha, módulo, estado y riesgo.

### Criterios de aceptación

- El dashboard muestra información real.
- El usuario puede filtrar casos y alertas.
- El usuario puede exportar Excel.
- El reporte Excel es entendible y útil.

---

## Fase 8 — Pulido, tests y preparación de demo

Duración estimada: 3 a 4 semanas.

### Objetivo

Convertir el MVP en una demo sólida y presentable.

### Tareas

- Crear datos simulados realistas.
- Crear escenarios de fraude simulados.
- Mejorar UI.
- Agregar mensajes de error claros.
- Agregar tests básicos.
- Validar permisos.
- Revisar migraciones.
- Revisar seguridad básica.
- Crear guía de instalación.
- Crear guía de uso.
- Crear video/demo script.

### Criterios de aceptación

- El proyecto se instala desde cero siguiendo documentación.
- La demo muestra casos reales detectados.
- Los permisos funcionan.
- Los reportes funcionan.
- El flujo completo se puede presentar sin intervención manual rara.

---

## 11. Plan temporal sugerido

## Plan de 3 meses, intensivo

| Mes | Objetivo |
|---|---|
| Mes 1 | Base técnica, usuarios, modelo de compras, importaciones |
| Mes 2 | Motor de reglas, alertas, casos, normalización |
| Mes 3 | Stock, dashboard, reportes, demo, tests básicos |

## Plan de 6 meses, más realista

| Mes | Objetivo |
|---|---|
| Mes 1 | Base técnica, usuarios, arquitectura, datos simulados |
| Mes 2 | Compras/proveedores/pagos + importaciones |
| Mes 3 | Reglas antifraude + alertas + casos |
| Mes 4 | Stock/inventario + reglas de stock |
| Mes 5 | Dashboard + reportes Excel + validaciones avanzadas |
| Mes 6 | Pulido, tests, seguridad, demo, documentación |

Recomendación: planificarlo como proyecto de **6 meses**, pero con un MVP demostrable al mes 3.

---

## 12. Checklist general

## Base técnica

- [ ] Crear repositorio.
- [ ] Crear monorepo.
- [ ] Crear entorno Flask.
- [ ] Configurar PostgreSQL.
- [ ] Configurar Docker Compose.
- [ ] Configurar SQLAlchemy.
- [ ] Configurar migraciones.
- [ ] Crear layout base.

## Seguridad

- [ ] Login.
- [ ] Logout.
- [ ] Roles.
- [ ] Permisos.
- [ ] Hash de contraseñas.
- [ ] Audit logs.

## Datos

- [ ] Proveedores.
- [ ] Facturas.
- [ ] Pagos.
- [ ] Órdenes de compra.
- [ ] Productos.
- [ ] Stock.
- [ ] Movimientos.

## Importaciones

- [ ] Plantillas Excel.
- [ ] Carga Excel.
- [ ] Carga CSV.
- [ ] Validación por fila.
- [ ] Log de importación.
- [ ] Reporte de errores.

## Antifraude

- [ ] Reglas de compras.
- [ ] Reglas de pagos.
- [ ] Reglas de proveedores.
- [ ] Reglas de stock.
- [ ] Score de riesgo.
- [ ] Alertas.
- [ ] Casos automáticos.

## Gestión de casos

- [ ] Listado.
- [ ] Detalle.
- [ ] Estados.
- [ ] Comentarios.
- [ ] Historial.
- [ ] Asignación.
- [ ] Normalización.
- [ ] Cierre.

## Reportes

- [ ] Exportar casos Excel.
- [ ] Exportar alertas Excel.
- [ ] Exportar resumen Excel.
- [ ] Filtros.

## Demo

- [ ] Datos demo.
- [ ] Casos demo.
- [ ] Guía de instalación.
- [ ] Guía de uso.
- [ ] Script de presentación.

---

## 13. Reglas de calidad para el desarrollo

- No crear código gigante en un solo archivo.
- Separar modelos, rutas, servicios y templates.
- Cada regla antifraude debe tener una función propia.
- Cada alerta debe ser explicable.
- No borrar datos críticos; usar estados.
- Toda acción importante debe quedar en `audit_logs`.
- No mezclar lógica de negocio dentro de templates.
- No depender de datos reales para la demo.
- Mantener `.env.example` actualizado.
- Mantener migraciones limpias.
- Documentar cada decisión importante.

---

## 14. Prioridad de desarrollo

Orden recomendado:

1. Base Flask + PostgreSQL.
2. Login y roles.
3. Modelos de compras/proveedores/pagos.
4. Importación Excel/CSV.
5. Plantillas descargables.
6. Motor de reglas.
7. Alertas.
8. Casos.
9. Stock/inventario.
10. Dashboard.
11. Reportes Excel.
12. Tests y demo.

---

## 15. Riesgos técnicos

| Riesgo | Mitigación |
|---|---|
| Querer hacer demasiados módulos al mismo tiempo | Priorizar compras/pagos antes de stock avanzado |
| Datos mal cargados | Validaciones fuertes e informes de error |
| Alertas duplicadas | Crear fingerprints por regla + entidad + período |
| Falsos positivos | Estados de caso y explicación clara |
| Proyecto difícil de mantener | Arquitectura por servicios y módulos |
| Base de datos desordenada | Migraciones y modelos claros desde el inicio |
| UI poco usable | Priorizar tablas, filtros y detalle de caso |
| Falta de demo convincente | Crear datos simulados con escenarios de fraude |

---

## 16. Decisiones pendientes para fases futuras

- Si el SaaS será multi-tenant real.
- Si se agregará IA/ML.
- Si se integrará OCR.
- Si se integrará con sistemas ERP.
- Si se crearán reportes PDF.
- Si se agregarán notificaciones.
- Si habrá API pública.
- Si se agregará app móvil.
- Si se agregará módulo de RRHH.
- Si se agregará módulo de POS/caja.

---

## 17. Definición de éxito del MVP

El MVP se considera exitoso si permite demostrar este escenario:

1. Se cargan datos simulados de una PyME.
2. El sistema detecta pagos duplicados, proveedores sospechosos y diferencias de stock.
3. Se generan alertas automáticamente.
4. Cada alerta crea un caso.
5. El auditor revisa los casos.
6. El auditor marca algunos como falso positivo, otros como confirmados y otros como normalizados.
7. El dueño ve un dashboard con monto en riesgo y casos abiertos.
8. Se exporta un Excel con el resumen de auditoría.

---

## 18. Próximo paso inmediato

Crear el repositorio y ejecutar los prompts iniciales de `PROMPTS_CODEX.md` en este orden:

1. Prompt 01 — Crear estructura base del monorepo.
2. Prompt 02 — Crear backend Flask con PostgreSQL.
3. Prompt 03 — Crear modelos base y migraciones.
4. Prompt 04 — Crear autenticación básica y roles.
5. Prompt 05 — Crear layout Jinja y dashboard inicial.

---

## 24. Instrucciones persistentes para agentes de código

Además de este roadmap y de `PROMPTS_CODEX.md`, el proyecto debe incluir un archivo `AGENTS.md` en la raíz del repositorio.

Ese archivo funciona como guía persistente para Codex u otros agentes de desarrollo. Debe indicar:

- rol técnico esperado;
- stack obligatorio;
- arquitectura del proyecto;
- módulos principales;
- reglas de calidad;
- restricciones del MVP;
- flujo antifraude obligatorio;
- criterios de aceptación;
- comandos esperados para correr, migrar y testear.

Regla de uso:

> Antes de pedirle código a Codex, indicarle que lea `ROADMAP.md`, `PROMPTS_CODEX.md` y `AGENTS.md`, y que no avance fuera del alcance de la fase actual.

