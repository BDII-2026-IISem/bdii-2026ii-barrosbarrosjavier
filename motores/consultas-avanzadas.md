# Consultas Avanzadas — HornoRaíz

## 1. Renombramiento de tablas y columnas a inglés (normativa del profesor)

Como requisito para esta tarea, el profesor exige que las tablas estén nombradas en plural y en inglés. Se ejecutó el siguiente script en el editor SQL de DBeaver, sobre la base `hornoraiz` en MySQL, renombrando las 10 tablas del modelo:

```sql
RENAME TABLE
  producto TO products,
  insumo TO supplies,
  receta TO recipes,
  receta_insumo TO recipe_supplies,
  lote_produccion TO production_batches,
  movimiento_insumo TO supply_movements,
  venta TO sales,
  venta_detalle TO sale_details,
  pago TO payments,
  promocion TO promotions;

SHOW TABLES;
```

**Evidencia (imagen):**

![Tablas renombradas correctamente en MySQL](consultas/01-tablas-renombradas.png)

**Resultado:** `SHOW TABLES` confirmó las 10 tablas con sus nuevos nombres en plural e inglés (`products`, `supplies`, `recipes`, `recipe_supplies`, `production_batches`, `supply_movements`, `sales`, `sale_details`, `payments`, `promotions`), sin pérdida de datos ni de las relaciones de Foreign Key existentes, ya que `RENAME TABLE` en MySQL preserva automáticamente las restricciones y los índices asociados.

## 2. Renombramiento de columnas a inglés

Con las 10 tablas ya renombradas (Sección 1), se renombraron sus columnas siguiendo el mismo criterio de idioma. Además del renombrado de nombres propios de columna (`nombre → name`, `descripcion → description`, `fecha → date`, `cantidad → quantity`, `estado`/`is_active → status`, etc.), se aplicó una convención adicional: la columna booleana `is_active`, presente en `products`, `supplies`, `recipes`, `recipe_supplies`, `production_batches` y `promotions`, se renombró también a `status`, unificando su nombre con la columna `status` de flujo de negocio ya existente en `sales`, `payments` y `supply_movements` (renombrada desde `estado`).

```sql
ALTER TABLE products
  RENAME COLUMN nombre TO name,
  RENAME COLUMN descripcion TO description,
  RENAME COLUMN precio TO price;

ALTER TABLE supplies
  RENAME COLUMN codigo TO code,
  RENAME COLUMN nombre TO name,
  RENAME COLUMN unidad_medida TO unit_of_measure,
  RENAME COLUMN stock_minimo TO min_stock;

ALTER TABLE recipes
  RENAME COLUMN producto_id TO product_id,
  RENAME COLUMN nombre TO name,
  RENAME COLUMN descripcion TO description;

ALTER TABLE recipe_supplies
  RENAME COLUMN principal_id TO main_id,
  RENAME COLUMN relacionado_id TO related_id,
  RENAME COLUMN datos_relacion TO relation_data;

ALTER TABLE production_batches
  RENAME COLUMN receta_id TO recipe_id,
  RENAME COLUMN nombre TO name,
  RENAME COLUMN descripcion TO description;

ALTER TABLE supply_movements
  RENAME COLUMN lote_produccion_id TO production_batch_id,
  RENAME COLUMN insumo_id TO supply_id,
  RENAME COLUMN tipo TO type,
  RENAME COLUMN fecha TO date,
  RENAME COLUMN cantidad TO quantity,
  RENAME COLUMN observaciones TO notes,
  RENAME COLUMN estado TO status;

ALTER TABLE sales
  RENAME COLUMN cliente_id TO client_id,
  RENAME COLUMN fecha TO date,
  RENAME COLUMN impuestos TO taxes,
  RENAME COLUMN estado TO status;

ALTER TABLE sale_details
  RENAME COLUMN cabecera_id TO header_id,
  RENAME COLUMN cantidad TO quantity,
  RENAME COLUMN valor_unitario TO unit_price,
  RENAME COLUMN observaciones TO notes;

ALTER TABLE payments
  RENAME COLUMN referencia_tipo TO reference_type,
  RENAME COLUMN referencia_id TO reference_id,
  RENAME COLUMN metodo TO method,
  RENAME COLUMN monto TO amount,
  RENAME COLUMN fecha TO date,
  RENAME COLUMN estado TO status;

ALTER TABLE promotions
  RENAME COLUMN nombre TO name,
  RENAME COLUMN descripcion TO description;

ALTER TABLE products RENAME COLUMN is_active TO status;
ALTER TABLE supplies RENAME COLUMN is_active TO status;
ALTER TABLE recipes RENAME COLUMN is_active TO status;
ALTER TABLE recipe_supplies RENAME COLUMN is_active TO status;
ALTER TABLE production_batches RENAME COLUMN is_active TO status;
ALTER TABLE promotions RENAME COLUMN is_active TO status;
```

**Evidencia (imagen):**

![Columnas renombradas — INFORMATION_SCHEMA.COLUMNS por tabla](consultas/02-columnas-renombradas.png)

**Resultado:** se verificaron los nombres finales mediante consulta a `INFORMATION_SCHEMA.COLUMNS`, confirmando que las 10 tablas quedaron con sus columnas en inglés. Se documenta como advertencia para las consultas siguientes: la columna `status` no tiene un tipo ni dominio de valores uniforme entre tablas — es `NUMBER(1)`/booleano (`0`/`1`, ex `is_active`) en `products`, `supplies`, `recipes`, `recipe_supplies`, `production_batches` y `promotions`, pero es texto de estado de flujo de negocio (ex `estado`) en `sales`, `payments` y `supply_movements`. Cualquier consulta que filtre o compare por `status` debe considerar esta diferencia según la tabla involucrada.

**Nota adicional:** `sale_details` no tiene columna `status` — no existía `is_active` ni `estado` en su definición original, y esa ausencia se mantuvo sin cambios.