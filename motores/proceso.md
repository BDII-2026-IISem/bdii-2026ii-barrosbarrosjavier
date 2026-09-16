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