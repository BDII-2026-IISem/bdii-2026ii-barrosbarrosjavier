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