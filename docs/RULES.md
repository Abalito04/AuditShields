# Reglas antifraude

AuditShields usa reglas explicables. Cada alerta debe indicar que regla se activo, por que, cual es la entidad afectada, el score, el nivel de riesgo y la evidencia.

## Niveles de riesgo

```text
0 - 29   Bajo
30 - 59  Medio
60 - 79  Alto
80 - 100 Critico
```

## Compras, proveedores y pagos

### R001 - Pago duplicado exacto

Detecta pagos con:

- mismo proveedor;
- misma factura o referencia equivalente;
- mismo monto;
- fechas iguales o cercanas.

Riesgo: pago duplicado, error de carga o salida indebida de fondos.

### R002 - Factura duplicada

Detecta facturas con:

- mismo proveedor;
- mismo numero;
- mismo importe.

Riesgo: duplicacion de factura y posible doble pago.

### R003 - Proveedores con misma cuenta bancaria

Detecta proveedores distintos que comparten `bank_account`.

Riesgo: proveedor duplicado, desvio de pagos o cuenta bancaria compartida sin justificacion.

### R004 - Proveedor nuevo con pagos altos

Detecta proveedores creados recientemente que acumulan pagos por encima del umbral configurado.

Config inicial:

```text
days = 30
amount_threshold = 1000000
```

Riesgo: alta reciente sin suficiente historial y pagos relevantes en poco tiempo.

### R005 - Pago o factura sin orden de compra

Detecta:

- facturas sin orden de compra;
- pagos sin factura;
- pagos asociados a facturas sin orden.

Riesgo: falta de trazabilidad y aprobacion previa.

### R006 - Compra fraccionada

Detecta varias ordenes del mismo proveedor dentro de una ventana corta, con montos justo debajo del limite de aprobacion.

Config inicial:

```text
approval_limit = 500000
lower_ratio = 0.9
window_days = 7
```

Riesgo: division artificial de compras para evitar aprobaciones.

### R007 - Aprobador igual al solicitante

Detecta ordenes donde la misma persona figura como solicitante y aprobador.

Riesgo: falta de separacion de funciones.

### R008 - Concentracion excesiva en proveedor

Detecta proveedores que concentran un porcentaje alto del total pagado.

Config inicial:

```text
share_threshold = 0.5
```

Riesgo: dependencia excesiva, condiciones no competitivas o proveedor privilegiado.

### R009 - Pago fuera de horario o dia no laboral

Detecta pagos registrados fuera del horario laboral o durante fin de semana.

Config inicial:

```text
start_hour = 8
end_hour = 19
```

Riesgo: operacion fuera del circuito normal de control.

### R010 - Proveedor con datos incompletos

Detecta proveedores sin datos criticos:

- `tax_id`;
- `bank_account`;
- `email`;
- `address`.

Riesgo: controles fiscales, bancarios o de contacto insuficientes.

## Stock e inventario

### S001 - Ajustes manuales repetidos

Detecta productos con muchos movimientos `ADJUSTMENT` en una ventana corta.

Config inicial:

```text
window_days = 15
min_adjustments = 3
```

Riesgo: diferencias recurrentes, correcciones manuales excesivas o falta de documentacion.

### S002 - Stock negativo

Calcula stock desde movimientos y detecta productos con resultado menor a cero.

Riesgo: egresos sin respaldo, movimientos faltantes o conteo incorrecto.

### S003 - Diferencia entre stock esperado y fisico

Detecta snapshots donde la diferencia absoluta supera el umbral.

Config inicial:

```text
quantity_threshold = 20
```

Riesgo: merma, error operativo o movimientos no registrados.

### S004 - Movimiento fuera de horario

Detecta movimientos de stock fuera del horario laboral o en fin de semana.

Riesgo: operacion fuera del proceso normal.

### S005 - Merma excesiva

Detecta salidas `OUT` o ajustes negativos con cantidad mayor al umbral.

Config inicial:

```text
quantity_threshold = 50
```

Riesgo: perdida, merma no explicada o egreso sin respaldo.

### S006 - Transferencia no conciliada

Detecta movimientos `TRANSFER` sin contraparte con la misma referencia.

Riesgo: transferencia incompleta o no conciliada.

### S007 - Operador con demasiados ajustes

Detecta operadores con cantidad relevante de ajustes manuales.

Config inicial:

```text
min_adjustments = 3
```

Riesgo: patron recurrente por usuario.

### S008 - Producto activo sin movimiento reciente

Detecta productos activos sin movimientos durante el periodo configurado.

Config inicial:

```text
days_without_movement = 30
```

Riesgo: stock inmovilizado, obsolescencia o falta de uso esperado.

## Duplicados

Cada alerta genera un `fingerprint` estable. Si se reejecuta la auditoria y el riesgo ya existe, el sistema ignora la alerta duplicada y no crea otro caso.
