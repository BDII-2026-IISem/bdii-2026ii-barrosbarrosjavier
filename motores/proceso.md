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