# BDII 2026-II — Javier Barros

<p align="center">
  <img src="https://img.shields.io/badge/Proyecto-HornoRa%C3%ADz-8B5A2B?style=for-the-badge" alt="HornoRaíz" />
  <img src="https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL" />
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/SQL_Server-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white" alt="SQL Server" />
  <img src="https://img.shields.io/badge/Oracle-F80000?style=for-the-badge&logo=oracle&logoColor=white" alt="Oracle" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white" alt="Ubuntu" />
  <img src="https://img.shields.io/badge/VirtualBox-21416B?style=for-the-badge&logo=virtualbox&logoColor=white" alt="VirtualBox" />
  <img src="https://img.shields.io/badge/DBeaver-382923?style=for-the-badge&logo=dbeaver&logoColor=white" alt="DBeaver" />
  <img src="https://img.shields.io/badge/Universidad_de_La_Guajira-Ingenier%C3%ADa_de_Sistemas-1F6FEB?style=for-the-badge" alt="Uniguajira" />
</p>

Repositorio de los talleres de **Bases de Datos II** — Universidad de La Guajira. Reúne la instalación y configuración de cuatro motores de bases de datos con Docker, y las consultas avanzadas, los procedimientos almacenados y los triggers de auditoría ejecutados sobre el mismo modelo en cada uno.

## Índice

- [Proyecto asignado](#proyecto-asignado)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Documentos](#documentos)
- [Estado del trabajo](#estado-del-trabajo)
- [Motores y versiones](#motores-y-versiones)
- [Autor](#autor)

## Proyecto asignado

**05. HornoRaíz - Producción y venta de panadería**

Sistema de producción y venta de panadería que versiona recetas, planea lotes de producción, reserva y consume insumos, registra mermas y convierte producción terminada en existencias vendibles. La base de datos se llama `hornoraiz` y se construyó con el mismo modelo en MySQL, PostgreSQL, SQL Server y Oracle.

## Estructura del repositorio

```text
bdii-2026ii-barrosbarrosjavier/
├── README.md
├── .gitignore
└── motores/
    ├── README.md
    ├── Instalacion-Configuracion-Motores-BD.md
    ├── proceso.md
    ├── consultas-avanzadas.md
    ├── assets/
    ├── reporte/
    └── consultas/
```

## Documentos

| Documento | Contenido |
|---|---|
| [`motores/README.md`](./motores/README.md) | Índice de la carpeta de trabajo, con el entorno y la estructura de cada informe. |
| [`motores/Instalacion-Configuracion-Motores-BD.md`](./motores/Instalacion-Configuracion-Motores-BD.md) | Informe de trazabilidad: instalación, configuración y verificación de los cuatro motores, con usuarios de acceso remoto, conexiones desde DBeaver y backups. |
| [`motores/proceso.md`](./motores/proceso.md) | Registro del proceso de trabajo paso a paso, con los comandos ejecutados y los problemas encontrados. |
| [`motores/consultas-avanzadas.md`](./motores/consultas-avanzadas.md) | Consultas avanzadas, procedimientos almacenados y triggers de auditoría en los cuatro motores, con la evidencia y el resultado de cada ejercicio. |

## Estado del trabajo

| Motor | Instalación | Consultas avanzadas | Procedimientos | Triggers de auditoría |
|---|:---:|:---:|:---:|:---:|
| MySQL | ✅ | ✅ | ✅ | ✅ |
| PostgreSQL | ✅ | ✅ | ✅ | ✅ |
| SQL Server | ✅ | ✅ | ✅ | ✅ |
| Oracle | ✅ | ✅ | ✅ | ✅ |

En el informe de consultas hay 9 consultas, 15 procedimientos y 2 tablas de auditoría por motor (`products_audit` y `sales_audit`). Los resultados coinciden en los cuatro motores, y las diferencias de sintaxis y de comportamiento quedaron documentadas en cada sección.

## Motores y versiones

| Motor | Versión | Imagen Docker |
|---|---|---|
| MySQL | 8.0 | `mysql:8.0` |
| PostgreSQL | 17 | `postgres:17` |
| SQL Server | 2022 | `mcr.microsoft.com/mssql/server:2022-latest` |
| Oracle | XE 21c | `gvenzl/oracle-xe:21-slim` |

La instalación se hizo sobre una máquina virtual de VirtualBox con Ubuntu. Las consultas avanzadas se ejecutaron sobre una VPS con Ubuntu y Docker, porque el equipo local no soportaba correr Oracle junto con los otros motores. El cliente de administración es DBeaver.

## Autor

**Javier Barros**
Estudiante de Ingeniería de Sistemas — Facultad de Ingeniería, Universidad de La Guajira
Tutor: Ing. Jaider Quintero M.