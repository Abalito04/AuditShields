# Guion de demo

Duracion sugerida: 5 a 10 minutos.

## 1. Presentar el problema

Mensaje:

```text
Muchas PyMEs pierden dinero por errores de carga, controles debiles, pagos duplicados, proveedores mal documentados o diferencias de stock. El problema no siempre es fraude intencional: muchas veces falta trazabilidad.
```

Idea fuerza:

```text
AuditShields no reemplaza al auditor: le muestra donde mirar primero.
```

## 2. Mostrar login y dashboard

Entrar con:

```text
admin@auditshields.local
admin123
```

Mostrar:

- alertas activas;
- casos abiertos;
- monto en riesgo;
- reglas mas activadas;
- ultimos casos.

## 3. Mostrar carga de datos

Abrir:

```text
/imports
```

Explicar:

- se pueden descargar plantillas;
- se pueden importar Excel/CSV;
- el sistema valida columnas y relaciones;
- las filas con error quedan registradas.

## 4. Ejecutar auditoria

Desde el dashboard, presionar:

```text
Ejecutar auditoria
```

Explicar:

- corre reglas claras;
- crea alertas;
- evita duplicados;
- crea casos automaticamente.

## 5. Revisar alertas

Abrir:

```text
/alerts
```

Mostrar una alerta con:

- regla activada;
- descripcion;
- score;
- monto;
- evidencia JSON.

Mensaje:

```text
La alerta no acusa a nadie. Explica una senal de riesgo para que el auditor revise.
```

## 6. Abrir caso critico

Desde una alerta, abrir el caso asociado.

Mostrar:

- estado;
- responsable;
- alerta original;
- comentarios;
- historial.

## 7. Gestionar el caso

Acciones sugeridas:

1. Asignar responsable.
2. Cambiar estado a `En revision`.
3. Agregar comentario.
4. Cambiar estado a `Normalizado` o `Falso positivo`.

Explicar que cada accion queda registrada.

## 8. Exportar reportes

Abrir:

```text
/reports
```

Descargar:

- casos;
- alertas;
- resumen de riesgo.

Mensaje:

```text
El jefe o dueno puede recibir un Excel entendible con los principales riesgos y el estado de normalizacion.
```

## 9. Cierre

Mensaje final:

```text
AuditShields convierte datos dispersos de compras, pagos e inventario en alertas explicables y casos gestionables. Ayuda a priorizar revision, documentar acciones y cerrar riesgos.
```

## Escenarios demo incluidos

Los datos demo incluyen:

- proveedor incompleto;
- proveedores con misma cuenta bancaria;
- factura duplicada;
- pago duplicado;
- pago sin factura;
- proveedor nuevo con pago alto;
- aprobador igual al solicitante;
- compras fraccionadas;
- ajustes manuales repetidos;
- diferencia de inventario;
- stock negativo;
- movimiento fuera de horario.
