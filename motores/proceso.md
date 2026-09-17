# Creación de Base de Datos — HornoRaíz

Este documento detalla la creación de la base de datos `hornoraiz` y sus tablas mediante dos métodos distintos, para cada motor: **por código**, escribiendo SQL directamente en el editor de DBeaver, y **de forma visual**, sin escribir código, usando la herramienta gráfica propia de cada motor.

---

## 1. Base de Datos MySQL

### 1.1 Creación de las tablas por el editor SQL de DBeaver

Las tablas de `hornoraiz` ya existían (creadas por terminal durante la instalación del motor). Para este ejercicio las eliminé primero, con el fin de recrearlas desde el editor SQL de DBeaver:

```sql
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS promocion_producto;
DROP TABLE IF EXISTS promocion;
DROP TABLE IF EXISTS pago;
DROP TABLE IF EXISTS venta_detalle;
DROP TABLE IF EXISTS venta;
DROP TABLE IF EXISTS movimiento_insumo;
DROP TABLE IF EXISTS lote_produccion;
DROP TABLE IF EXISTS receta_insumo;
DROP TABLE IF EXISTS receta;
DROP TABLE IF EXISTS insumo;
DROP TABLE IF EXISTS producto;
SET FOREIGN_KEY_CHECKS = 1;
SHOW TABLES;
```

**Evidencia (imagen):**

![Tablas eliminadas correctamente](reporte/mysql-01-tablas-eliminadas.png)

**Resultado:** Ejecuté el script completo con `Alt+X` (ejecutar todas las sentencias, no solo la que tiene el cursor). `SHOW TABLES` confirmó `No data` — la base de datos `hornoraiz` quedó sin tablas, lista para reconstruirlas desde cero por este método.

### 1.2 Creación de la tabla `producto`

```sql
CREATE TABLE producto (
  id INT PRIMARY KEY AUTO_INCREMENT,
  sku VARCHAR(50) NOT NULL UNIQUE,
  nombre VARCHAR(100) NOT NULL,
  descripcion VARCHAR(255),
  precio DECIMAL(10, 2) NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE
);
```

**Evidencia (imagen):**

![Tabla producto creada](reporte/mysql-02-tabla-producto.png)

**Resultado:** La tabla se creó sin errores (`Execute time: 0,132s`).

### 1.3 Creación de la tabla `insumo`
 
```sql
CREATE TABLE insumo (
  id INT PRIMARY KEY AUTO_INCREMENT,
  codigo VARCHAR(50) NOT NULL UNIQUE,
  nombre VARCHAR(100) NOT NULL,
  unidad_medida VARCHAR(30) NOT NULL,
  stock_minimo DECIMAL(10, 2) NOT NULL DEFAULT 0,
  is_active BOOLEAN NOT NULL DEFAULT TRUE
);
```
 
**Evidencia (imagen):**
 
![Tabla insumo creada](reporte/mysql-03-tabla-insumo.png)
 
**Resultado:** La tabla se creó sin errores (`Execute time: 0,287s`).

### 1.4 Creación de la tabla `receta`
 
```sql
CREATE TABLE receta (
  id INT PRIMARY KEY AUTO_INCREMENT,
  producto_id INT NOT NULL,
  nombre VARCHAR(100) NOT NULL,
  descripcion VARCHAR(255),
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (producto_id) REFERENCES producto(id)
);
```
 
**Evidencia (imagen):**
 
![Tabla receta creada](reporte/mysql-04-tabla-receta.png)
 
**Resultado:** La tabla se creó sin errores (`Execute time: 0,328s`), respetando la llave foránea hacia `producto`.

### 1.5 Creación de la tabla `receta_insumo`
 
```sql
CREATE TABLE receta_insumo (
  id INT PRIMARY KEY AUTO_INCREMENT,
  principal_id INT NOT NULL,
  relacionado_id INT NOT NULL,
  datos_relacion VARCHAR(255),
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  FOREIGN KEY (principal_id) REFERENCES receta(id),
  FOREIGN KEY (relacionado_id) REFERENCES insumo(id)
);
```
 
**Evidencia (imagen):**
 
![Tabla receta_insumo creada](reporte/mysql-05-tabla-receta-insumo.png)
 
**Resultado:** La tabla se creó sin errores (`Execute time: 0,253s`), resolviendo la relación N:M entre `receta` e `insumo`.

### 1.6 Creación de la tabla `lote_produccion`
 
```sql
CREATE TABLE lote_produccion (
  id INT PRIMARY KEY AUTO_INCREMENT,
  receta_id INT NOT NULL,
  nombre VARCHAR(100) NOT NULL,
  descripcion VARCHAR(255),
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (receta_id) REFERENCES receta(id)
);
```
 
**Evidencia (imagen):**
 
![Tabla lote_produccion creada](reporte/mysql-06-tabla-lote-produccion.png)
 
**Resultado:** La tabla se creó sin errores (`Execute time: 0,16s`).

### 1.7 Creación de la tabla `movimiento_insumo`
 
```sql
CREATE TABLE movimiento_insumo (
  id INT PRIMARY KEY AUTO_INCREMENT,
  lote_produccion_id INT,
  insumo_id INT NOT NULL,
  tipo VARCHAR(50) NOT NULL,
  fecha DATETIME NOT NULL,
  cantidad DECIMAL(10, 2) NOT NULL,
  observaciones TEXT,
  estado VARCHAR(30) NOT NULL,
  FOREIGN KEY (lote_produccion_id) REFERENCES lote_produccion(id),
  FOREIGN KEY (insumo_id) REFERENCES insumo(id)
);
```
 
**Evidencia (imagen):**
 
![Tabla movimiento_insumo creada](reporte/mysql-07-tabla-movimiento-insumo.png)
 
**Resultado:** La tabla se creó sin errores (`Execute time: 0,134s`).

### 1.8 Creación de la tabla `venta`
 
```sql
CREATE TABLE venta (
  id INT PRIMARY KEY AUTO_INCREMENT,
  cliente_id INT,
  fecha DATETIME NOT NULL,
  subtotal DECIMAL(10, 2) NOT NULL,
  impuestos DECIMAL(10, 2) NOT NULL DEFAULT 0,
  total DECIMAL(10, 2) NOT NULL,
  estado VARCHAR(30) NOT NULL
);
```
 
**Evidencia (imagen):**
 
![Tabla venta creada](reporte/mysql-08-tabla-venta.png)
 
**Resultado:** La tabla se creó sin errores (`Execute time: 0,224s`).
 
 ### 1.9 Creación de la tabla `venta_detalle`
 
```sql
CREATE TABLE venta_detalle (
  id INT PRIMARY KEY AUTO_INCREMENT,
  cabecera_id INT NOT NULL,
  item_id INT NOT NULL,
  cantidad DECIMAL(10, 2) NOT NULL,
  valor_unitario DECIMAL(10, 2) NOT NULL,
  total DECIMAL(10, 2) NOT NULL,
  observaciones TEXT,
  FOREIGN KEY (cabecera_id) REFERENCES venta(id),
  FOREIGN KEY (item_id) REFERENCES producto(id)
);
```
 
**Evidencia (imagen):**
 
![Tabla venta_detalle creada](reporte/mysql-09-tabla-venta-detalle.png)
 
**Resultado:** La tabla se creó sin errores (`Execute time: 0,113s`).
 
 ### 1.10 Creación de la tabla `pago`
 
```sql
CREATE TABLE pago (
  id INT PRIMARY KEY AUTO_INCREMENT,
  referencia_tipo VARCHAR(50) NOT NULL,
  referencia_id INT NOT NULL,
  metodo VARCHAR(50) NOT NULL,
  monto DECIMAL(10, 2) NOT NULL,
  fecha DATETIME NOT NULL,
  estado VARCHAR(30) NOT NULL
);
```
 
**Evidencia (imagen):**
 
![Tabla pago creada](reporte/mysql-10-tabla-pago.png)
 
**Resultado:** La tabla se creó sin errores (`Execute time: 0,075s`).

### 1.11 Creación de la tabla `promocion`
 
```sql
CREATE TABLE promocion (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  descripcion VARCHAR(255),
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```
 
**Evidencia (imagen):**
 
![Tabla promocion creada](reporte/mysql-11-tabla-promocion.png)
 
**Resultado:** La tabla se creó sin errores (`Execute time: 0,066s`).

### 1.12 Verificación final

```sql
SHOW TABLES;
```

**Evidencia (imagen):**

![Verificación final de las 10 tablas](reporte/mysql-12-show-tables-final.png)

**Resultado:** `SHOW TABLES` devolvió las 10 tablas esperadas (`insumo`, `lote_produccion`, `movimiento_insumo`, `pago`, `producto`, `promocion`, `receta`, `receta_insumo`, `venta`, `venta_detalle`), confirmando que el modelo quedó completo tras crear las 10 sentencias, sin tablas puente adicionales.

**Nota sobre la relación Promocion N:M Producto:** a diferencia de Receta N:M Insumo (resuelta explícitamente "mediante RecetaInsumo" en el enunciado), la narrativa del proyecto no especifica un mecanismo de resolución para esta relación, ni los atributos sugeridos para `Promocion` incluyen una columna de conexión. Se optó por mantener la tabla `promocion` exactamente como fue especificada, sin agregar columnas ni tablas adicionales, respetando el modelo entregado de forma literal.
 
 ### 2. Creación de la base de datos de forma visual por MySQL Workbench

#### 2.1 Creación de la base de datos `hornoraiz_visual`

![Schema hornoraiz_visual creado](reporte/mysql-visual-01-schema.png)

**Resultado:** se creó el schema `hornoraiz_visual` dentro del EER Model de MySQL Workbench, como destino separado del `hornoraiz` ya evaluado en la Sección 1, para no sobrescribir esa evidencia.

#### 2.2 Creación de la tabla `producto`

![Columnas de producto configuradas en el editor](reporte/mysql-visual-02-producto-columnas.png)

**Script SQL generado por el modelo:**

![Script CREATE TABLE producto generado](reporte/mysql-visual-02-producto-script.png)

**Evidencia de la creación (Forward Engineer):**

![SHOW TABLES tras crear producto](reporte/mysql-visual-02-producto-show-tables.png)

**Resultado:** se cargaron las columnas `id` (PK, AI), `sku` (UQ), `nombre`, `descripcion`, `precio` y `is_active` (default `1`), replicando exactamente el `CREATE TABLE producto` de la Sección 1. La evidencia de creación real contra el servidor se documenta al final de esta sección, junto con el Forward Engineer de las 10 tablas.

#### 2.3 Creación de la tabla `insumo`

![Columnas de insumo configuradas en el editor](reporte/mysql-visual-03-insumo-columnas.png)

**Script SQL generado por el modelo:**

![Script CREATE TABLE insumo generado](reporte/mysql-visual-03-insumo-script.png)

**Evidencia de la creación (Forward Engineer):**

![SHOW TABLES tras crear insumo](reporte/mysql-visual-03-insumo-show-tables.png)

**Resultado:** se cargaron las columnas `id` (PK, AI), `codigo` (UQ), `nombre`, `unidad_medida`, `stock_minimo` (default `0`) e `is_active` (default `1`), replicando exactamente el `CREATE TABLE insumo` de la Sección 1. Se ejecutó el Forward Engineer individual para esta tabla, y `SHOW TABLES` sobre `hornoraiz_visual` confirma ambas tablas creadas hasta el momento (`producto`, `insumo`).

#### 2.4 Creación de la tabla `receta`

![Columnas de receta configuradas en el editor](reporte/mysql-visual-04-receta-columnas.png)

**Script SQL generado por el modelo:**

![Script CREATE TABLE receta generado](reporte/mysql-visual-04-receta-script.png)

**Evidencia de la creación (Forward Engineer):**

![SHOW TABLES tras crear receta](reporte/mysql-visual-04-receta-show-tables.png)

**Resultado:** se cargaron las columnas replicando el `CREATE TABLE receta` de la Sección 1, incluyendo la cláusula `ON UPDATE CURRENT_TIMESTAMP` en `updated_at`. Se definió la Foreign Key `producto_id → producto(id)`, visible como conector en el diagrama EER. Se ejecutó el Forward Engineer individual y `SHOW TABLES` sobre `hornoraiz_visual` confirma tres tablas creadas hasta el momento (`producto`, `insumo`, `receta`).

#### 2.5 Creación de la tabla `receta_insumo`

![Columnas de receta_insumo configuradas en el editor](reporte/mysql-visual-05-receta_insumo-columnas.png)

**Script SQL generado por el modelo:**

![Script CREATE TABLE receta_insumo generado](reporte/mysql-visual-05-receta_insumo-script.png)

**Evidencia de la creación (Forward Engineer):**

![SHOW TABLES tras crear receta_insumo](reporte/mysql-visual-05-receta_insumo-show-tables.png)

**Resultado:** se cargaron las columnas y las dos Foreign Keys (`principal_id → receta`, `relacionado_id → insumo`), resolviendo la relación `Receta N:M Insumo` del enunciado, igual que en la Sección 1. Se ejecutó el Forward Engineer individual y `SHOW TABLES` sobre `hornoraiz_visual` confirma cuatro tablas creadas hasta el momento.

#### 2.6 Creación de la tabla `lote_produccion`

![Columnas de lote_produccion configuradas en el editor](reporte/mysql-visual-06-lote_produccion-columnas.png)

**Script SQL generado por el modelo:**

![Script CREATE TABLE lote_produccion generado](reporte/mysql-visual-06-lote_produccion-script.png)

**Evidencia de la creación (Forward Engineer):**

![SHOW TABLES tras crear lote_produccion](reporte/mysql-visual-06-lote_produccion-show-tables.png)

**Resultado:** se cargaron las columnas y la Foreign Key `receta_id → receta(id)`, incluyendo `ON UPDATE CURRENT_TIMESTAMP` en `updated_at` desde la primera configuración. Se ejecutó el Forward Engineer individual y `SHOW TABLES` sobre `hornoraiz_visual` confirma cinco tablas creadas hasta el momento.

#### 2.7 Creación de la tabla `movimiento_insumo`

![Columnas de movimiento_insumo configuradas en el editor](reporte/mysql-visual-07-movimiento_insumo-columnas.png)

**Script SQL generado por el modelo:**

![Script CREATE TABLE movimiento_insumo generado](reporte/mysql-visual-07-movimiento_insumo-script.png)

**Evidencia de la creación (Forward Engineer):**

![SHOW TABLES tras crear movimiento_insumo](reporte/mysql-visual-07-movimiento_insumo-show-tables.png)

**Resultado:** se cargaron las columnas y las dos Foreign Keys (`lote_produccion_id → lote_produccion`, nullable; `insumo_id → insumo`, obligatoria), replicando exactamente el `CREATE TABLE movimiento_insumo` de la Sección 1. Se ejecutó el Forward Engineer individual y `SHOW TABLES` sobre `hornoraiz_visual` confirma seis tablas creadas hasta el momento.

#### 2.8 Creación de la tabla `venta`

![Columnas de venta configuradas en el editor](reporte/mysql-visual-08-venta-columnas.png)

**Script SQL generado por el modelo:**

![Script CREATE TABLE venta generado](reporte/mysql-visual-08-venta-script.png)

**Evidencia de la creación (Forward Engineer):**

![SHOW TABLES tras crear venta](reporte/mysql-visual-08-venta-show-tables.png)

**Resultado:** se cargaron las columnas sin Foreign Key (`cliente_id` queda como columna simple, sin tabla `Cliente` en el modelo de 10 tablas). Se ejecutó el Forward Engineer individual y `SHOW TABLES` sobre `hornoraiz_visual` confirma siete tablas creadas hasta el momento.

#### 2.9 Creación de la tabla `venta_detalle`

![Columnas de venta_detalle configuradas en el editor](reporte/mysql-visual-09-venta_detalle-columnas.png)

**Script SQL generado por el modelo:**

![Script CREATE TABLE venta_detalle generado](reporte/mysql-visual-09-venta_detalle-script.png)

**Evidencia de la creación (Forward Engineer):**

![SHOW TABLES tras crear venta_detalle](reporte/mysql-visual-09-venta_detalle-show-tables.png)

**Resultado:** se cargaron las columnas y las dos Foreign Keys (`cabecera_id → venta`, `item_id → producto`), replicando exactamente el `CREATE TABLE venta_detalle` de la Sección 1. Se ejecutó el Forward Engineer individual y `SHOW TABLES` sobre `hornoraiz_visual` confirma ocho tablas creadas hasta el momento.

#### 2.10 Creación de la tabla `pago`

![Columnas de pago configuradas en el editor](reporte/mysql-visual-10-pago-columnas.png)

**Script SQL generado por el modelo:**

![Script CREATE TABLE pago generado](reporte/mysql-visual-10-pago-script.png)

**Evidencia de la creación (Forward Engineer):**

![SHOW TABLES tras crear pago](reporte/mysql-visual-10-pago-show-tables.png)

**Resultado:** se cargaron las columnas sin Foreign Key — `referencia_id` es polimórfica (puede apuntar a distintas entidades según `referencia_tipo`), igual que en la Sección 1. Se ejecutó el Forward Engineer individual y `SHOW TABLES` sobre `hornoraiz_visual` confirma nueve tablas creadas hasta el momento.

#### 2.11 Creación de la tabla `promocion`

![Columnas de promocion configuradas en el editor](reporte/mysql-visual-11-promocion-columnas.png)

**Script SQL generado por el modelo:**

![Script CREATE TABLE promocion generado](reporte/mysql-visual-11-promocion-script.png)

**Evidencia de la creación (Forward Engineer):**

![SHOW TABLES tras crear promocion](reporte/mysql-visual-11-promocion-show-tables.png)

**Resultado:** se cargaron las columnas sin ninguna Foreign Key ni conector en el diagrama, respetando la misma decisión documentada en la Sección 1 para la relación `Promocion N:M Producto`. Se ejecutó el Forward Engineer individual.

#### 2.12 Verificación final

**Diagrama EER obtenido por Reverse Engineer desde `hornoraiz_visual`:**

![Diagrama EER reverse-engineered — 10 tablas](reporte/mysql-visual-12-diagrama-eer.png)

![SHOW TABLES final sobre hornoraiz_visual — 10 tablas](reporte/mysql-visual-12-show-tables-final.png)

**Resultado:** para verificar que el modelo construido manualmente en Workbench (Secciones 2.1 a 2.11) coincide con lo realmente creado en el servidor, se generó un diagrama EER por Reverse Engineer directamente desde `hornoraiz_visual`. El resultado confirma las 10 tablas y las 8 relaciones esperadas, con `promocion` sin ningún conector, tal como fue definido. `SHOW TABLES` confirma las mismas 10 tablas, idénticas en nombre a las de la Sección 1.
#### Conclusión

Con esto se finaliza la creación de la base de datos `hornoraiz` de forma visual en MySQL Workbench, replicando exactamente las 10 tablas, las 8 relaciones (todas menos `promocion`, sin conector por decisión ya documentada) y los tipos de datos definidos en la Sección 1, verificado tabla por tabla mediante Forward Engineer individual según lo exigido por el docente.

## 2. Base de Datos PostgreSQL

### 2.1 Limpieza de tablas existentes

```sql
DROP TABLE IF EXISTS venta_detalle;
DROP TABLE IF EXISTS pago;
DROP TABLE IF EXISTS venta;
DROP TABLE IF EXISTS movimiento_insumo;
DROP TABLE IF EXISTS lote_produccion;
DROP TABLE IF EXISTS receta_insumo;
DROP TABLE IF EXISTS receta;
DROP TABLE IF EXISTS promocion_producto;
DROP TABLE IF EXISTS promocion;
DROP TABLE IF EXISTS insumo;
DROP TABLE IF EXISTS producto;
```

**Evidencia (imagen):**

![Tablas eliminadas correctamente en PostgreSQL](reporte/postgres-01-tablas-eliminadas.png)

**Resultado:** se ejecutó el script completo con `Alt+X`. Se incluyó `promocion_producto`, una tabla puente residual de una instalación previa del motor que no forma parte del modelo de 10 tablas. Todas las tablas quedaron eliminadas sin errores de dependencia, respetando el orden inverso de las Foreign Keys.

### 2.2 Función `actualizar_updated_at`

```sql
CREATE FUNCTION actualizar_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

**Resultado:** se creó una función reutilizable que replica el comportamiento de `ON UPDATE CURRENT_TIMESTAMP` de MySQL, ya que PostgreSQL no tiene un equivalente directo en la definición de columna. Esta función se asocia mediante triggers `BEFORE UPDATE` a cada tabla que lo requiera (`receta`, `lote_produccion`, `promocion`).

### 2.3 Creación de la tabla `producto`

```sql
CREATE TABLE producto (
  id SERIAL PRIMARY KEY,
  sku VARCHAR(50) NOT NULL UNIQUE,
  nombre VARCHAR(100) NOT NULL,
  descripcion VARCHAR(255),
  precio DECIMAL(10,2) NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE
);
```

**Evidencia (imagen):**

![Tabla producto creada en PostgreSQL](reporte/postgres-03-tabla-producto.png)

**Resultado:** la tabla se creó sin errores (`Execute time: 0,071s`).

### 2.4 Creación de la tabla `insumo`

```sql
CREATE TABLE insumo (
  id SERIAL PRIMARY KEY,
  codigo VARCHAR(50) NOT NULL UNIQUE,
  nombre VARCHAR(100) NOT NULL,
  unidad_medida VARCHAR(30) NOT NULL,
  stock_minimo DECIMAL(10,2) NOT NULL DEFAULT 0,
  is_active BOOLEAN NOT NULL DEFAULT TRUE
);
```

**Evidencia (imagen):**

![Tabla insumo creada en PostgreSQL](reporte/postgres-04-tabla-insumo.png)

**Resultado:** la tabla se creó sin errores (`Execute time: 0,021s`).

### 2.5 Creación de la tabla `receta`

```sql
CREATE TABLE receta (
  id SERIAL PRIMARY KEY,
  producto_id INT NOT NULL REFERENCES producto(id),
  nombre VARCHAR(100) NOT NULL,
  descripcion VARCHAR(255),
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_receta_updated_at
  BEFORE UPDATE ON receta
  FOR EACH ROW EXECUTE FUNCTION actualizar_updated_at();
```

**Evidencia (imagen):**

![Tabla receta y trigger creados en PostgreSQL](reporte/postgres-05-tabla-receta.png)

**Verificación del trigger:**

![Prueba de INSERT y UPDATE mostrando el cambio de updated_at](reporte/postgres-05-receta-trigger-test.png)

**Resultado:** la tabla se creó sin errores, respetando la Foreign Key hacia `producto`. Se verificó el trigger `trg_receta_updated_at` mediante una fila de prueba: tras un `UPDATE`, `updated_at` cambió de `06:00:52.015` a `06:01:39` mientras `created_at` permaneció igual, confirmando el equivalente funcional de `ON UPDATE CURRENT_TIMESTAMP` de MySQL. La fila de prueba fue eliminada después de la verificación.

### 2.6 Creación de la tabla `receta_insumo`

```sql
CREATE TABLE receta_insumo (
  id SERIAL PRIMARY KEY,
  principal_id INT NOT NULL REFERENCES receta(id),
  relacionado_id INT NOT NULL REFERENCES insumo(id),
  datos_relacion VARCHAR(255),
  is_active BOOLEAN NOT NULL DEFAULT TRUE
);
```

**Evidencia (imagen):**

![Tabla receta_insumo creada en PostgreSQL](reporte/postgres-06-tabla-receta-insumo.png)

**Resultado:** la tabla se creó sin errores (`Execute time: 0,077s`), resolviendo la relación N:M entre `receta` e `insumo`, igual que en la Sección 1 de MySQL.

### 2.7 Creación de la tabla `lote_produccion`

```sql
CREATE TABLE lote_produccion (
  id SERIAL PRIMARY KEY,
  receta_id INT NOT NULL REFERENCES receta(id),
  nombre VARCHAR(100) NOT NULL,
  descripcion VARCHAR(255),
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_lote_produccion_updated_at
  BEFORE UPDATE ON lote_produccion
  FOR EACH ROW EXECUTE FUNCTION actualizar_updated_at();
```

**Evidencia (imagen):**

![Tabla lote_produccion y trigger creados en PostgreSQL](reporte/postgres-07-tabla-lote-produccion.png)

**Resultado:** la tabla se creó sin errores (`Execute time: 0,036s`), reutilizando la función `actualizar_updated_at()` ya verificada en `receta` para el mismo comportamiento de `updated_at` automático.

### 2.8 Creación de la tabla `movimiento_insumo`

```sql
CREATE TABLE movimiento_insumo (
  id SERIAL PRIMARY KEY,
  lote_produccion_id INT REFERENCES lote_produccion(id),
  insumo_id INT NOT NULL REFERENCES insumo(id),
  tipo VARCHAR(50) NOT NULL,
  fecha TIMESTAMP NOT NULL,
  cantidad DECIMAL(10,2) NOT NULL,
  observaciones TEXT,
  estado VARCHAR(30) NOT NULL
);
```

**Evidencia (imagen):**

![Tabla movimiento_insumo creada en PostgreSQL](reporte/postgres-08-tabla-movimiento-insumo.png)

**Resultado:** la tabla se creó sin errores (`Execute time: 0,02s`), con `lote_produccion_id` nullable, igual que en la Sección 1 de MySQL.

### 2.9 Creación de la tabla `venta`

```sql
CREATE TABLE venta (
  id SERIAL PRIMARY KEY,
  cliente_id INT,
  fecha TIMESTAMP NOT NULL,
  subtotal DECIMAL(10,2) NOT NULL,
  impuestos DECIMAL(10,2) NOT NULL DEFAULT 0,
  total DECIMAL(10,2) NOT NULL,
  estado VARCHAR(30) NOT NULL
);
```

**Evidencia (imagen):**

![Tabla venta creada en PostgreSQL](reporte/postgres-09-tabla-venta.png)

**Resultado:** la tabla se creó sin errores (`Execute time: 0,01s`), sin Foreign Key para `cliente_id` — no existe una entidad `Cliente` en el modelo de 10 tablas, mismo criterio aplicado en la Sección 1 y en MySQL Workbench.

### 2.10 Creación de la tabla `venta_detalle`

```sql
CREATE TABLE venta_detalle (
  id SERIAL PRIMARY KEY,
  cabecera_id INT NOT NULL REFERENCES venta(id),
  item_id INT NOT NULL REFERENCES producto(id),
  cantidad DECIMAL(10,2) NOT NULL,
  valor_unitario DECIMAL(10,2) NOT NULL,
  total DECIMAL(10,2) NOT NULL,
  observaciones TEXT
);
```

**Evidencia (imagen):**

![Tabla venta_detalle creada en PostgreSQL](reporte/postgres-10-tabla-venta-detalle.png)

**Resultado:** la tabla se creó sin errores (`Execute time: 0,013s`), con las Foreign Keys `cabecera_id → venta` e `item_id → producto`, igual que en la Sección 1 de MySQL.

### 2.11 Creación de la tabla `pago`

```sql
CREATE TABLE pago (
  id SERIAL PRIMARY KEY,
  referencia_tipo VARCHAR(50) NOT NULL,
  referencia_id INT NOT NULL,
  metodo VARCHAR(50) NOT NULL,
  monto DECIMAL(10,2) NOT NULL,
  fecha TIMESTAMP NOT NULL,
  estado VARCHAR(30) NOT NULL
);
```

**Evidencia (imagen):**

![Tabla pago creada en PostgreSQL](reporte/postgres-11-tabla-pago.png)

**Resultado:** la tabla se creó sin errores (`Execute time: 0,015s`), sin Foreign Key — `referencia_id` es polimórfica, igual que en la Sección 1 de MySQL.

### 2.12 Creación de la tabla `promocion`

```sql
CREATE TABLE promocion (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  descripcion VARCHAR(255),
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_promocion_updated_at
  BEFORE UPDATE ON promocion
  FOR EACH ROW EXECUTE FUNCTION actualizar_updated_at();
```

**Evidencia (imagen):**

![Tabla promocion y trigger creados en PostgreSQL](reporte/postgres-12-tabla-promocion.png)

**Resultado:** la tabla se creó sin errores (`Execute time: 0,083s`), sin ninguna Foreign Key ni tabla puente para la relación `Promocion N:M Producto`, respetando la misma decisión documentada en la Sección 1 de MySQL.

### 2.13 Verificación final

```sql
SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;
```

**Evidencia (imagen):**

![Verificación final de las 10 tablas en PostgreSQL](reporte/postgres-13-verificacion-final.png)

**Resultado:** la consulta devolvió las 10 tablas esperadas (`insumo`, `lote_produccion`, `movimiento_insumo`, `pago`, `producto`, `promocion`, `receta`, `receta_insumo`, `venta`, `venta_detalle`), confirmando que el modelo quedó completo, sin la tabla puente `promocion_producto` que existía por instalación previa.

#### Conclusión

Con esto se finaliza la creación de la base de datos `hornoraiz` en PostgreSQL mediante código SQL en DBeaver. A diferencia de MySQL, fue necesario implementar una función y triggers (`actualizar_updated_at`) para replicar el comportamiento de `ON UPDATE CURRENT_TIMESTAMP`, verificado mediante pruebas de INSERT/UPDATE sobre `receta`. Con esto queda cerrada la Sección 2.1 (código); en la Sección 2.2 se recreará el mismo modelo de forma visual usando pgAdmin 4.

#### 3.2 Creación de la tabla `producto`

![Columnas de producto configuradas en pgAdmin](reporte/postgres-visual-02-producto-columnas.png)

**Script SQL generado por pgAdmin:**

![Script CREATE TABLE producto generado](reporte/postgres-visual-02-producto-script.png)

**Evidencia de la creación:**

![Consulta pg_tables confirmando producto creada](reporte/postgres-visual-02-producto-tablas.png)

**Resultado:** se creó la tabla `producto` mediante la interfaz gráfica de pgAdmin (diálogo Create-Table), sin escribir SQL manualmente. El script generado coincide con el `CREATE TABLE producto` de la Sección 2.1 (código), incluyendo la restricción `UNIQUE` sobre `sku`.

#### 3.3 Creación de la tabla `insumo`

![Columnas de insumo configuradas en pgAdmin](reporte/postgres-visual-03-insumo-columnas.png)

**Script SQL generado por pgAdmin:**

![Script CREATE TABLE insumo generado](reporte/postgres-visual-03-insumo-script.png)

**Evidencia de la creación:**

![Consulta pg_tables confirmando insumo creada](reporte/postgres-visual-03-insumo-tablas.png)

**Resultado:** se creó la tabla `insumo` mediante pgAdmin, con la restricción `UNIQUE` correctamente aplicada sobre `codigo` (corregida de un intento inicial que la había apuntado por error a `stock_minimo`). Coincide con el `CREATE TABLE insumo` de la Sección 2.1.

#### 3.4 Creación de la tabla `receta`

![Columnas y Foreign Key de receta configuradas en pgAdmin](reporte/postgres-visual-04-receta-columnas.png)

**Script SQL generado por pgAdmin:**

![Script CREATE TABLE receta generado](reporte/postgres-visual-04-receta-script.png)

**Trigger aplicado:**

![CREATE TRIGGER trg_receta_updated_at ejecutado sin errores](reporte/postgres-visual-04-receta-trigger.png)

**Evidencia de la creación:**

![Consulta pg_tables confirmando receta creada](reporte/postgres-visual-04-receta-tablas.png)

**Resultado:** se creó la tabla `receta` mediante pgAdmin, con la Foreign Key hacia `producto` y el trigger `trg_receta_updated_at`, reutilizando la función `actualizar_updated_at()` ya existente en este servidor local. Coincide con el `CREATE TABLE receta` de la Sección 2.1.

#### 3.5 Creación de la tabla `receta_insumo`

![Columnas y Foreign Keys de receta_insumo configuradas en pgAdmin](reporte/postgres-visual-05-receta_insumo-columnas.png)

**Script SQL generado por pgAdmin:**

![Script CREATE TABLE receta_insumo generado](reporte/postgres-visual-05-receta_insumo-script.png)

**Evidencia de la creación:**

![Consulta pg_tables confirmando receta_insumo creada](reporte/postgres-visual-05-receta_insumo-tablas.png)

**Resultado:** se creó la tabla `receta_insumo` mediante pgAdmin, resolviendo la relación N:M entre `receta` e `insumo` con las Foreign Keys `principal_id` y `relacionado_id`. Se corrigió un error de tecleo inicial (`datos_relacionado` → `datos_relacion`) antes del cierre. Coincide con el `CREATE TABLE receta_insumo` de la Sección 2.1.

#### 3.6 Creación de la tabla `lote_produccion`

![Columnas y Foreign Key de lote_produccion configuradas en pgAdmin](reporte/postgres-visual-06-lote_produccion-columnas.png)

**Script SQL generado por pgAdmin:**

![Script CREATE TABLE lote_produccion generado](reporte/postgres-visual-06-lote-produccion-script.png)

**Trigger aplicado:**

![CREATE TRIGGER trg_lote_produccion_updated_at ejecutado sin errores](reporte/postgres-visual-06-lote_produccion-trigger.png)

**Evidencia de la creación:**

![Consulta pg_tables confirmando lote_produccion creada](reporte/postgres-visual-06-lote_produccion-tablas.png)

**Resultado:** se creó la tabla `lote_produccion` mediante pgAdmin, con la Foreign Key hacia `receta` y el trigger `trg_lote_produccion_updated_at`, reutilizando la función `actualizar_updated_at()`. Se corrigió `descripcion` (faltaba la longitud `255`) antes del cierre. Coincide con el `CREATE TABLE lote_produccion` de la Sección 2.1.

#### 3.7 Creación de la tabla `movimiento_insumo`

![Columnas y Foreign Keys de movimiento_insumo configuradas en pgAdmin](reporte/postgres-visual-07-movimiento_insumo-columnas.png)

**Script SQL generado por pgAdmin:**

![Script CREATE TABLE movimiento_insumo generado](reporte/postgres-visual-07-movimiento_insumo-script.png)

**Evidencia de la creación:**

![Consulta pg_tables confirmando movimiento_insumo creada](reporte/postgres-visual-07-movimiento_insumo-tablas.png)

**Resultado:** se creó la tabla `movimiento_insumo` mediante pgAdmin, con `lote_produccion_id` nullable y ambas Foreign Keys resueltas correctamente. Coincide con el `CREATE TABLE movimiento_insumo` de la Sección 2.1.

#### 3.8 Creación de la tabla `venta`

![Columnas de venta configuradas en pgAdmin](reporte/postgres-visual-08-venta-columnas.png)

**Script SQL generado por pgAdmin:**

![Script CREATE TABLE venta generado](reporte/postgres-visual-08-venta-script.png)

**Evidencia de la creación:**

![Consulta pg_tables confirmando venta creada](reporte/postgres-visual-08-venta-tablas.png)

**Resultado:** se creó la tabla `venta` mediante pgAdmin, sin Foreign Key para `cliente_id` — no existe una entidad `Cliente` en el modelo de 10 tablas, mismo criterio aplicado en la Sección 2.1. Coincide con el `CREATE TABLE venta` de la Sección 1 de MySQL.

#### 3.9 Creación de la tabla `venta_detalle`

![Columnas y Foreign Keys de venta_detalle configuradas en pgAdmin](reporte/postgres-visual-09-venta_detalle-columnas.png)

**Script SQL generado por pgAdmin:**

![Script CREATE TABLE venta_detalle generado](reporte/postgres-visual-09-venta_detalle-script.png)

**Evidencia de la creación:**

![Consulta pg_tables confirmando venta_detalle creada](reporte/postgres-visual-09-venta_detalle-tablas.png)

**Resultado:** se creó la tabla `venta_detalle` mediante pgAdmin, con las Foreign Keys `cabecera_id → venta` e `item_id → producto`. Coincide con el `CREATE TABLE venta_detalle` de la Sección 2.1.

#### 3.10 Creación de la tabla `pago`

![Columnas de pago configuradas en pgAdmin](reporte/postgres-visual-10-pago-columnas.png)

**Script SQL generado por pgAdmin:**

![Script CREATE TABLE pago generado](reporte/postgres-visual-10-pago-script.png)

**Evidencia de la creación:**

![Consulta pg_tables confirmando pago creada](reporte/postgres-visual-10-pago-tablas.png)

**Resultado:** se creó la tabla `pago` mediante pgAdmin, sin Foreign Key — `referencia_id` es polimórfica, igual que en la Sección 2.1.

#### 3.11 Creación de la tabla `promocion`

![Columnas de promocion configuradas en pgAdmin](reporte/postgres-visual-11-promocion-columnas.png)

**Script SQL generado por pgAdmin:**

![Script CREATE TABLE promocion generado](reporte/postgres-visual-11-promocion-script.png)

**Trigger aplicado:**

![CREATE TRIGGER trg_promocion_updated_at ejecutado sin errores](reporte/postgres-visual-11-promocion-trigger.png)

**Evidencia de la creación:**

![Consulta pg_tables confirmando promocion creada](reporte/postgres-visual-11-promocion-tablas.png)

**Resultado:** se creó la tabla `promocion` mediante pgAdmin, sin ninguna Foreign Key ni tabla puente para la relación `Promocion N:M Producto`, con el trigger `trg_promocion_updated_at` reutilizando la función `actualizar_updated_at()`. Respeta la misma decisión documentada en la Sección 1 de MySQL.

#### 3.12 Verificación final

**Diagrama ERD obtenido desde `hornoraiz_visual` (pgAdmin ERD Tool):**

![Diagrama ERD generado por pgAdmin — 10 tablas](reporte/postgres-visual-12-diagrama-erd.png)

![Consulta pg_tables final confirmando las 10 tablas](reporte/postgres-visual-12-verificacion-final.png)

**Resultado:** para verificar que el modelo construido manualmente en pgAdmin (Secciones 3.1 a 3.11) coincide con lo realmente creado en el servidor, se generó un diagrama ERD directamente desde `hornoraiz_visual`. El resultado confirma las 10 tablas y las 8 relaciones esperadas, con `promocion` sin ningún conector, tal como fue definido. `pg_tables` confirma las mismas 10 tablas, idénticas en nombre a las de la Sección 2.1.

## 4. Base de Datos SQL Server

### 4.1 Limpieza de tablas existentes

```sql
USE master;
GO
ALTER DATABASE hornoraiz SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
GO
DROP DATABASE hornoraiz;
GO
CREATE DATABASE hornoraiz;
GO
USE hornoraiz;
GO
```

**Evidencia (imagen):**

![Base de datos recreada correctamente en SQL Server](reporte/mssql-01-base-recreada.png)

**Resultado:** se optó por eliminar y recrear la base de datos completa (`DROP DATABASE` / `CREATE DATABASE`) en vez de borrar tabla por tabla, ya que la base traía 11 tablas residuales de la instalación previa del motor, incluyendo una tabla puente `promocion_producto` que no forma parte del modelo. Fue necesario `ALTER DATABASE ... SET SINGLE_USER WITH ROLLBACK IMMEDIATE` para forzar el cierre de sesiones activas antes del `DROP`.

### 4.2 Creación de la tabla `producto`

```sql
CREATE TABLE producto (
  id INT IDENTITY(1,1) PRIMARY KEY,
  sku VARCHAR(50) NOT NULL UNIQUE,
  nombre VARCHAR(100) NOT NULL,
  descripcion VARCHAR(255),
  precio DECIMAL(10,2) NOT NULL,
  is_active BIT NOT NULL DEFAULT 1
);
```

**Evidencia (imagen):**

![Tabla producto creada en SQL Server](reporte/mssql-02-tabla-producto.png)

**Resultado:** la tabla se creó sin errores.

### 4.3 Creación de la tabla `insumo`

```sql
CREATE TABLE insumo (
  id INT IDENTITY(1,1) PRIMARY KEY,
  codigo VARCHAR(50) NOT NULL UNIQUE,
  nombre VARCHAR(100) NOT NULL,
  unidad_medida VARCHAR(30) NOT NULL,
  stock_minimo DECIMAL(10,2) NOT NULL DEFAULT 0,
  is_active BIT NOT NULL DEFAULT 1
);
```

**Evidencia (imagen):**

![Tabla insumo creada en SQL Server](reporte/mssql-03-tabla-insumo.png)

**Resultado:** la tabla se creó sin errores.

### 4.4 Creación de la tabla `receta`

```sql
CREATE TABLE receta (
  id INT IDENTITY(1,1) PRIMARY KEY,
  producto_id INT NOT NULL REFERENCES producto(id),
  nombre VARCHAR(100) NOT NULL,
  descripcion VARCHAR(255),
  is_active BIT NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT GETDATE(),
  updated_at DATETIME NOT NULL DEFAULT GETDATE()
);
GO

CREATE TRIGGER trg_receta_updated_at
ON receta
AFTER UPDATE
AS
BEGIN
  UPDATE receta
  SET updated_at = GETDATE()
  FROM receta
  INNER JOIN inserted ON receta.id = inserted.id;
END;
GO
```

**Evidencia (imagen):**

![Tabla receta y trigger creados en SQL Server](reporte/mssql-04-tabla-receta.png)

**Resultado:** la tabla se creó sin errores, con la Foreign Key hacia `producto` y el trigger `trg_receta_updated_at` (`AFTER UPDATE`, ya que SQL Server no soporta `BEFORE UPDATE` como PostgreSQL), replicando el equivalente funcional de `ON UPDATE CURRENT_TIMESTAMP` de MySQL.

### 4.5 Creación de la tabla `receta_insumo`

```sql
CREATE TABLE receta_insumo (
  id INT IDENTITY(1,1) PRIMARY KEY,
  principal_id INT NOT NULL REFERENCES receta(id),
  relacionado_id INT NOT NULL REFERENCES insumo(id),
  datos_relacion VARCHAR(255),
  is_active BIT NOT NULL DEFAULT 1
);
```

**Evidencia (imagen):**

![Tabla receta_insumo creada en SQL Server](reporte/mssql-05-tabla-receta-insumo.png)

**Resultado:** la tabla se creó sin errores, resolviendo la relación N:M entre `receta` e `insumo` con las Foreign Keys `principal_id` y `relacionado_id`.

### 4.6 Creación de la tabla `lote_produccion`

```sql
CREATE TABLE lote_produccion (
  id INT IDENTITY(1,1) PRIMARY KEY,
  receta_id INT NOT NULL REFERENCES receta(id),
  nombre VARCHAR(100) NOT NULL,
  descripcion VARCHAR(255),
  is_active BIT NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT GETDATE(),
  updated_at DATETIME NOT NULL DEFAULT GETDATE()
);
GO

CREATE TRIGGER trg_lote_produccion_updated_at
ON lote_produccion
AFTER UPDATE
AS
BEGIN
  UPDATE lote_produccion
  SET updated_at = GETDATE()
  FROM lote_produccion
  INNER JOIN inserted ON lote_produccion.id = inserted.id;
END;
GO
```

**Evidencia (imagen):**

![Tabla lote_produccion y trigger creados en SQL Server](reporte/mssql-06-tabla-lote-produccion.png)

**Resultado:** la tabla se creó sin errores, con la Foreign Key hacia `receta` y el trigger `trg_lote_produccion_updated_at`.

### 4.7 Creación de la tabla `movimiento_insumo`

```sql
CREATE TABLE movimiento_insumo (
  id INT IDENTITY(1,1) PRIMARY KEY,
  lote_produccion_id INT REFERENCES lote_produccion(id),
  insumo_id INT NOT NULL REFERENCES insumo(id),
  tipo VARCHAR(50) NOT NULL,
  fecha DATETIME NOT NULL,
  cantidad DECIMAL(10,2) NOT NULL,
  observaciones VARCHAR(MAX),
  estado VARCHAR(30) NOT NULL
);
```

**Evidencia (imagen):**

![Tabla movimiento_insumo creada en SQL Server](reporte/mssql-07-tabla-movimiento-insumo.png)

**Resultado:** la tabla se creó sin errores, con `lote_produccion_id` nullable y ambas Foreign Keys resueltas correctamente. Se usó `VARCHAR(MAX)` como equivalente de `TEXT`, ya que este último tipo está deprecado en SQL Server.

### 4.8 Creación de la tabla `venta`

```sql
CREATE TABLE venta (
  id INT IDENTITY(1,1) PRIMARY KEY,
  cliente_id INT,
  fecha DATETIME NOT NULL,
  subtotal DECIMAL(10,2) NOT NULL,
  impuestos DECIMAL(10,2) NOT NULL DEFAULT 0,
  total DECIMAL(10,2) NOT NULL,
  estado VARCHAR(30) NOT NULL
);
```

**Evidencia (imagen):**

![Tabla venta creada en SQL Server](reporte/mssql-08-tabla-venta.png)

**Resultado:** la tabla se creó sin errores, sin Foreign Key para `cliente_id` — no existe una entidad `Cliente` en el modelo de 10 tablas, mismo criterio aplicado en los demás motores.

### 4.9 Creación de la tabla `venta_detalle`

```sql
CREATE TABLE venta_detalle (
  id INT IDENTITY(1,1) PRIMARY KEY,
  cabecera_id INT NOT NULL REFERENCES venta(id),
  item_id INT NOT NULL REFERENCES producto(id),
  cantidad DECIMAL(10,2) NOT NULL,
  valor_unitario DECIMAL(10,2) NOT NULL,
  total DECIMAL(10,2) NOT NULL,
  observaciones VARCHAR(MAX)
);
```

**Evidencia (imagen):**

![Tabla venta_detalle creada en SQL Server](reporte/mssql-09-tabla-venta-detalle.png)

**Resultado:** la tabla se creó sin errores, con las Foreign Keys `cabecera_id → venta` e `item_id → producto`.

### 4.10 Creación de la tabla `pago`

```sql
CREATE TABLE pago (
  id INT IDENTITY(1,1) PRIMARY KEY,
  referencia_tipo VARCHAR(50) NOT NULL,
  referencia_id INT NOT NULL,
  metodo VARCHAR(50) NOT NULL,
  monto DECIMAL(10,2) NOT NULL,
  fecha DATETIME NOT NULL,
  estado VARCHAR(30) NOT NULL
);
```

**Evidencia (imagen):**

![Tabla pago creada en SQL Server](reporte/mssql-10-tabla-pago.png)

**Resultado:** la tabla se creó sin errores, sin Foreign Key — `referencia_id` es polimórfica, igual que en los demás motores.

### 4.11 Creación de la tabla `promocion`

```sql
CREATE TABLE promocion (
  id INT IDENTITY(1,1) PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  descripcion VARCHAR(255),
  is_active BIT NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT GETDATE(),
  updated_at DATETIME NOT NULL DEFAULT GETDATE()
);
GO

CREATE TRIGGER trg_promocion_updated_at
ON promocion
AFTER UPDATE
AS
BEGIN
  UPDATE promocion
  SET updated_at = GETDATE()
  FROM promocion
  INNER JOIN inserted ON promocion.id = inserted.id;
END;
GO
```

**Evidencia (imagen):**

![Tabla promocion y trigger creados en SQL Server](reporte/mssql-11-tabla-promocion.png)

**Resultado:** la tabla se creó sin errores, sin ninguna Foreign Key ni tabla puente para la relación `Promocion N:M Producto`, con el trigger `trg_promocion_updated_at`. Respeta la misma decisión documentada en los demás motores.

### 4.12 Verificación final

```sql
SELECT name FROM sys.tables ORDER BY name;
```

**Evidencia (imagen):**

![Verificación final de las 10 tablas en SQL Server](reporte/mssql-12-verificacion-final.png)

**Resultado:** la consulta devolvió las 10 tablas esperadas (`insumo`, `lote_produccion`, `movimiento_insumo`, `pago`, `producto`, `promocion`, `receta`, `receta_insumo`, `venta`, `venta_detalle`), confirmando que el modelo quedó completo, sin la tabla puente `promocion_producto` que existía por instalación previa.

#### Conclusión

Con esto se finaliza la creación de la base de datos `hornoraiz` en SQL Server mediante código SQL en DBeaver. A diferencia de MySQL y similar a PostgreSQL, fue necesario implementar triggers `AFTER UPDATE` (SQL Server no soporta `BEFORE UPDATE`) para replicar el comportamiento de `updated_at` automático en `receta`, `lote_produccion` y `promocion`. Con esto queda cerrada la Sección 4.1 (código); en la Sección 4.2 se recreará el mismo modelo de forma visual usando SQL Server Management Studio 20.

## 5. Base de Datos SQL Server — Parte Visual (SQL Server Management Studio)

### 5.1 Instalación y configuración

Se instaló **SQL Server 2025 Evaluation Edition** de forma local en Windows (instancia por defecto `MSSQLSERVER`, autenticación de Windows), junto con **SQL Server Management Studio** para la parte gráfica.

**Evidencia (imagen):**

![Instalación de SQL Server 2025 completada exitosamente](reporte/mssql-visual-00-instalacion.png)

**Nota metodológica:** al igual que en MySQL Workbench y pgAdmin 4, se optó por instalar el motor localmente en Windows en vez de conectar SSMS directamente al SQL Server de la VM, para mantener el mismo patrón de trabajo en los tres motores con parte visual.

### 5.2 Creación de la base de datos `hornoraiz_visual`

**Evidencia (imagen):**

![Base de datos hornoraiz_visual creada en SSMS](reporte/mssql-visual-01-database-creada.png)

**Resultado:** se creó la base de datos `hornoraiz_visual` mediante el asistente gráfico "Nueva base de datos" de SSMS, sin escribir código SQL, como destino separado de la base `hornoraiz` ya evaluada por código en la Sección 4.1.

### 5.3 Creación de la tabla `producto`

![Columnas de producto configuradas en SSMS](reporte/mssql-visual-02-producto-columnas.png)

**Configuración del índice único sobre `sku`:**

![Diálogo Índices o claves con UNIQUE en sku](reporte/mssql-visual-02-producto-indice.png)

**Script SQL generado por SSMS (Generar script de tabla como → CREATE To):**

![Script CREATE TABLE producto generado](reporte/mssql-visual-02-producto-script.png)

**Evidencia de la creación:**

![Consulta sys.tables confirmando producto creada](reporte/mssql-visual-02-producto-tablas.png)

**Resultado:** se creó la tabla `producto` mediante el Diseñador de tablas de SSMS, sin escribir SQL manualmente. El script generado coincide con el `CREATE TABLE producto` de la Sección 4.2 (código), incluyendo la restricción `UNIQUE` sobre `sku` — agregada tras la configuración inicial mediante el diálogo "Índices o claves...", motivo por el cual quedó como cláusula inline sin nombre explícito, a diferencia de `PK_producto` y `DF_producto_is_active`.

### 5.4 Creación de la tabla `insumo`

![Columnas de insumo configuradas en SSMS](reporte/mssql-visual-03-insumo-columnas.png)

**Script SQL generado por SSMS (Generar script de tabla como → CREATE To):**

![Script CREATE TABLE insumo generado](reporte/mssql-visual-03-insumo-script.png)

**Evidencia de la creación:**

![Consulta sys.tables confirmando insumo creada](reporte/mssql-visual-03-insumo-tablas.png)

**Resultado:** se creó la tabla `insumo` mediante el Diseñador de tablas de SSMS, sin escribir SQL manualmente. El script generado coincide con el `CREATE TABLE insumo` de la Sección 4.3 (código), incluyendo la restricción `UNIQUE` sobre `codigo` y los valores predeterminados `0` en `stock_minimo` y `1` en `is_active`. A diferencia de `producto`, el índice único quedó como cláusula inline desde el primer guardado, sin necesidad de una segunda pasada.

### 5.5 Creación de la tabla `receta`

![Columnas de receta configuradas en SSMS](reporte/mssql-visual-04-receta-columnas.png)

**Configuración de la Foreign Key hacia `producto` (diálogo "Relaciones..."):**

![Diálogo Tablas y columnas con FK_receta_producto](reporte/mssql-visual-04-receta-relaciones.png)

**Script SQL generado por SSMS (Generar script de tabla como → CREATE To):**

![Script CREATE TABLE receta generado](reporte/mssql-visual-04-receta-script.png)

**Nota metodológica — trigger `updated_at`:** SSMS no ofrece un diseñador gráfico para la creación de triggers, a diferencia de MySQL Workbench y pgAdmin, que sí permiten definirlos por diálogo. Por esta razón, y como excepción documentada dentro de esta sección visual, el trigger `trg_receta_updated_at` se creó escribiendo el código directamente en una nueva ventana de consulta contra `hornoraiz_visual`, mientras que la estructura de columnas, la Primary Key, la Foreign Key y los valores predeterminados de la tabla sí se configuraron íntegramente por diseñador, sin código.

```sql
CREATE TRIGGER trg_receta_updated_at
ON receta
AFTER UPDATE
AS
BEGIN
  UPDATE receta
  SET updated_at = GETDATE()
  FROM receta
  INNER JOIN inserted ON receta.id = inserted.id;
END;
```

![Ejecución del trigger trg_receta_updated_at sin errores](reporte/mssql-visual-04-receta-trigger.png)

**Evidencia de la creación:**

![Consulta sys.tables confirmando receta creada](reporte/mssql-visual-04-receta-tablas.png)

**Resultado:** se creó la tabla `receta` mediante el Diseñador de tablas de SSMS, con la Foreign Key hacia `producto` configurada mediante el diálogo "Relaciones...", y los valores predeterminados `1` en `is_active` y `getdate()` en `created_at`/`updated_at` configurados por diseñador. El trigger `trg_receta_updated_at` se creó por código, como excepción documentada ante la ausencia de un diseñador gráfico de triggers en SSMS. El script generado coincide con el `CREATE TABLE receta` de la Sección 4.4 (código), incluyendo `IDENTITY(1,1)` en `id`.

### 5.6 Creación de la tabla `receta_insumo`

![Columnas de receta_insumo configuradas en SSMS](reporte/mssql-visual-05-receta_insumo-columnas.png)

**Configuración de las Foreign Keys hacia `receta` e `insumo` (diálogo "Relaciones..."):**

![Diálogo Tablas y columnas con FK_receta_insumo_receta y FK_receta_insumo_insumo](reporte/mssql-visual-05-receta_insumo-relaciones.png)

**Script SQL generado por SSMS (Generar script de tabla como → CREATE To):**

![Script CREATE TABLE receta_insumo generado](reporte/mssql-visual-05-receta_insumo-script.png)

**Evidencia de la creación:**

![Consulta sys.tables confirmando receta_insumo creada](reporte/mssql-visual-05-receta_insumo-tablas.png)

**Resultado:** se creó la tabla `receta_insumo` mediante el Diseñador de tablas de SSMS, sin escribir SQL manualmente. Se configuraron dos Foreign Keys mediante el diálogo "Relaciones...": `principal_id → receta(id)` y `relacionado_id → insumo(id)`, resolviendo la relación N:M entre `receta` e `insumo`, igual que en los otros tres motores. El script generado coincide con el `CREATE TABLE receta_insumo` de la Sección 4.5 (código).

### 5.7 Creación de la tabla `lote_produccion`

![Columnas de lote_produccion configuradas en SSMS](reporte/mssql-visual-06-lote_produccion-columnas.png)

**Configuración de la Foreign Key hacia `receta` (diálogo "Relaciones..."):**

![Diálogo Tablas y columnas con FK_lote_produccion_receta](reporte/mssql-visual-06-lote_produccion-relaciones.png)

**Script SQL generado por SSMS (Generar script de tabla como → CREATE To):**

![Script CREATE TABLE lote_produccion generado](reporte/mssql-visual-06-lote_produccion-script.png)

**Nota metodológica — trigger `updated_at`:** al igual que en `receta` (Sección 5.5), SSMS no ofrece un diseñador gráfico para triggers, por lo que `trg_lote_produccion_updated_at` se creó por código en una nueva ventana de consulta contra `hornoraiz_visual`, mientras que la estructura de columnas, la Primary Key, la Foreign Key y los valores predeterminados sí se configuraron íntegramente por diseñador.

```sql
CREATE TRIGGER trg_lote_produccion_updated_at
ON lote_produccion
AFTER UPDATE
AS
BEGIN
  UPDATE lote_produccion
  SET updated_at = GETDATE()
  FROM lote_produccion
  INNER JOIN inserted ON lote_produccion.id = inserted.id;
END;
```

![Ejecución del trigger trg_lote_produccion_updated_at sin errores](reporte/mssql-visual-06-lote_produccion-trigger.png)

**Evidencia de la creación:**

![Consulta sys.tables confirmando lote_produccion creada](reporte/mssql-visual-06-lote_produccion-tablas.png)

**Resultado:** se creó la tabla `lote_produccion` mediante el Diseñador de tablas de SSMS, con la Foreign Key hacia `receta` configurada mediante el diálogo "Relaciones...", y los valores predeterminados `1` en `is_active` y `getdate()` en `created_at`/`updated_at` configurados por diseñador. El trigger `trg_lote_produccion_updated_at` se creó por código, como excepción documentada ante la ausencia de un diseñador gráfico de triggers en SSMS. El script generado coincide con el `CREATE TABLE lote_produccion` de la Sección 4.6 (código).


### 5.8 Creación de la tabla `movimiento_insumo`

![Columnas de movimiento_insumo configuradas en SSMS](reporte/mssql-visual-07-movimiento_insumo-columnas.png)

**Configuración de las Foreign Keys hacia `lote_produccion` e `insumo` (diálogo "Relaciones..."):**

![Diálogo Tablas y columnas con FK_movimiento_insumo_lote_produccion y FK_movimiento_insumo_insumo](reporte/mssql-visual-07-movimiento_insumo-relaciones.png)

**Script SQL generado por SSMS (Generar script de tabla como → CREATE To):**

![Script CREATE TABLE movimiento_insumo generado](reporte/mssql-visual-07-movimiento_insumo-script.png)

**Evidencia de la creación:**

![Consulta sys.tables confirmando movimiento_insumo creada](reporte/mssql-visual-07-movimiento_insumo-tablas.png)

**Resultado:** se creó la tabla `movimiento_insumo` mediante el Diseñador de tablas de SSMS, sin escribir SQL manualmente. Se configuraron dos Foreign Keys mediante el diálogo "Relaciones...": `lote_produccion_id → lote_produccion(id)` (nullable) e `insumo_id → insumo(id)` (obligatoria), replicando el `CREATE TABLE movimiento_insumo` de la Sección 4.7 (código), incluyendo `varchar(max)` en `observaciones` como equivalente de `TEXT`.

### 5.9 Creación de la tabla `venta`

![Columnas de venta configuradas en SSMS](reporte/mssql-visual-08-venta-columnas.png)

**Script SQL generado por SSMS (Generar script de tabla como → CREATE To):**

![Script CREATE TABLE venta generado](reporte/mssql-visual-08-venta-script.png)

**Evidencia de la creación:**

![Consulta sys.tables confirmando venta creada](reporte/mssql-visual-08-venta-tablas.png)

**Resultado:** se creó la tabla `venta` mediante el Diseñador de tablas de SSMS, sin escribir SQL manualmente, sin Foreign Key para `cliente_id` — no existe una entidad `Cliente` en el modelo de 10 tablas, mismo criterio aplicado en los demás motores. El script generado coincide con el `CREATE TABLE venta` de la Sección 4.8 (código), incluyendo el valor predeterminado `0` en `impuestos`.

### 5.10 Creación de la tabla `venta_detalle`

![Columnas de venta_detalle configuradas en SSMS](reporte/mssql-visual-09-venta_detalle-columnas.png)

**Configuración de las Foreign Keys hacia `venta` y `producto` (diálogo "Relaciones..."):**

![Diálogo Tablas y columnas con FK_venta_detalle_venta y FK_venta_detalle_producto](reporte/mssql-visual-09-venta_detalle-relaciones.png)

**Script SQL generado por SSMS (Generar script de tabla como → CREATE To):**

![Script CREATE TABLE venta_detalle generado](reporte/mssql-visual-09-venta_detalle-script.png)

**Evidencia de la creación:**

![Consulta sys.tables confirmando venta_detalle creada](reporte/mssql-visual-09-venta_detalle-tablas.png)

**Resultado:** se creó la tabla `venta_detalle` mediante el Diseñador de tablas de SSMS, sin escribir SQL manualmente. Se configuraron dos Foreign Keys mediante el diálogo "Relaciones...": `cabecera_id → venta(id)` e `item_id → producto(id)`, replicando el `CREATE TABLE venta_detalle` de la Sección 4.9 (código).

### 5.11 Creación de la tabla `pago`

![Columnas de pago configuradas en SSMS](reporte/mssql-visual-10-pago-columnas.png)

**Script SQL generado por SSMS (Generar script de tabla como → CREATE To):**

![Script CREATE TABLE pago generado](reporte/mssql-visual-10-pago-script.png)

**Evidencia de la creación:**

![Consulta sys.tables confirmando pago creada](reporte/mssql-visual-10-pago-tablas.png)

**Resultado:** se creó la tabla `pago` mediante el Diseñador de tablas de SSMS, sin escribir SQL manualmente, sin Foreign Key — `referencia_id` es polimórfica, igual que en los demás motores. El script generado coincide con el `CREATE TABLE pago` de la Sección 4.10 (código).

### 5.12 Creación de la tabla `promocion`

![Columnas de promocion configuradas en SSMS](reporte/mssql-visual-11-promocion-columnas.png)

**Script SQL generado por SSMS (Generar script de tabla como → CREATE To):**

![Script CREATE TABLE promocion generado](reporte/mssql-visual-11-promocion-script.png)

**Nota metodológica — trigger `updated_at`:** al igual que en `receta` (Sección 5.5) y `lote_produccion` (Sección 5.7), SSMS no ofrece un diseñador gráfico para triggers, por lo que `trg_promocion_updated_at` se creó por código en una nueva ventana de consulta contra `hornoraiz_visual`, mientras que la estructura de columnas y los valores predeterminados sí se configuraron íntegramente por diseñador.

```sql
CREATE TRIGGER trg_promocion_updated_at
ON promocion
AFTER UPDATE
AS
BEGIN
  UPDATE promocion
  SET updated_at = GETDATE()
  FROM promocion
  INNER JOIN inserted ON promocion.id = inserted.id;
END;
```

![Ejecución del trigger trg_promocion_updated_at sin errores](reporte/mssql-visual-11-promocion-trigger.png)

**Evidencia de la creación:**

![Consulta sys.tables confirmando promocion creada](reporte/mssql-visual-11-promocion-tablas.png)

**Resultado:** se creó la tabla `promocion` mediante el Diseñador de tablas de SSMS, sin ninguna Foreign Key ni tabla puente para la relación `Promocion N:M Producto`, respetando la misma decisión documentada en los demás motores. El trigger `trg_promocion_updated_at` se creó por código, como excepción documentada. El script generado coincide con el `CREATE TABLE promocion` de la Sección 4.11 (código).

### 5.13 Verificación final

![Diagrama de base de datos generado en SSMS — 10 tablas](reporte/mssql-visual-13-diagrama.png)

```sql
SELECT name FROM sys.tables ORDER BY name;
```

![Consulta sys.tables final — 10 tablas](reporte/mssql-visual-13-verificacion-final.png)

**Resultado:** para verificar que el modelo construido manualmente en el Diseñador de tablas de SSMS (Secciones 5.3 a 5.12) coincide con lo realmente creado en el servidor, se generó un diagrama de base de datos directamente desde `hornoraiz_visual`. El resultado confirma las 10 tablas y las 8 relaciones esperadas (todas menos `promocion`, sin conector por decisión ya documentada). `sys.tables` confirma las mismas 10 tablas, idénticas en nombre a las de la Sección 4.12 (código).

#### Conclusión

Con esto se finaliza la creación de la base de datos `hornoraiz` de forma visual en SQL Server Management Studio, replicando las 10 tablas, las 8 relaciones y los tipos de datos definidos en la Sección 4 (código). A diferencia de MySQL Workbench y pgAdmin, SSMS no ofrece un diseñador gráfico para triggers, por lo que los tres triggers de `updated_at` (`receta`, `lote_produccion`, `promocion`) se crearon por código como excepción documentada, mientras que la estructura completa de columnas, Primary Keys, Foreign Keys, índices únicos y valores predeterminados se configuró íntegramente por diseñador, sin escribir código SQL.