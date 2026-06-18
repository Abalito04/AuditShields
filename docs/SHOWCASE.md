# Kit de presentacion

Este documento sirve para preparar screenshots, video demo, post de LinkedIn y portfolio de AuditShields.

## Screenshots recomendados

Guardar las capturas en una carpeta `media/auditshields/` o similar.

### 01_login.png

Pantalla: `/login`

Objetivo:

- mostrar acceso profesional;
- dejar claro que hay autenticacion.

Encuadre:

- formulario centrado;
- sin datos sensibles reales.

### 02_dashboard.png

Pantalla: `/dashboard`

Antes de capturar:

1. Entrar con admin.
2. Presionar `Preparar demo`.

Objetivo:

- mostrar metricas reales;
- monto en riesgo;
- casos abiertos;
- reglas mas activadas;
- ultimos casos.

### 03_importaciones.png

Pantalla: `/imports`

Objetivo:

- mostrar plantillas descargables;
- mostrar trazabilidad de importaciones.

Mensaje:

```text
Carga Excel/CSV con validaciones y registro de errores.
```

### 04_alertas.png

Pantalla: `/alerts`

Objetivo:

- mostrar listado de alertas;
- filtros por modulo, riesgo y estado;
- reglas activadas.

### 05_detalle_alerta.png

Pantalla: detalle de una alerta interesante.

Recomendadas:

- pago duplicado;
- proveedor con cuenta bancaria compartida;
- operador con demasiados ajustes;
- stock negativo.

Objetivo:

- mostrar explicacion;
- evidencia interpretada;
- score y monto.

Evitar:

- abrir `Ver datos tecnicos` para screenshots comerciales.

### 06_casos.png

Pantalla: `/cases`

Objetivo:

- mostrar gestion de casos;
- estados;
- responsables;
- riesgo.

### 07_detalle_caso.png

Pantalla: detalle de un caso.

Objetivo:

- mostrar comentario;
- cambio de estado;
- historial;
- alerta original.

Accion previa sugerida:

1. Asignar responsable.
2. Cambiar estado a `En revision`.
3. Agregar comentario.

### 08_reportes.png

Pantalla: `/reports`

Objetivo:

- mostrar salida ejecutiva en Excel;
- reportes de casos, alertas y resumen de riesgo.

### 09_excel_resumen.png

Pantalla: archivo `resumen_riesgo.xlsx` abierto.

Objetivo:

- mostrar que el resultado se puede compartir con jefe, auditor o socio.

## Guion de video demo

Duracion ideal: 60 a 90 segundos.

### Escena 1 - Problema

Texto en pantalla:

```text
Las PyMEs pierden dinero por controles debiles, pagos duplicados y errores de inventario.
```

Mostrar:

- dashboard inicial con metricas.

### Escena 2 - Carga de datos

Mostrar:

- pantalla de importaciones;
- plantillas;
- importacion registrada.

Voz/texto:

```text
AuditShields permite cargar datos manualmente o por Excel/CSV con validaciones.
```

### Escena 3 - Auditoria

Mostrar:

- boton `Ejecutar auditoria`;
- mensaje de alertas/casos generados.

Voz/texto:

```text
El motor ejecuta reglas claras y evita duplicar alertas ya detectadas.
```

### Escena 4 - Alertas explicables

Mostrar:

- listado de alertas;
- detalle de alerta.

Voz/texto:

```text
Cada alerta explica que regla se activo, por que y que evidencia la respalda.
```

### Escena 5 - Casos de auditoria

Mostrar:

- detalle de caso;
- comentario;
- historial.

Voz/texto:

```text
Cada alerta crea un caso gestionable hasta su normalizacion o cierre.
```

### Escena 6 - Reportes

Mostrar:

- pantalla de reportes;
- Excel de resumen.

Voz/texto:

```text
El resultado se puede exportar a Excel para seguimiento ejecutivo.
```

### Cierre

Texto:

```text
AuditShields: auditoria continua y antifraude explicable para PyMEs.
```

## Carrusel de LinkedIn

### Slide 1

```text
AuditShields
Auditoria continua y antifraude para PyMEs
```

Visual: dashboard.

### Slide 2

```text
Problema
Pagos duplicados, proveedores incompletos, compras sin trazabilidad y diferencias de stock.
```

Visual: lista de alertas.

### Slide 3

```text
Reglas explicables
Cada alerta indica que se detecto, por que y con que evidencia.
```

Visual: detalle de alerta.

### Slide 4

```text
Casos gestionables
Cada alerta crea automaticamente un caso con estado, comentarios e historial.
```

Visual: detalle de caso.

### Slide 5

```text
Reportes ejecutivos
Exportacion Excel para compartir riesgos, casos y resumen.
```

Visual: reportes o Excel.

### Slide 6

```text
Stack
Python, Flask, PostgreSQL, SQLAlchemy, Jinja, Pandas, OpenPyXL y pytest.
```

Visual: dashboard o arquitectura simple.

## Texto corto para portfolio

```text
AuditShields es una plataforma web MVP para auditoria continua y control antifraude en PyMEs. Permite cargar datos de compras, pagos, proveedores e inventario, ejecutar reglas explicables, generar alertas, crear casos de auditoria y exportar reportes ejecutivos.

El proyecto cubre el flujo completo: autenticacion, roles, CRUD, importacion Excel/CSV, validaciones, motor de reglas, alertas, casos, dashboard, reportes, tests y deploy en Railway con PostgreSQL.
```

## Checklist antes de grabar

- Base limpia o demo preparada.
- Login funcionando.
- Dashboard con metricas visibles.
- Al menos 10 alertas generadas.
- Al menos 5 casos visibles.
- Un caso con comentario e historial.
- Reportes descargables.
- Zoom del navegador en 90% o 100%.
- No mostrar credenciales ni variables de entorno.
