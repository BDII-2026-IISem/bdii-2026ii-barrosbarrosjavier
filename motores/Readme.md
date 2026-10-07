# BDII 2026-II — Javier Barros

Repositorio de los talleres de Bases de Datos II — Universidad de La Guajira: instalación y configuración de motores de bases de datos, y consultas avanzadas, procedimientos almacenados y triggers de auditoría sobre el mismo modelo en los cuatro motores.

## Proyecto asignado

**05. HornoRaíz - Producción y venta de panadería**

Sistema de producción y venta de panadería que versiona recetas, planea lotes de producción, reserva y consume insumos, registra mermas y convierte producción terminada en existencias vendibles.

## Contenido del repositorio

- 📄 [`Instalacion-Configuracion-Motores-BD.md`](./Instalacion-Configuracion-Motores-BD.md) — Informe de trazabilidad completo: instalación, configuración y verificación de los cuatro motores de base de datos (MySQL, PostgreSQL, MS SQL Server y Oracle XE) sobre una máquina virtual de VirtualBox con Ubuntu y Docker, incluyendo la base de datos `hornoraiz` con sus 11 tablas, usuarios con acceso remoto, conexiones verificadas desde DBeaver y backups de cada motor.
- 📄 [`proceso.md`](./proceso.md) — Registro del proceso de trabajo paso a paso, con los comandos ejecutados y los problemas encontrados en cada etapa.
- 📄 [`consultas-avanzadas.md`](./consultas-avanzadas.md) — Informe de consultas avanzadas, procedimientos almacenados y triggers de auditoría sobre `hornoraiz`, ejecutados en los cuatro motores, con la evidencia y el resultado de cada ejercicio.
- 🖼️ [`assets/`](./assets) — Capturas de evidencia del informe de instalación.
- 🖼️ [`reporte/`](./reporte) — Capturas de evidencia de `proceso.md`.
- 🖼️ [`consultas/`](./consultas) — Capturas de evidencia del informe de consultas, procedimientos y triggers.

## Informe de consultas avanzadas

Sobre las 10 tablas del modelo, renombradas a plural e inglés (`products`, `supplies`, `recipes`, `recipe_supplies`, `production_batches`, `supply_movements`, `sales`, `sale_details`, `payments`, `promotions`), con 100 registros de prueba por tabla cargados desde los mismos archivos CSV en los cuatro motores.

Cada motor sigue la misma estructura:

| Motor | Consultas avanzadas | Procedimientos almacenados | Triggers de auditoría |
|---|---|---|---|
| MySQL 8.0 | 1.13 | 1.14 | 1.15 |
| PostgreSQL 17 | 2.14 | 2.15 | 2.16 |
| SQL Server 2022 | 3.15 | 3.16 | 3.17 |
| Oracle XE 21c | 4.15 | 4.16 | 4.17 |

- **Consultas avanzadas (9):** proyección de columnas, ordenamiento, relación de tablas con `WHERE` y con `JOIN`, filtros por estado, `LIKE`, `BETWEEN` sobre cuatro tablas, `GROUP BY` con `HAVING` y subconsultas con teoría de conjuntos (`NOT IN` y `LEFT JOIN ... IS NULL`). Los resultados coinciden en los cuatro motores.
- **Procedimientos almacenados (15 por motor):** cada consulta se llevó a un procedimiento. Cada motor lo resuelve a su manera: `CALL` en MySQL, cursor `refcursor` en PostgreSQL, `EXEC` en SQL Server y `DBMS_SQL.RETURN_RESULT` en Oracle.
- **Triggers de auditoría:** sobre `products` y `sales`, con el estado anterior y posterior de cada fila en JSON, y protección de las tablas de auditoría contra `UPDATE`, `DELETE` e `INSERT` directo.

Los incidentes encontrados quedaron documentados en el informe, entre ellos la conversión incorrecta de `boolean` al importar en PostgreSQL, la columna de identidad `GENERATED ALWAYS` y la palabra reservada `DATE` en Oracle, el privilegio `SUPER` para crear triggers en MySQL y los errores de DBeaver al crear triggers con bloques `BEGIN ... END` en MySQL y SQL Server.

## Entorno de trabajo

- **Instalación y configuración:** VirtualBox con Ubuntu 26.04 LTS
- **Consultas avanzadas:** VPS en Contabo con Ubuntu 24.04 LTS y 8 GB de RAM. Los contenedores se migraron desde la máquina virtual copiando sus carpetas de datos, porque es mas facil de poder usar en otros lugares.
- **Contenedores:** Docker + Docker Compose
- **Motores:** MySQL 8.0, PostgreSQL 17, SQL Server 2022, Oracle XE 21c
- **Cliente de administración:** DBeaver, con conexión remota a la VPS. Los puertos de las bases de datos están restringidos por IP en el firewall.

## Autor

**Javier Barros**
Estudiante de Ingeniería de Sistemas — Universidad de La Guajira
Tutor: Ing. Jaider Quintero M.