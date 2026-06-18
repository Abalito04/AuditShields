# AuditShields - Caso de portfolio

## Resumen

AuditShields es una plataforma web de auditoria continua y control antifraude para PyMEs. El MVP permite cargar datos de compras, proveedores, facturas, pagos, productos e inventario; ejecutar reglas antifraude explicables; generar alertas; crear casos de auditoria; gestionar estados y exportar reportes Excel.

## Problema

Muchas PyMEs tienen informacion dispersa en planillas o sistemas simples. Esto dificulta detectar:

- pagos duplicados;
- facturas repetidas;
- proveedores incompletos o duplicados;
- compras sin aprobacion suficiente;
- stock negativo;
- ajustes manuales repetidos;
- movimientos fuera de horario.

## Solucion

AuditShields centraliza datos operativos, ejecuta reglas claras y convierte senales de riesgo en casos gestionables.

Flujo:

```text
Carga de datos
-> Validacion
-> Motor de reglas
-> Alertas
-> Casos
-> Revision
-> Normalizacion o cierre
-> Reportes Excel
```

## Funcionalidades

- Autenticacion con Flask-Login.
- Roles: admin, auditor y solo lectura.
- CRUD de entidades clave.
- Importacion Excel/CSV con Pandas.
- Plantillas Excel generadas con OpenPyXL.
- Motor antifraude basado en reglas explicables.
- Alertas con score, nivel de riesgo y evidencia.
- Casos de auditoria con comentarios, estados e historial.
- Dashboard con metricas reales.
- Reportes Excel.
- Tests con pytest.
- Deploy en Railway con PostgreSQL.

## Reglas implementadas

Compras y pagos:

- Pago duplicado.
- Factura duplicada.
- Proveedores con misma cuenta bancaria.
- Proveedor nuevo con pagos altos.
- Pago o factura sin orden de compra.
- Compra fraccionada.
- Aprobador igual al solicitante.
- Concentracion excesiva en proveedor.
- Pago fuera de horario.
- Proveedor con datos incompletos.

Inventario:

- Ajustes manuales repetidos.
- Stock negativo.
- Diferencia entre stock esperado y fisico.
- Movimiento fuera de horario.
- Merma excesiva.
- Transferencia no conciliada.
- Operador con demasiados ajustes.
- Producto activo sin movimiento reciente.

## Stack

- Python
- Flask
- PostgreSQL
- SQLAlchemy
- Flask-Migrate
- Flask-Login
- Jinja2
- Bootstrap
- Pandas
- OpenPyXL
- pytest
- Railway

## Decisiones tecnicas

- MVP sin React para priorizar velocidad y simplicidad.
- Reglas explicables en vez de machine learning.
- Fingerprint por alerta para evitar duplicados.
- Caso automatico por cada alerta.
- Evidencia estructurada para trazabilidad.
- Reportes Excel en vez de PDF para adaptarse al uso real de PyMEs.

## Resultado

El MVP permite demostrar un flujo completo de auditoria:

1. cargar datos;
2. ejecutar reglas;
3. detectar riesgos;
4. revisar alertas;
5. gestionar casos;
6. exportar resumen ejecutivo.

## Aprendizajes

- La explicabilidad es clave en sistemas antifraude.
- No alcanza con detectar: hay que ayudar a normalizar.
- Los datos incompletos son parte del problema, no una excepcion.
- Un MVP empresarial necesita trazabilidad antes que features llamativas.
