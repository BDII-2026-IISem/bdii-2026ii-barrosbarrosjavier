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

## 3. Carga de datos — tabla `products`

Se generaron 100 registros de prueba para la tabla `products`, en un archivo CSV separado por `;`, con las columnas `id`, `sku`, `name`, `description`, `price`, `status`, correspondientes al esquema ya renombrado en la Sección 2.

**Evidencia (imagen):**

![100 registros importados correctamente en products](consultas/03-products-importados.png)

**Resultado:** se importaron los 100 registros en la tabla `products` sin errores, configurando el delimitador `;` en el asistente de importación de DBeaver.

## 4. Carga de datos — tabla `supplies`

Se generaron 100 registros de prueba para la tabla `supplies`, en un archivo CSV separado por `;`, con las columnas `id`, `code`, `name`, `unit_of_measure`, `min_stock`, `status`.

**Evidencia (imagen):**

![100 registros importados correctamente en supplies](consultas/04-supplies-importados.png)

**Resultado:** se importaron los 100 registros en la tabla `supplies` sin errores, configurando el delimitador `;` en el asistente de importación de DBeaver.

## 5. Carga de datos — tabla `recipes`

Se generaron 100 registros de prueba para la tabla `recipes`, en un archivo CSV separado por `;`, con las columnas `id`, `product_id`, `name`, `description`, `status`, `created_at`, `updated_at`. Los valores de `product_id` se generaron dentro del rango 1-100, referenciando los productos ya cargados en la Sección 3, respetando la Foreign Key hacia `products`.

**Resultado:** se importaron los 100 registros en la tabla `recipes` sin errores. Se incluyeron 20 productos con una segunda receta asociada, reflejando la relación `Producto 1:N Receta` de la narrativa del proyecto (donde una sola versión de receta puede estar vigente por producto); estas recetas alternativas se marcaron con `status = 0` para simular versiones no vigentes.

**Evidencia (imagen):**

![100 registros importados correctamente en recipes](consultas/05-recipes-importados.png)

## 6. Carga de datos — tabla `recipe_supplies`

Se generaron 100 registros de prueba para la tabla `recipe_supplies`, en un archivo CSV separado por `;`, con las columnas `id`, `main_id`, `related_id`, `relation_data`, `status`. Los valores de `main_id` referencian `recipes(id)` y `related_id` referencian `supplies(id)`, ambos en el rango 1-100, sin pares repetidos, resolviendo la relación N:M entre `recipes` y `supplies`.

**Resultado:** se importaron los 100 registros sin errores. La columna `relation_data` se generó como texto libre combinando cantidad y unidad de medida (ej. `"6.93 l"`), dado que su tipo (`VARCHAR2(255)`) no define una estructura fija.

**Evidencia (imagen):**

![100 registros importados correctamente en recipe_supplies](consultas/06-recipe_supplies-importados.png)

## 7. Carga de datos — tabla `production_batches`

Se generaron 100 registros de prueba para la tabla `production_batches`, en un archivo CSV separado por `;`, con las columnas `id`, `recipe_id`, `name`, `description`, `status`, `created_at`, `updated_at`. Los valores de `recipe_id` se generaron dentro del rango 1-100, referenciando las recetas ya cargadas en la Sección 5, respetando la Foreign Key hacia `recipes`.

**Resultado:** se importaron los 100 registros sin errores. Se usó una distribución de `status` con 85% activo / 15% inactivo, para dar variedad a las consultas de filtrado posteriores.

**Evidencia (imagen):**

![100 registros importados correctamente en production_batches](consultas/07-production_batches-importados.png)

## 8. Carga de datos — tabla `supply_movements`

Se generaron 100 registros de prueba para la tabla `supply_movements`, en un archivo CSV separado por `;`, con las columnas `id`, `production_batch_id`, `supply_id`, `type`, `date`, `quantity`, `notes`, `status`. `supply_id` se generó siempre dentro del rango 1-100 (obligatorio), mientras que `production_batch_id` se dejó vacío en aproximadamente el 30% de las filas, reflejando su carácter nullable — movimientos sin lote de producción asociado, como compras directas o mermas de bodega.

**Resultado:** se importaron los 100 registros sin errores, verificando que las celdas vacías de `production_batch_id` se interpretaran como `NULL` en el asistente de importación. Los valores de `type` (`IN`, `OUT`, `ADJUSTMENT`) y `status` (`completed`, `pending`, `cancelled`) son texto de flujo de negocio, distinto del `status` booleano usado en `products`, `supplies`, `recipes`, `recipe_supplies`, `production_batches` y `promotions` (ver nota de la Sección 2).

**Evidencia (imagen):**

![100 registros importados correctamente en supply_movements](consultas/08-supply_movements-importados.png)

## 9. Carga de datos — tabla `sales`

Se generaron 100 registros de prueba para la tabla `sales`, en un archivo CSV separado por `;`, con las columnas `id`, `client_id`, `date`, `subtotal`, `taxes`, `total`, `status`. `client_id` se dejó vacío en aproximadamente el 40% de las filas, simulando ventas de mostrador sin cliente registrado — consistente con la ausencia de Foreign Key para esta columna, ya documentada en el modelo original. `taxes` se calculó como el 19% del `subtotal`, y `total` como la suma de ambos, para mantener consistencia numérica entre las tres columnas.

**Resultado:** se importaron los 100 registros sin errores. `status` (`paid`, `pending`, `cancelled`) es texto de flujo de negocio, distinto del `status` booleano usado en otras tablas del modelo (ver nota de la Sección 2).

**Evidencia (imagen):**

![100 registros importados correctamente en sales](consultas/09-sales-importados.png)

## 10. Carga de datos — tabla `sale_details`

Se generaron 100 registros de prueba para la tabla `sale_details`, en un archivo CSV separado por `;`, con las columnas `id`, `header_id`, `item_id`, `quantity`, `unit_price`, `total`, `notes`. `header_id` referencia `sales(id)` e `item_id` referencia `products(id)`, ambos en el rango 1-100. `total` se calculó como `quantity × unit_price`, garantizando consistencia interna en cada fila.

**Resultado:** se importaron los 100 registros sin errores.

**Nota:** `header_id` se generó de forma independiente al `subtotal` registrado en `sales` (Sección 9); la suma de `total` por `header_id` no necesariamente coincide con el `subtotal` de la venta correspondiente, al tratarse de dos conjuntos de datos generados por separado para fines de prueba.

**Evidencia (imagen):**

![100 registros importados correctamente en sale_details](consultas/10-sale_details-importados.png)

## 11. Carga de datos — tabla `payments`

Se generaron 100 registros de prueba para la tabla `payments`, en un archivo CSV separado por `;`, con las columnas `id`, `reference_type`, `reference_id`, `method`, `amount`, `date`, `status`. Todos los registros se generaron con `reference_type = 'sale'` y `reference_id` en el rango 1-100, asociando cada pago a una venta de la tabla `sales` (Sección 9) por convención de datos, dado que esta columna es polimórfica y no está resguardada por una Foreign Key.

**Resultado:** se importaron los 100 registros sin errores.

**Evidencia (imagen):**

![100 registros importados correctamente en payments](consultas/11-payments-importados.png)

## 12. Carga de datos — tabla `promotions`

Se generaron 100 registros de prueba para la tabla `promotions`, en un archivo CSV separado por `;`, con las columnas `id`, `name`, `description`, `status`, `created_at`, `updated_at`. Sin Foreign Key ni tabla puente hacia `products`, respetando la decisión ya documentada para la relación `Promotion N:M Product`.

**Resultado:** se importaron los 100 registros sin errores. Se usó una distribución de `status` con 70% activo / 30% inactivo, simulando promociones ya vencidas para dar variedad a las consultas de filtrado.

**Evidencia (imagen):**

![100 registros importados correctamente en promotions](consultas/12-promotions-importados.png)

## 1. Consultas avanzadas en MySQL

### 1.1 Mostrar algunos de los registros de la tabla `products`

```sql
SELECT sku, name, price, status FROM products;
```

**Evidencia (imagen):**

![Registros de la tabla products](consultas/mysql-01-1-products.png)

**Resultado:** la consulta devolvió los 100 registros de `products` con sus columnas `sku`, `name`, `price` y `status`, confirmando la carga de datos realizada en la Sección 3.

### 1.2 Mostrar de forma ordenada (DESC) las ventas desde su comienzo

```sql
SELECT id, date, subtotal, status FROM sales ORDER BY date DESC;
```

**Evidencia (imagen):**

![Ventas ordenadas descendentemente por fecha](consultas/mysql-02-1-sales.png)

**Resultado:** la consulta devolvió los 100 registros de `sales` ordenados de la fecha más reciente (2026-03-27) a la más antigua (2025-06-02), confirmando que `ORDER BY date DESC` funciona correctamente sobre los datos cargados en la Sección 9.

### 1.3 Consultas a múltiples tablas mediante WHERE

```sql
SELECT *
FROM sale_details SD, sales S
WHERE S.id = SD.header_id;
```

**Evidencia (imagen):**

![Join de sale_details y sales mediante WHERE](consultas/mysql-03-1-sale_details_sales_where.png)

**Resultado:** la consulta devolvió los 100 registros de `sale_details` combinados con su venta correspondiente en `sales`, mediante la condición `S.id = SD.header_id` en la cláusula WHERE.

### 1.4 Consultas a múltiples tablas mediante JOIN

```sql
SELECT S.date, S.status, SD.*
FROM sales AS S
JOIN sale_details AS SD ON (S.id = SD.header_id);
```

**Evidencia (imagen):**

![Join de sales y sale_details mediante JOIN](consultas/mysql-04-1-sales_sale_details_join.png)

**Resultado:** la consulta devolvió los 100 registros combinando `sales` y `sale_details` mediante `JOIN ... ON`, con el mismo resultado que la Sección 1.3 (forma WHERE), confirmando que ambas sintaxis son equivalentes para esta relación.

### 1.5 Condiciones en las consultas / filtros

Para las condiciones se utiliza la cláusula WHERE. Se realiza la misma consulta de la Sección 1.3/1.4, filtrando por un estado específico de `sales.status`.

```sql
SELECT *
FROM sale_details SD, sales S
WHERE S.id = SD.header_id AND S.status = 'paid';
```

**Evidencia (imagen):**

![Filtro WHERE con status = paid](consultas/mysql-05-1-status-paid.png)

**Resultado:** la consulta devolvió 82 registros con `status = 'paid'`, filtrando del total de 100 combinaciones `sale_details`/`sales`.

```sql
SELECT S.date, S.status, SD.*
FROM sales AS S
JOIN sale_details AS SD ON (S.id = SD.header_id)
WHERE S.status = 'cancelled';
```

**Evidencia (imagen):**

![Filtro JOIN con status = cancelled](consultas/mysql-05-2-status-cancelled.png)

**Resultado:** la consulta devolvió 10 registros con `status = 'cancelled'`, usando la forma JOIN en vez de WHERE para la relación entre tablas.

### 1.6 Consultas con filtros condicional LIKE

```sql
SELECT * FROM products AS P WHERE P.name LIKE 'Pan%';
```

**Evidencia (imagen):**

![Productos cuyo nombre empieza con Pan](consultas/mysql-06-1-like-pan.png)

**Resultado:** la consulta devolvió 28 registros cuyo `name` comienza con "Pan" (Pan de yema, Pan integral, Pan de leche, Panettone, etc.), aplicando el operador `LIKE` con comodín al final del patrón.

**Mostrar los productos cuya descripción contenga la palabra "chocolate":**

```sql
SELECT * FROM products AS P WHERE P.description LIKE CONCAT('%','chocolate','%');
```

**Evidencia (imagen):**

![Producto cuya descripción contiene chocolate](consultas/mysql-06-2-like-chocolate.png)

**Resultado:** la consulta devolvió 1 registro (`Torta de chocolate Mini clasico`), usando `CONCAT` para construir el patrón `%chocolate%` y localizar la coincidencia dentro de la descripción, sin importar su posición en el texto.