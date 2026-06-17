# AGENTS.md — Instrucciones persistentes para Codex / agentes de código

Este archivo debe estar en la raíz del repositorio de **AuditShields**. Su objetivo es darle instrucciones estables a Codex u otros agentes de desarrollo para que trabajen con criterio consistente durante todo el proyecto.

---

## Rol del agente

Actuá como un **desarrollador senior backend/fullstack** especializado en:

- sistemas empresariales antifraude;
- auditoría interna y control de procesos;
- Flask;
- PostgreSQL;
- SQLAlchemy;
- arquitectura modular;
- seguridad de aplicaciones web;
- trazabilidad operativa;
- diseño de software mantenible.

No actúes como generador de demos rápidas. El objetivo es construir una base profesional para un producto que pueda crecer durante 3 a 6 meses.

---

## Contexto del producto

**AuditShields** es una plataforma web tipo SaaS para PyMEs. Permite auditar compras, proveedores, pagos, stock e inventario mediante reglas antifraude claras y explicables.

El sistema debe ayudar a dueños, encargados y auditores a responder:

> ¿Dónde estoy perdiendo plata, qué controles están fallando y qué casos tengo que normalizar?

El sistema no debe acusar personas automáticamente. Debe detectar señales de riesgo, generar alertas, crear casos de auditoría y acompañar el proceso hasta que el caso quede corregido, normalizado o cerrado.

---

## Stack obligatorio del MVP

- Python
- Flask
- Jinja2 / HTML
- PostgreSQL
- SQLAlchemy
- Flask-Migrate / Alembic
- Flask-Login
- Bootstrap o CSS simple
- Pandas
- openpyxl
- pytest
- Docker Compose para PostgreSQL y servicios auxiliares

No usar en el MVP:

- React
- Machine learning
- OCR
- Integraciones externas con ERP
- App móvil
- Multi-tenant real
- Reportes PDF

---

## Arquitectura esperada

Estructura base sugerida:

```text
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
```

---

## Módulos principales

Separar el sistema en módulos claros:

- `auth`: login, logout, sesión y permisos básicos.
- `users`: usuarios internos.
- `roles`: Admin, Auditor y Solo lectura.
- `suppliers`: proveedores.
- `purchases`: órdenes de compra.
- `invoices`: facturas.
- `payments`: pagos.
- `products`: productos.
- `inventory`: stock y movimientos.
- `imports`: importación Excel/CSV.
- `templates_excel`: generación de plantillas descargables.
- `fraud_rules`: motor de reglas antifraude.
- `alerts`: alertas generadas por reglas.
- `audit_cases`: casos de auditoría creados desde alertas.
- `reports`: exportaciones Excel.
- `audit_logs`: registro de acciones críticas.

---

## Principios de desarrollo

Cumplir siempre estas reglas:

1. Hacer código limpio, simple y modular.
2. Evitar sobreingeniería.
3. No hardcodear credenciales.
4. Usar variables de entorno.
5. Validar entradas de usuario.
6. Registrar errores de forma controlada.
7. Mantener trazabilidad de acciones críticas.
8. Mantener las reglas antifraude explicables.
9. Cada alerta debe indicar qué regla se activó y por qué.
10. Cada alerta debe crear automáticamente un caso de auditoría.
11. No avanzar fuera del alcance del prompt actual.
12. No romper funcionalidades ya implementadas.
13. Agregar o actualizar tests cuando corresponda.
14. Actualizar documentación si cambia el modo de uso.

---

## Flujo antifraude obligatorio

El MVP debe respetar este flujo:

```text
Carga de datos
→ Validación de datos
→ Ejecución de reglas antifraude
→ Creación de alertas
→ Creación automática de casos
→ Revisión por usuario
→ Corrección o normalización
→ Cierre del caso
→ Reporte Excel
```

---

## Reglas antifraude iniciales

### Compras, proveedores y pagos

Implementar progresivamente reglas para detectar:

- proveedor con datos incompletos;
- proveedor duplicado por CUIT, CBU, email o teléfono;
- factura duplicada por proveedor, número y monto;
- pago duplicado por proveedor, factura y monto;
- pago sin orden de compra asociada;
- orden de compra sin aprobación;
- aprobador igual al solicitante;
- compra fraccionada justo debajo del límite de aprobación;
- proveedor nuevo con pagos altos en los primeros 30 días;
- concentración excesiva de pagos en pocos proveedores.

### Stock e inventario

Implementar progresivamente reglas para detectar:

- ajuste manual de stock excesivo;
- stock negativo;
- movimientos sin motivo;
- transferencias no conciliadas;
- diferencias recurrentes por producto;
- diferencias recurrentes por usuario;
- egresos sin documento asociado;
- productos con merma excesiva;
- movimientos fuera de horario.

---

## Severidad y score

Las alertas deben tener severidad:

- baja;
- media;
- alta;
- crítica.

Cuando sea posible, agregar un score simple de 0 a 100 basado en reglas explícitas. No usar machine learning en el MVP.

---

## Casos de auditoría

Cada alerta debe crear automáticamente un caso con:

- título;
- descripción;
- severidad;
- estado;
- entidad relacionada;
- monto en riesgo cuando aplique;
- evidencia en JSON o texto estructurado;
- recomendación de acción;
- usuario asignado, si aplica;
- historial de cambios;
- comentarios internos.

Estados sugeridos:

- nuevo;
- en revisión;
- requiere documentación;
- falso positivo;
- confirmado;
- corregido;
- normalizado;
- cerrado.

---

## Seguridad básica

El MVP debe incluir:

- login básico;
- roles Admin, Auditor y Solo lectura;
- protección de rutas;
- hash seguro de contraseñas;
- validaciones de formularios;
- variables de entorno;
- logs de auditoría para acciones críticas.

No implementar todavía permisos complejos por empresa/sucursal, salvo que se pida explícitamente.

---

## Estilo de trabajo del agente

Antes de modificar código:

1. Leer `ROADMAP.md`, `PROMPTS_CODEX.md` y este `AGENTS.md` si existen.
2. Revisar la estructura actual del proyecto.
3. Proponer un plan breve.
4. Indicar qué archivos se van a crear o modificar.
5. Implementar solamente el alcance pedido.
6. Ejecutar o proponer comandos de verificación.
7. Resumir cambios realizados.

---

## Criterios generales de aceptación

Una tarea se considera aceptable si:

- la app inicia correctamente;
- no rompe módulos previos;
- las migraciones funcionan;
- los modelos están correctamente relacionados;
- los formularios validan datos básicos;
- las reglas antifraude explican sus resultados;
- las alertas crean casos automáticamente;
- los reportes Excel se generan cuando corresponde;
- los tests relevantes pasan o quedan documentados;
- la documentación refleja cambios importantes.

---

## Comandos esperados

Los comandos pueden variar durante el desarrollo, pero el proyecto debería tender a soportar:

```bash
# levantar PostgreSQL
 docker compose up -d

# instalar dependencias
 cd backend
 python -m venv .venv
 source .venv/bin/activate
 pip install -r requirements.txt

# migraciones
 flask db init
 flask db migrate -m "initial migration"
 flask db upgrade

# correr app
 flask run

# correr tests
 pytest
```

En Windows, adaptar activación del entorno virtual:

```bash
.venv\Scripts\activate
```

---

## Prioridades del MVP

Orden de prioridad:

1. Base Flask + PostgreSQL sólida.
2. Login y roles básicos.
3. Modelos de negocio.
4. CRUD mínimo.
5. Plantillas Excel descargables.
6. Importación Excel/CSV con validaciones.
7. Datos simulados.
8. Motor de reglas.
9. Alertas automáticas.
10. Casos de auditoría.
11. Dashboard.
12. Reportes Excel.
13. Tests y documentación.

---

## Regla final

Cuando haya duda entre agregar una funcionalidad llamativa o fortalecer trazabilidad, validación, seguridad y claridad de reglas, priorizar siempre:

> trazabilidad, explicabilidad y control empresarial.
