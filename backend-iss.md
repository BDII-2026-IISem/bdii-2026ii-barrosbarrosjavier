# Informe de ISS — HornoRaíz Backend (Django + DRF)

**Estudiante:** Jaime Rafael Gonzalez Ballesta
**Programa:** Ingeniería de Sistemas — Universidad de La Guajira
**Proyecto:** HornoRaíz — Producción y venta de panadería
**Repositorio:** bdii-2026ii-barrosbarrosjavier

---

## ISS-00 — Configuración del entorno y creación del proyecto Django

### Narrativa

El desarrollo del backend comienza con la preparación del entorno de trabajo y la estructura base de Django. Se configuró un entorno virtual independiente para aislar las dependencias del proyecto y evitar conflictos con otras instalaciones de Python. Posteriormente, se creó la estructura inicial de Django, que servirá como base para desarrollar la lógica del backend de HornoRaíz. En esta etapa no se implementan modelos de datos ni endpoints; el propósito es establecer una base organizada y funcional para las siguientes unidades.

### Objetivo

Configurar un entorno virtual e inicializar el proyecto Django `config` para HornoRaíz, dejando preparada la estructura básica del backend, sin implementar todavía modelos ni endpoints.

### Requisitos

- Python 3.12 instalado en el VPS (Ubuntu 24.04).
- Un directorio de proyecto (`Backend/`) dentro del repositorio.
- Conexión a Internet para instalar Django 5.2.17.
- Terminal SSH hacia el VPS.

### Construcción

Se creó y activó un entorno virtual para aislar las dependencias de HornoRaíz. A continuación, se instaló Django en la versión 5.2.17, fijando así una versión específica del framework para mantener la consistencia del entorno de desarrollo. Después, se ejecutó el comando `startproject config .`, utilizando el punto final para ubicar `manage.py` directamente en la raíz del proyecto y conservar los archivos de configuración dentro del directorio `config/`. Finalmente, se registraron las dependencias instaladas en el archivo `requirements.txt`.

```bash
cd /root/bdii/Backend
python3 -m venv .venv
source .venv/bin/activate
which python
python -m pip install "Django==5.2.17"
django-admin startproject config .
python -m pip freeze > requirements.txt
python -m django --version
```

**Creación del `.gitignore`:**

Django no crea un `.gitignore`, así que se añadió a mano. Su función es evitar que el entorno virtual, los secretos del `.env`, las bases de datos locales y los archivos temporales lleguen al repositorio.

```bash
cat > .gitignore <<'EOF'
.venv/
__pycache__/
*.py[cod]
.env
db.sqlite3
*.log
.idea/
.vscode/
staticfiles/
media/
.pytest_cache/
htmlcov/
.coverage
EOF
```

### Explicación

- **Django 5.2.17:** framework principal de esta unidad. Proporciona las herramientas necesarias para iniciar el proyecto, gestionar la configuración y preparar el desarrollo del backend.
- **`.venv`:** entorno virtual que mantiene las dependencias de HornoRaíz separadas de las del sistema. Cuando está activo, el terminal muestra `(.venv)`.
- **`django-admin startproject config .`:** genera la estructura inicial del proyecto, dejando `manage.py` en la raíz y los archivos de configuración dentro de `config/`.
- **`.gitignore`:** archivo que evita incluir en el repositorio elementos locales o sensibles, como `.venv/` y `.env`.
- **`python -m pip`:** permite administrar los paquetes de Python mediante el intérprete del entorno activo, facilitando el control de las dependencias instaladas.

### Criterios de aceptación

- **AC-00-01:** el comando `python -m django --version` muestra la versión `5.2.17`.
- **AC-00-02:** existen los archivos `manage.py` y `config/urls.py`.
- **AC-00-03:** el proyecto todavía no contiene modelos de negocio ni endpoints propios de HornoRaíz.

### Verificación

Para cerrar la unidad se comprobó la versión instalada y se ejecutó el chequeo del proyecto, que confirma que la estructura es válida aunque todavía no tenga lógica de negocio.

```bash
python -m django --version
python manage.py check
```

**Evidencia EVI-00-01** — Entorno virtual activo y `which python` apuntando al `.venv`:

![Entorno virtual activo](evidencias/EVI-00-01-venv-activo.png)

**Evidencia EVI-00-02** — Instalación exitosa de Django 5.2.17:

![Instalación de Django](evidencias/EVI-00-02-instalacion-django.png)

**Evidencia EVI-00-03** — Estructura del proyecto creada (`manage.py` y `config/`):

![Estructura del proyecto](evidencias/EVI-00-03-estructura-proyecto.png)

**Evidencia EVI-00-04** — Versión de Django instalada:

![Versión de Django](evidencias/EVI-00-04-version-django.png)

**Evidencia EVI-00-05** — `manage.py check` sin errores:

![Check exitoso](evidencias/EVI-00-05-check-ok.png)

**Evidencia EVI-00-06** — Árbol del proyecto:

![Árbol del proyecto](evidencias/EVI-00-06-arbol-proyecto.png)

### GATE

| **AC**   | **Verificación**               | **Evidencia** | **Resultado** |
|----------|--------------------------------|---------------|---------------|
| AC-00-01 | versión de Django              | EVI-00-04     | PASS          |
| AC-00-02 | archivos del proyecto          | EVI-00-03     | PASS          |
| AC-00-03 | ausencia de modelos de negocio | EVI-00-06     | PASS          |

---

## ISS-01 — Settings y selección del motor

### Narrativa

Una vez preparada la estructura inicial, el siguiente paso consiste en definir cómo se conectará el backend con la base de datos. Se decidió utilizar un archivo `.env` que permita seleccionar el motor de base de datos mediante variables de entorno, sin modificar la lógica de Python. En esta unidad se establece una configuración flexible y organizada, con la regla de utilizar un solo motor de base de datos por ejecución del proyecto.

### Objetivo

Configurar la selección de un único motor de base de datos para HornoRaíz mediante variables de entorno definidas en `.env`.

### Requisitos

- Haber completado el ISS-00 y tener activo el entorno virtual `(.venv)`.
- Contar con las variables de configuración necesarias para los 4 motores.
- Disponer de un archivo `.env` para almacenar los parámetros de configuración.

### Construcción

**1. Confirmar el entorno**

```bash
source .venv/bin/activate
which python
```

![Entorno virtual activo](evidencias/EVI-01-01-venv-activo.png)

**2. Instalar dependencias del sistema**

`mysqlclient` necesita compilar una extensión en C, por lo que requiere las librerías de desarrollo de MySQL y herramientas de compilación.

```bash
apt update
apt install -y build-essential pkg-config default-libmysqlclient-dev python3.12-dev
```

![Dependencias del sistema](evidencias/EVI-01-02-deps-sistema.png)

**3. Instalar `python-dotenv` y los drivers**

```bash
python -m pip install "python-dotenv==1.2.3"
python -m pip install "psycopg[binary]==3.3.6"
python -m pip install "mysqlclient==2.3.0"
python -m pip install "mssql-django==2.0.0"
python -m pip install "oracledb==26.0.1"
python -m pip freeze > requirements.txt
```

![Instalación de drivers](evidencias/EVI-01-03-instalacion-drivers.png)

![requirements.txt](evidencias/EVI-01-04-requirements.png)

**4. Convertir `settings.py` en paquete**

```bash
rm config/settings.py
mkdir -p config/settings
```

![settings convertido en paquete](evidencias/EVI-01-05-settings-paquete.png)

**5. Crear `.env.example`**

```bash
cat > .env.example <<'EOF'
# Copie este archivo a .env y complete los valores.
# .env no se versiona.

DJANGO_SECRET_KEY=
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,testserver

# Motor activo. Uno solo por ejecución: postgresql | mysql | mssql | oracle
DB_ENGINE=mysql

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432

MYSQL_DB=hornoraiz_django
MYSQL_USER=admin
MYSQL_PASSWORD=1704
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306

MSSQL_DB=
MSSQL_USER=
MSSQL_PASSWORD=
MSSQL_HOST=127.0.0.1
MSSQL_PORT=1433

ORACLE_DB=
ORACLE_USER=
ORACLE_PASSWORD=
ORACLE_HOST=127.0.0.1
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=

# Laboratorio académico. En producción liste orígenes explícitos.
CORS_ALLOW_ALL_ORIGINS=True
EOF
cp .env.example .env
```

![.env.example creado](evidencias/EVI-01-06-env-example.png)

**6. Generar la SECRET_KEY y editar `.env`**

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Se copió el valor generado en `.env`, en la línea `DJANGO_SECRET_KEY=`.

![.env con MySQL configurado](evidencias/EVI-01-07-env-mysql.png)

**7. Crear `config/database.py`**

Se escribió el traductor entre el entorno y Django. Lee `DB_ENGINE` y devuelve un único `DATABASES["default"]`.

![config/database.py](evidencias/EVI-01-08-database-py.png)

**8. Crear `config/settings/__init__.py`**

Carga el `.env`, exige la `SECRET_KEY` y delega la base de datos a `database.py`.

![config/settings/__init__.py](evidencias/EVI-01-09-settings-init.png)

**9. Crear `config/project_python.py`**

Permite ejecutar `python3 manage.py` sin activar el entorno virtual.

![config/project_python.py](evidencias/EVI-01-10-project-python.png)

**10. Parchear `manage.py`, `config/wsgi.py` y `config/asgi.py`**

Se editaron los tres puntos de entrada para que carguen el `.env` antes de que Django lea la configuración.

![manage.py](evidencias/EVI-01-11-manage-py.png)

![config/wsgi.py](evidencias/EVI-01-12-wsgi-py.png)

![config/asgi.py](evidencias/EVI-01-13-asgi-py.png)

### Explicación

- **Intérprete de Python:** `use_project_python()` permite ejecutar `python3 manage.py runserver` sin activar el entorno.
- **Carga de variables de entorno:** `load_dotenv()` carga las variables definidas en `.env`, respetando las existentes.
- **Configuración única de la base de datos:** Django utiliza exclusivamente `DATABASES["default"]`.
- **Conexión a Oracle:** el DSN se construye con `SERVICE_NAME`, con `PORT` vacío.
- **Conexión a SQL Server:** el valor `mssql` se establece en `ENGINE`, según `mssql-django`.
- **Configuración regional:** `LANGUAGE_CODE = "es"`, `TIME_ZONE = "America/Bogota"`, `USE_TZ = True`.

El proceso sigue esta secuencia:

```
.env → DB_ENGINE → database_from_environ → DATABASES["default"] → ORM
```

### Criterios de aceptación

- **AC-01-01:** los motores `postgresql`, `mysql`, `mssql` y `oracle` generan el `ENGINE` correspondiente.
- **AC-01-02:** un motor no reconocido produce `ImproperlyConfigured`.
- **AC-01-03:** la ausencia de una variable obligatoria lanza error antes de conectar.
- **AC-01-04:** el DSN de Oracle incluye `SERVICE_NAME`.

### Verificación

```bash
python -m django --version
python manage.py check
python manage.py shell -c "from django.db import connection; connection.ensure_connection(); print('Motor:', connection.vendor); print('Base de datos:', connection.settings_dict['NAME']); print('Conexión: OK')"
```

![Check exitoso](evidencias/EVI-01-14-check-ok.png)

![Conexión a MySQL](evidencias/EVI-01-15-conexion-mysql.png)

Los tests de `DatabaseSelectionTests` se escriben en el ISS-03.

### GATE

| **AC**   | **Verificación**               | **Evidencia** | **Resultado** |
|----------|--------------------------------|---------------|---------------|
| AC-01-01 | Los 4 motores generan el ENGINE correcto | EVI-01-15 | PASS |
| AC-01-02 | Motor inválido lanza `ImproperlyConfigured` | EVI-01-15 | PASS |
| AC-01-03 | Variable vacía lanza error | EVI-01-15 | PASS |
| AC-01-04 | DSN de Oracle contiene `SERVICE_NAME` | EVI-01-15 | PASS |