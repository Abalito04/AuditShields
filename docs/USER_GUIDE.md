# Guia de usuario

Esta guia describe el uso operativo de AuditShields.

## 1. Iniciar sesion

Entrar a la URL de la app y usar las credenciales del usuario admin inicial:

```text
admin@auditshields.local
admin123
```

Roles disponibles:

- `admin`: puede cargar datos, ejecutar auditoria, gestionar casos y usuarios.
- `auditor`: puede operar auditoria y casos.
- `readonly`: puede ver informacion, pero no modificar datos.

## 2. Cargar datos manualmente

Desde el menu lateral se pueden cargar:

- Proveedores
- Ordenes de compra
- Facturas
- Pagos
- Productos
- Stock
- Movimientos de stock

Los campos de solicitante, aprobador y operador representan personas del proceso original de la empresa, no necesariamente usuarios de AuditShields.

## 3. Importar Excel o CSV

Entrar a:

```text
/imports
```

Desde ahi se pueden descargar plantillas para:

- proveedores
- ordenes de compra
- facturas
- pagos
- productos
- stock actual
- movimientos de stock

Para importar:

1. Entrar a `/imports/new`.
2. Seleccionar entidad.
3. Subir `.xlsx` o `.csv`.
4. Revisar el resultado de importacion.

El sistema valida:

- columnas obligatorias;
- fechas;
- montos;
- relaciones por `supplier_code`, `po_number`, `invoice_number` y `sku`;
- extension de archivo;
- archivo vacio;
- tamano maximo.

Las filas invalidas no se importan y quedan registradas en el detalle.

## 4. Ejecutar auditoria

Desde el dashboard, presionar:

```text
Ejecutar auditoria
```

El motor:

1. ejecuta reglas activas;
2. genera alertas nuevas;
3. ignora alertas duplicadas por fingerprint;
4. crea automaticamente un caso por cada alerta.

## 5. Revisar alertas

Entrar a:

```text
/alerts
```

Cada alerta muestra:

- regla activada;
- modulo;
- entidad;
- riesgo;
- score;
- monto en riesgo;
- estado;
- evidencia JSON.

## 6. Gestionar casos

Entrar a:

```text
/cases
```

En cada caso se puede:

- cambiar estado;
- escribir resumen de resolucion;
- agregar comentarios;
- asignar responsable;
- revisar historial;
- abrir la alerta original.

Estados disponibles:

- Nuevo
- En revision
- Requiere documentacion
- Observado
- En correccion
- Normalizado
- Falso positivo
- Confirmado
- Escalado
- Cerrado

## 7. Dashboard

El dashboard muestra:

- alertas activas;
- casos abiertos;
- casos criticos;
- monto en riesgo;
- proveedores observados;
- productos o movimientos observados;
- ultimos casos;
- reglas mas activadas;
- casos por estado;
- alertas por modulo.

## 8. Reportes

Entrar a:

```text
/reports
```

Reportes disponibles:

- casos de auditoria;
- alertas;
- resumen de riesgo.

Los archivos se descargan en formato Excel.
