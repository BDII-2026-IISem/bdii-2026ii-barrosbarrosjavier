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

---

## ISS-02 — Apps catalog, production y sale

### Narrativa

Con la configuración del entorno y de la base de datos preparada, HornoRaíz necesita una estructura que permita organizar las funcionalidades del sistema. Django utiliza aplicaciones (*apps*) para separar la lógica del proyecto en módulos independientes, cada uno enfocado en una parte específica del negocio. En esta unidad se crearon las aplicaciones correspondientes a la gestión de la panadería y se organizaron dentro del paquete `apps/`, evitando que el directorio raíz se llene de carpetas dispersas. En esta etapa no se implementan modelos ni reglas de negocio; el trabajo se centra en establecer la estructura modular y registrar las aplicaciones en la configuración del proyecto.

### Objetivo

Crear las aplicaciones de negocio de HornoRaíz mediante las herramientas de Django, organizarlas dentro del paquete `apps/` y registrarlas en la configuración para facilitar su desarrollo en las siguientes unidades.

### Requisitos

- Haber completado el ISS-01, correspondiente a la configuración del entorno y la selección del motor de base de datos.
- Tener activo el entorno virtual `(.venv)` en la terminal.
- Contar con el proyecto Django `config` creado y funcionando.
- No implementar todavía los modelos de negocio.

### Construcción

**1. Confirmar el entorno**

```bash
source .venv/bin/activate
which python
```

![Entorno virtual activo](evidencias/EVI-02-01-venv-activo.png)

**2. Crear los directorios y las apps con `startapp`**

`startapp` exige que el directorio destino ya exista. Por eso primero se crean las carpetas y luego se genera cada app.

```bash
mkdir -p apps/catalog apps/production apps/sale

python manage.py startapp catalog apps/catalog
python manage.py startapp production apps/production
python manage.py startapp sale apps/sale
```

![Apps creadas con startapp](evidencias/EVI-02-02-startapp.png)

**3. Verificar la estructura de las apps**

```bash
tree apps -I "__pycache__"
```

![Estructura de las apps](evidencias/EVI-02-03-estructura-apps.png)

**4. Convertir `apps` en paquete**

Se creó `apps/__init__.py`, vacío, para que Python trate la carpeta `apps` como un paquete.

```bash
cat > apps/__init__.py <<'EOF'
EOF
```

![apps/__init__.py creado](evidencias/EVI-02-04-apps-init.png)

**5. Parchear el `apps.py` de cada app**

Como las apps viven dentro de `apps/`, hay que indicarle a Django la ruta completa del paquete. Se mantiene el `label` corto para que las migraciones no arrastren el prefijo `apps.`.

```python
# apps/catalog/apps.py
from django.apps import AppConfig


class CatalogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.catalog"
    label = "catalog"
```

```python
# apps/production/apps.py
from django.apps import AppConfig


class ProductionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.production"
    label = "production"
```

```python
# apps/sale/apps.py
from django.apps import AppConfig


class SaleConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.sale"
    label = "sale"
```

![apps.py parcheados](evidencias/EVI-02-05-apps-py.png)

**6. Registrar las apps en `config/settings/__init__.py`**

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.catalog.apps.CatalogConfig",
    "apps.production.apps.ProductionConfig",
    "apps.sale.apps.SaleConfig",
]
```

![Apps registradas en INSTALLED_APPS](evidencias/EVI-02-06-installed-apps.png)

### Explicación

Django necesita conocer la ruta completa de cada aplicación para poder reconocerla y cargarla correctamente. En HornoRaíz, las aplicaciones se encuentran dentro del directorio `apps/`, por lo que el atributo `AppConfig.name` debe especificar la ruta correspondiente, como `apps.catalog`.

El atributo `label` conserva el nombre corto de cada aplicación, por ejemplo `catalog`, facilitando su identificación dentro del proyecto y evitando introducir el prefijo del paquete en las referencias de las migraciones.

Cada aplicación representa un área funcional de HornoRaíz:

```
apps/
├── catalog/     products, supplies, recipes, recipe_supplies, promotions
├── production/  production_batches, supply_movements
└── sale/        sales, sale_details, payments
```

En esta etapa se prepara la estructura de las aplicaciones, sin implementar todavía los modelos de negocio.

### Criterios de aceptación

- **AC-02-01:** verificar que las aplicaciones `catalog`, `production` y `sale` se hayan creado mediante el comando `startapp` de Django.
- **AC-02-02:** comprobar que `python manage.py check` se ejecute sin errores relacionados con el registro o la configuración de las aplicaciones.
- **AC-02-03:** confirmar que todavía no se hayan implementado modelos de negocio en esta etapa del desarrollo.

### Verificación

```bash
python manage.py check
```

![Check exitoso](evidencias/EVI-02-07-check-ok.png)

### GATE

| **AC**   | **Verificación**               | **Evidencia** | **Resultado** |
|----------|--------------------------------|---------------|---------------|
| AC-02-01 | directorios de las apps        | EVI-02-03     | PASS          |
| AC-02-02 | `manage.py check`              | EVI-02-07     | PASS          |
| AC-02-03 | este ISS no escribe modelos    | revisión de los `models.py` vacíos | PASS |

---

## ISS-03 — Custom User antes de la primera migración

### Narrativa

Con la estructura de apps lista, el siguiente paso consiste en definir el modelo de usuario propio del sistema antes de la primera migración. Django trae un usuario por defecto, pero cambiarlo después de migrar obliga a borrar tablas. Por eso, en esta unidad se creó el usuario personalizado de HornoRaíz sobre `django.contrib.auth`, se declaró en la configuración y solo entonces se hizo la primera migración. Así, las credenciales del sistema quedan en una tabla propia (`users`).

### Objetivo

Definir el usuario de HornoRaíz sobre `django.contrib.auth` y fijar `AUTH_USER_MODEL` antes de migrar.

### Requisitos

- ISS-02 superado.
- Terminal con el entorno virtual `.venv` activo.
- Decisión explícita entre `AbstractUser` y `AbstractBaseUser`: se eligió `AbstractUser`.

### Construcción

**1. Confirmar el entorno**

```bash
cd /root/bdii/Backend
source .venv/bin/activate
which python
```

![Entorno virtual activo](evidencias/EVI-03-01-venv-activo.png)

**2. Crear el paquete `apps/common` con `RecordStatus`**

El estado "activo / inactivo" lo usarán el usuario y, desde el ISS-04, las tablas del negocio. `apps/common` no es una app: no se registra en `INSTALLED_APPS` ni se crea con `startapp`.

```bash
mkdir -p apps/common
cat > apps/common/__init__.py <<'EOF'
EOF
cat > apps/common/status.py <<'EOF'
from django.db import models


class RecordStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
EOF
```

![apps/common creado](evidencias/EVI-03-02-apps-common.png)

**3. Crear la app `security` con la CLI**

```bash
mkdir -p apps/security
python manage.py startapp security apps/security
```

![App security creada](evidencias/EVI-03-03-startapp-security.png)

**4. Parchear `apps/security/apps.py`**

```python
from django.apps import AppConfig


class SecurityConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.security"
    label = "security"
```

![apps.py parcheado](evidencias/EVI-03-04-apps-py.png)

**5. Escribir el modelo de usuario**

```python
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from apps.common.status import RecordStatus


class HornoRaizUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("status", RecordStatus.INACTIVE)
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("status", RecordStatus.ACTIVE)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField("correo electrónico", max_length=150, unique=True)
    status = models.CharField(
        max_length=8,
        choices=RecordStatus.choices,
        default=RecordStatus.INACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = HornoRaizUserManager()

    class Meta:
        db_table = "users"
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(status__in=RecordStatus.values),
                name="users_status_valid",
            )
        ]

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.strip().lower()
        self.is_active = self.status == RecordStatus.ACTIVE
        super().save(*args, **kwargs)
```

`create_user` deja `status` en `inactive` si nadie lo indica. `create_superuser` lo fuerza a `active`, para que `save()` no desactive al superusuario.

![models.py del usuario](evidencias/EVI-03-05-models-py.png)

**6. Registrar la app y fijar `AUTH_USER_MODEL`**

En `config/settings/__init__.py`, la app de seguridad va delante de las de negocio:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.security.apps.SecurityConfig",
    "apps.catalog.apps.CatalogConfig",
    "apps.production.apps.ProductionConfig",
    "apps.sale.apps.SaleConfig",
]
```

Y debajo de `DATABASES = database_from_environ(os.environ)`:

```python
AUTH_USER_MODEL = "security.User"
```

![AUTH_USER_MODEL configurado](evidencias/EVI-03-06-auth-user-model.png)

**7. Escribir el test de selección del motor**

```python
from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase

from config.database import database_from_environ


class DatabaseSelectionTests(SimpleTestCase):
    def _env(self, engine):
        return {
            "DB_ENGINE": engine,
            "POSTGRES_DB": "hornoraiz",
            "POSTGRES_USER": "hornoraiz",
            "POSTGRES_PASSWORD": "hornoraiz",
            "POSTGRES_HOST": "127.0.0.1",
            "POSTGRES_PORT": "5432",
            "MYSQL_DB": "hornoraiz_django",
            "MYSQL_USER": "admin",
            "MYSQL_PASSWORD": "1704",
            "MYSQL_HOST": "127.0.0.1",
            "MYSQL_PORT": "3306",
            "MSSQL_DB": "hornoraiz",
            "MSSQL_USER": "sa",
            "MSSQL_PASSWORD": "hornoraiz",
            "MSSQL_HOST": "127.0.0.1",
            "MSSQL_PORT": "1433",
            "ORACLE_DB": "hornoraiz",
            "ORACLE_USER": "admin",
            "ORACLE_PASSWORD": "hornoraiz",
            "ORACLE_HOST": "127.0.0.1",
            "ORACLE_PORT": "1521",
            "ORACLE_SERVICE_NAME": "FREEPDB1",
        }

    def test_postgresql_engine(self):
        config = database_from_environ(self._env("postgresql"))
        self.assertEqual(config["default"]["ENGINE"], "django.db.backends.postgresql")

    def test_mysql_engine(self):
        config = database_from_environ(self._env("mysql"))
        self.assertEqual(config["default"]["ENGINE"], "django.db.backends.mysql")
        self.assertEqual(config["default"]["OPTIONS"]["charset"], "utf8mb4")

    def test_mssql_engine(self):
        config = database_from_environ(self._env("mssql"))
        self.assertEqual(config["default"]["ENGINE"], "mssql")

    def test_oracle_uses_service_name(self):
        config = database_from_environ(self._env("oracle"))
        self.assertIn("SERVICE_NAME=FREEPDB1", config["default"]["NAME"])
        self.assertEqual(config["default"]["PORT"], "")

    def test_invalid_engine(self):
        with self.assertRaises(ImproperlyConfigured):
            database_from_environ({"DB_ENGINE": "sqlite"})

    def test_missing_variable(self):
        env = self._env("postgresql")
        env["POSTGRES_DB"] = ""
        with self.assertRaises(ImproperlyConfigured):
            database_from_environ(env)
```

![Tests de selección de motor](evidencias/EVI-03-07-tests-py.png)

**8. Generar la migración**

```bash
python manage.py makemigrations security
```

Resultado:
```
Migrations for 'security':
  apps/security/migrations/0001_initial.py
    + Create model User
```

![makemigrations](evidencias/EVI-03-08-makemigrations.png)

**9. Migrar**

```bash
python manage.py migrate
```

Resultado:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, security, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying security.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying sessions.0001_initial... OK
```

![migrate](evidencias/EVI-03-09-migrate.png)

**10. Ejecutar los tests**

```bash
python manage.py test apps.security.tests.DatabaseSelectionTests
```

Resultado:
```
Found 6 test(s).
System check identified no issues (0 silenced).
......
Ran 6 tests in 0.001s

OK
```

![Tests PASS](evidencias/EVI-03-10-tests-pass.png)

**11. Probar la conexión a MySQL**

```bash
python manage.py shell -c "from django.db import connection; connection.ensure_connection(); print('Motor:', connection.vendor); print('Base de datos:', connection.settings_dict['NAME']); print('Conexión: OK')"
```

Resultado:
```
Motor: mysql
Base de datos: hornoraiz_django
Conexión: OK
```

![Conexión a MySQL](evidencias/EVI-03-11-conexion-mysql.png)

**12. Crear el superusuario**

```bash
python manage.py createsuperuser
```

![Superusuario creado](evidencias/EVI-03-12-createsuperuser.png)

**13. Verificar la tabla `users` en MySQL**

```bash
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; SHOW TABLES;"
```

Resultado:
```
Tables_in_hornoraiz_django
auth_group
auth_group_permissions
auth_permission
django_admin_log
django_content_type
django_migrations
django_session
users            ← la tabla del usuario personalizado
users_groups
users_user_permissions
```

![Tablas creadas](evidencias/EVI-03-13-tabla-users.png)

**14. Verificar el superusuario en la tabla**

```bash
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; SELECT id, username, email, status, is_active, is_staff, is_superuser FROM users;"
```

Resultado:
```
id  username  email                       status  is_active  is_staff  is_superuser
1   admin     barrosbarrosjavier@gmail.com  active  1          1         1
```

![Superusuario verificado](evidencias/EVI-03-14-superusuario-verificado.png)

### Explicación

Se prefirió `AbstractUser` sobre `AbstractBaseUser` porque proporciona funcionalidades de autenticación ya implementadas por Django, como el hash de contraseñas, los validadores, los métodos `set_password()` y `check_password()`, y la integración con el panel administrativo.

El campo `status` permite representar el estado funcional de la cuenta, mientras que `is_active` se conserva para mantener la compatibilidad con los mecanismos de autenticación de Django. Para garantizar el comportamiento esperado, ambos campos se mantienen sincronizados desde el método `save()`.

```
AbstractUser
    + status
    + created_at / updated_at
    + email único
         │
         ▼
AUTH_USER_MODEL = security.User
```

### Criterios de aceptación

- **AC-03-01:** `AUTH_USER_MODEL` apunta a `security.User`.
- **AC-03-02:** la tabla `users` se crea en `hornoraiz_django` (no `auth_user`).
- **AC-03-03:** el `HornoRaizUserManager` marca los usuarios nuevos como `inactive` y el superusuario como `active`.
- **AC-03-04:** el superusuario creado tiene `status = active` e `is_active = 1`.

### Verificación

```bash
python manage.py test apps.security.tests.DatabaseSelectionTests
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; SELECT id, username, email, status, is_active, is_staff, is_superuser FROM users;"
```

![Tests PASS](evidencias/EVI-03-10-tests-pass.png)

![Superusuario verificado](evidencias/EVI-03-14-superusuario-verificado.png)

### GATE

| **AC**   | **Verificación**               | **Evidencia** | **Resultado** |
|----------|--------------------------------|---------------|---------------|
| AC-03-01 | `AUTH_USER_MODEL` configurado  | EVI-03-06     | PASS          |
| AC-03-02 | tabla `users` creada en MySQL  | EVI-03-13     | PASS          |
| AC-03-03 | manager maneja el estado       | EVI-03-05     | PASS          |
| AC-03-04 | superusuario activo creado     | EVI-03-14     | PASS          |

---

## ISS-04 — Modelos Product, Supply, Recipe y RecipeSupply

### Narrativa

Con el modelo de usuario del sistema ya definido y migrado, se desarrollan los primeros modelos de negocio de HornoRaíz. Antes de implementarlos, se creó una clase base común para los modelos del negocio, que centraliza la auditoría temporal cuando la tabla la necesita. En este ISS se modelan las entidades del catálogo: los productos de panadería (`Product`), los insumos (`Supply`), las recetas (`Recipe`) y la relación entre recetas e insumos (`RecipeSupply`). Los modelos respetan la estructura exacta de las tablas `products`, `supplies`, `recipes` y `recipe_supplies` del esquema original.

### Objetivo

Persistir y administrar la información del catálogo de HornoRaíz mediante los modelos `Product`, `Supply`, `Recipe` y `RecipeSupply`, respetando el diccionario de datos y la estructura definida para sus tablas.

### Requisitos

- ISS-03 superado: modelo de usuario del sistema definido y migrado.
- Terminal con el entorno virtual `.venv` activo.
- Clase base común para los modelos del negocio.
- Aplicación `catalog` registrada correctamente en la configuración de Django.
- Conexión a la base de datos MySQL `hornoraiz_django` configurada.

### Construcción

**1. Confirmar el entorno**

```bash
cd /root/bdii/Backend
source .venv/bin/activate
which python
```

![Entorno virtual activo](evidencias/EVI-04-01-venv-activo.png)

**2. Crear el modelo abstracto base**

Se definió `TimeStampedModel` en `apps/common/models.py`, que aporta `created_at` y `updated_at` a los modelos que lo necesiten.

```python
from django.db import models


class TimeStampedModel(models.Model):
    """Añade created_at y updated_at a cualquier modelo."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

![apps/common/models.py](evidencias/EVI-04-02-common-models.png)

**3. Escribir los modelos del catálogo**

Se reescribió `apps/catalog/models.py` entero con los cuatro modelos del catálogo.

```python
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from apps.common.models import TimeStampedModel


class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    description = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "products"
        verbose_name = "producto"
        verbose_name_plural = "productos"
        ordering = ["name", "id"]

    def __str__(self):
        return f"{self.sku} - {self.name}"


class Supply(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    unit_of_measure = models.CharField(max_length=30)
    min_stock = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "supplies"
        verbose_name = "insumo"
        verbose_name_plural = "insumos"
        ordering = ["name", "id"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Recipe(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="recipes",
        db_column="product_id",
    )
    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    description = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "recipes"
        verbose_name = "receta"
        verbose_name_plural = "recetas"
        ordering = ["name", "id"]

    def __str__(self):
        return self.name


class RecipeSupply(models.Model):
    main = models.ForeignKey(
        Recipe,
        on_delete=models.PROTECT,
        related_name="recipe_supplies",
        db_column="main_id",
    )
    related = models.ForeignKey(
        Supply,
        on_delete=models.PROTECT,
        related_name="recipe_supplies",
        db_column="related_id",
    )
    relation_data = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "recipe_supplies"
        verbose_name = "insumo de receta"
        verbose_name_plural = "insumos de receta"
        ordering = ["main_id", "related_id", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["main", "related"],
                name="recipe_supplies_unique",
            ),
        ]

    def __str__(self):
        return f"{self.main} - {self.related}"
```

![apps/catalog/models.py](evidencias/EVI-04-03-catalog-models.png)

**4. Generar la migración**

```bash
python manage.py makemigrations catalog
```

Resultado:
```
Migrations for 'catalog':
  apps/catalog/migrations/0001_initial.py
    + Create model Product
    + Create model Supply
    + Create model Recipe
    + Create model RecipeSupply
```

![makemigrations](evidencias/EVI-04-04-makemigrations.png)

**5. Migrar**

```bash
python manage.py migrate
```

Resultado:
```
Operations to perform:
  Apply all migrations: admin, auth, catalog, contenttypes, security, sessions
Running migrations:
  Applying catalog.0001_initial... OK
```

![migrate](evidencias/EVI-04-05-migrate.png)

**6. Verificar las tablas en MySQL**

```bash
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; SHOW TABLES;"
```

![Tablas creadas](evidencias/EVI-04-06-tablas-creadas.png)

```bash
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; DESCRIBE products;"
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; DESCRIBE supplies;"
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; DESCRIBE recipes;"
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; DESCRIBE recipe_supplies;"
```

![Estructura de tablas](evidencias/EVI-04-07-describe-tablas.png)

**7. Probar en el shell**

```python
from apps.catalog.models import Product, Supply, Recipe, RecipeSupply
from decimal import Decimal
from django.db import IntegrityError

p = Product.objects.create(sku="TEST-001", name="Pan de prueba", price=Decimal("1000.00"))
print("Product:", p.id, p.status)

s = Supply.objects.create(code="INS-001", name="Harina", unit_of_measure="kg", min_stock=Decimal("5.00"))
print("Supply:", s.id, s.status)

r = Recipe.objects.create(product=p, name="Receta de pan de prueba")
print("Recipe:", r.id, r.status, r.created_at is not None)

rs = RecipeSupply.objects.create(main=r, related=s, relation_data="500 gramos")
print("RecipeSupply:", rs.id, rs.status)

try:
    Product.objects.create(sku="TEST-001", name="Otro pan", price=Decimal("500.00"))
except IntegrityError:
    print("OK: rechazó el sku duplicado")

from django.core.exceptions import ValidationError
try:
    p2 = Product(sku="TEST-002", name="A", price=Decimal("100.00"))
    p2.full_clean()
except ValidationError:
    print("OK: rechazó nombre de 1 carácter")
```

Resultado:
```
Product: 1 True
Supply: 1 True
Recipe: 1 True True
RecipeSupply: 1 True
OK: rechazó el sku duplicado
OK: rechazó nombre de 1 carácter
```

![Pruebas en shell](evidencias/EVI-04-08-shell-test.png)

**8. Verificar los datos en MySQL**

```bash
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; SELECT id, sku, name, price, status FROM products;"
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; SELECT id, code, name, unit_of_measure, min_stock, status FROM supplies;"
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; SELECT id, product_id, name, status FROM recipes;"
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; SELECT id, main_id, related_id, relation_data, status FROM recipe_supplies;"
```

![Datos insertados](evidencias/EVI-04-09-datos-mysql.png)

### Explicación

- **`Product`** almacena los productos de panadería con `sku` único, `name`, `description`, `price` y `status`.
- **`Supply`** almacena los insumos con `code` único, `name`, `unit_of_measure`, `min_stock` y `status`.
- **`Recipe`** relaciona un producto con sus recetas, con `product_id` como FK protegida y timestamps `created_at` y `updated_at`.
- **`RecipeSupply`** resuelve la relación N:M entre recetas e insumos, con `main_id` (receta) y `related_id` (insumo), y una restricción de unicidad en el par.
- El `status` es un `BooleanField(default=True)` que refleja el `tinyint(1)` del esquema original.
- `on_delete=models.PROTECT` impide eliminar un producto o insumo que tenga recetas o relaciones asociadas.

```
catalog/
├── Product      → products
├── Supply       → supplies
├── Recipe       → recipes
└── RecipeSupply → recipe_supplies
```

### Criterios de aceptación

- **AC-04-01:** las tablas físicas son `products`, `supplies`, `recipes`, `recipe_supplies`.
- **AC-04-02:** sin `status` en el alta, el valor por defecto es `True`.
- **AC-04-03:** `created_at` y `updated_at` se generan en `Recipe`.
- **AC-04-04:** el `sku` duplicado se rechaza con `IntegrityError`.
- **AC-04-05:** un nombre de un carácter se rechaza con `ValidationError`.

### Verificación

```bash
python manage.py migrate
python manage.py shell
```

![Pruebas en shell](evidencias/EVI-04-08-shell-test.png)

![Datos insertados](evidencias/EVI-04-09-datos-mysql.png)

### GATE

| **AC**   | **Verificación**                | **Evidencia** | **Resultado** |
|----------|---------------------------------|---------------|---------------|
| AC-04-01 | `db_table` en Meta              | EVI-04-07     | PASS          |
| AC-04-02 | status default True             | EVI-04-08     | PASS          |
| AC-04-03 | timestamps en Recipe            | EVI-04-08     | PASS          |
| AC-04-04 | sku duplicado rechazado         | EVI-04-08     | PASS          |
| AC-04-05 | nombre corto rechazado          | EVI-04-08     | PASS          |

---

## ISS-05 — Modelos ProductionBatch, SupplyMovement y Promotion

### Narrativa

Con el catálogo modelado en el ISS-04, el siguiente paso consiste en representar las operaciones de producción y las promociones del negocio. Se modelan los lotes de producción (`ProductionBatch`), los movimientos de insumos (`SupplyMovement`) y las promociones (`Promotion`). Los lotes se vinculan a una receta mediante `PROTECT`, los movimientos de insumos pueden o no estar asociados a un lote (nullable) y las promociones no tienen FK, respetando la decisión de diseño del proyecto original.

### Objetivo

Persistir y administrar los lotes de producción, los movimientos de insumos y las promociones de HornoRaíz, respetando el esquema original de las tablas `production_batches`, `supply_movements` y `promotions`.

### Requisitos

- ISS-04 superado: catálogo modelado y migrado.
- Terminal con el entorno virtual `.venv` activo.
- Aplicaciones `catalog` y `production` registradas en la configuración.

### Construcción

**1. Confirmar el entorno**

```bash
cd /root/bdii/Backend
source .venv/bin/activate
which python
```

![Entorno virtual activo](evidencias/EVI-05-01-venv-activo.png)

**2. Escribir los modelos de producción**

```python
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from apps.catalog.models import Recipe, Supply
from apps.common.models import TimeStampedModel


class ProductionBatch(TimeStampedModel):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.PROTECT,
        related_name="production_batches",
        db_column="recipe_id",
    )
    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    description = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "production_batches"
        verbose_name = "lote de producción"
        verbose_name_plural = "lotes de producción"
        ordering = ["name", "id"]

    def __str__(self):
        return self.name


class SupplyMovement(models.Model):
    production_batch = models.ForeignKey(
        ProductionBatch,
        on_delete=models.PROTECT,
        related_name="supply_movements",
        db_column="production_batch_id",
        null=True,
        blank=True,
    )
    supply = models.ForeignKey(
        Supply,
        on_delete=models.PROTECT,
        related_name="supply_movements",
        db_column="supply_id",
    )
    type = models.CharField(max_length=50)
    date = models.DateTimeField()
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    notes = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=30)

    class Meta:
        db_table = "supply_movements"
        verbose_name = "movimiento de insumo"
        verbose_name_plural = "movimientos de insumos"
        ordering = ["-date", "id"]

    def __str__(self):
        return f"{self.type} - {self.supply} ({self.quantity})"
```

![apps/production/models.py](evidencias/EVI-05-02-production-models.png)

**3. Agregar `Promotion` al catálogo**

```python
class Promotion(TimeStampedModel):
    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    description = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "promotions"
        verbose_name = "promoción"
        verbose_name_plural = "promociones"
        ordering = ["name", "id"]

    def __str__(self):
        return self.name
```

![apps/catalog/models.py con Promotion](evidencias/EVI-05-03-catalog-models.png)

**4. Generar las migraciones**

```bash
python manage.py makemigrations catalog production
```

Resultado:
```
Migrations for 'catalog':
  apps/catalog/migrations/0002_promotion.py
    + Create model Promotion
Migrations for 'production':
  apps/production/migrations/0001_initial.py
    + Create model ProductionBatch
    + Create model SupplyMovement
```

![makemigrations](evidencias/EVI-05-04-makemigrations.png)

**5. Migrar**

```bash
python manage.py migrate
```

Resultado:
```
Applying catalog.0002_promotion... OK
Applying production.0001_initial... OK
```

![migrate](evidencias/EVI-05-05-migrate.png)

**6. Verificar las tablas en MySQL**

```bash
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; SHOW TABLES;"
```

![Tablas creadas](evidencias/EVI-05-06-tablas-creadas.png)

```bash
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; DESCRIBE production_batches;"
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; DESCRIBE supply_movements;"
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; DESCRIBE promotions;"
```

![Estructura de las 3 tablas](evidencias/EVI-05-07-describe-tablas.png)

**7. Probar en el shell**

```python
from apps.catalog.models import Product, Supply, Recipe, Promotion
from apps.production.models import ProductionBatch, SupplyMovement
from decimal import Decimal
from django.utils import timezone
from django.db.models import ProtectedError

p = Product.objects.create(sku="TEST-004", name="Pan de prueba 4", price=Decimal("1000.00"))
s = Supply.objects.create(code="INS-004", name="Harina 4", unit_of_measure="kg", min_stock=Decimal("5.00"))
r = Recipe.objects.create(product=p, name="Receta prueba 4")

print("Product:", p.id, p.status)
print("Supply:", s.id, s.status)
print("Recipe:", r.id, r.status)

promo = Promotion.objects.create(name="Promo 2x1 test")
print("Promotion:", promo.id, promo.status)

pb = ProductionBatch.objects.create(recipe=r, name="Lote de prueba 2")
print("ProductionBatch:", pb.id, pb.status, pb.created_at is not None)

sm1 = SupplyMovement.objects.create(
    production_batch=pb, supply=s, type="IN", date=timezone.now(),
    quantity=Decimal("10.00"), notes="Compra de insumo", status="completed"
)
print("SupplyMovement con lote:", sm1.id)

sm2 = SupplyMovement.objects.create(
    supply=s, type="OUT", date=timezone.now(),
    quantity=Decimal("2.00"), status="pending"
)
print("SupplyMovement sin lote:", sm2.id)

try:
    pb.delete()
except ProtectedError:
    print("OK: rechazó borrar el lote con movimientos")

try:
    r.delete()
except ProtectedError:
    print("OK: rechazó borrar la receta con lotes")
```

Resultado:
```
Product: 6 True
Supply: 5 True
Recipe: 4 True
Promotion: 4 True
ProductionBatch: 3 True True
SupplyMovement con lote: 5
SupplyMovement sin lote: 6
OK: rechazó borrar el lote con movimientos
OK: rechazó borrar la receta con lotes
```

![Pruebas en shell](evidencias/EVI-05-08-shell-test.png)

**8. Verificar los datos en MySQL**

```bash
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; SELECT id, name, status FROM promotions;"
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; SELECT id, recipe_id, name, status FROM production_batches;"
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; SELECT id, production_batch_id, supply_id, type, quantity, status FROM supply_movements;"
```

![Datos insertados](evidencias/EVI-05-09-datos-mysql.png)

### Explicación

- **`ProductionBatch`** se vincula a una `Recipe` con `on_delete=PROTECT`. Tiene timestamps porque su tabla original los tiene.
- **`SupplyMovement`** tiene `production_batch` **nullable** (movimientos sin lote, como compras directas) y `supply` obligatorio. Su `status` es `CharField` (texto de flujo) y no booleano, respetando el esquema original.
- **`Promotion`** no tiene FK a productos, siguiendo el diseño original del proyecto.
- `PROTECT` impide eliminar una receta con lotes ni un lote con movimientos. Django lanza `ProtectedError` en ambos casos.

```
catalog/       → products, supplies, recipes, recipe_supplies, promotions
production/    → production_batches, supply_movements
sale/          → (pendiente ISS-06)
```

### Criterios de aceptación

- **AC-05-01:** la FK `recipe_id` de `ProductionBatch` es obligatoria (`null=False`).
- **AC-05-02:** borrar un lote con movimientos falla con `ProtectedError`.
- **AC-05-03:** borrar una receta con lotes falla con `ProtectedError`.
- **AC-05-04:** los `status` por defecto son `True` (booleano) en `ProductionBatch` y `Promotion`, y texto libre en `SupplyMovement`.

### Verificación

```bash
python manage.py migrate
python manage.py shell
```

![Pruebas en shell](evidencias/EVI-05-08-shell-test.png)

![Datos insertados](evidencias/EVI-05-09-datos-mysql.png)

### GATE

| **AC**   | **Verificación**                  | **Evidencia** | **Resultado** |
|----------|-----------------------------------|---------------|---------------|
| AC-05-01 | FK `recipe_id` sin null           | EVI-05-07     | PASS          |
| AC-05-02 | `ProtectedError` al borrar lote   | EVI-05-08     | PASS          |
| AC-05-03 | `ProtectedError` al borrar receta | EVI-05-08     | PASS          |
| AC-05-04 | defaults de status                | EVI-05-08     | PASS          |

---

## ISS-06 — Modelos Sale, SaleDetail y Payment

### Narrativa

Con el catálogo y la producción modelados, el siguiente paso consiste en representar las transacciones comerciales de HornoRaíz. Se modelan las ventas (`Sale`), sus líneas de detalle (`SaleDetail`) y los pagos (`Payment`). Cada venta guarda el `unit_price` en el momento de la venta, de modo que si el precio del producto cambia después, la venta conserva el valor histórico aplicado. El detalle no se reemplaza por un `ManyToManyField`, porque cada línea tiene información propia: cantidad, precio unitario, total y observaciones. La relación con el cliente es un `IntegerField` sin FK, porque las ventas de mostrador pueden no tener cliente registrado, respetando el esquema original.

### Objetivo

Persistir y administrar las ventas, sus líneas de detalle y los pagos de HornoRaíz, respetando el esquema original de las tablas `sales`, `sale_details` y `payments`, garantizando el precio histórico por línea.

### Requisitos

- ISS-05 superado: catálogo y producción modelados.
- Terminal con el entorno virtual `.venv` activo.
- Aplicación `sale` registrada en la configuración.
- Modelo `Product` disponible en `apps/catalog`.

### Construcción

**1. Confirmar el entorno**

```bash
cd /root/bdii/Backend
source .venv/bin/activate
which python
```

![Entorno virtual activo](evidencias/EVI-06-01-venv-activo.png)

**2. Crear el manager de ventas**

`apps/sale/managers.py` es nuevo. En este ISS el manager todavía no registra la venta: solo permite que el modelo `Sale` tenga un manager propio (`objects`) con su `QuerySet`.

```python
from django.db import models


class SaleQuerySet(models.QuerySet):
    pass


class SaleManager(models.Manager.from_queryset(SaleQuerySet)):
    pass
```

![apps/sale/managers.py](evidencias/EVI-06-02-managers-py.png)

**3. Escribir los modelos de venta**

```python
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from apps.catalog.models import Product
from apps.sale.managers import SaleManager


class Sale(models.Model):
    client_id = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    taxes = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30)

    objects = SaleManager()

    class Meta:
        db_table = "sales"
        verbose_name = "venta"
        verbose_name_plural = "ventas"
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"Venta {self.pk}"


class SaleDetail(models.Model):
    sale = models.ForeignKey(
        Sale,
        on_delete=models.PROTECT,
        related_name="details",
        db_column="header_id",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="sale_details",
        db_column="item_id",
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "sale_details"
        verbose_name = "detalle de venta"
        verbose_name_plural = "detalles de venta"
        ordering = ["id"]

    def __str__(self):
        return f"{self.product} x {self.quantity}"

    def save(self, *args, **kwargs):
        self.total = (self.unit_price * self.quantity).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)


class Payment(models.Model):
    reference_type = models.CharField(max_length=50)
    reference_id = models.IntegerField()
    method = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    status = models.CharField(max_length=30)

    class Meta:
        db_table = "payments"
        verbose_name = "pago"
        verbose_name_plural = "pagos"
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"Pago {self.pk} - {self.amount}"
```

![apps/sale/models.py](evidencias/EVI-06-03-sale-models.png)

**4. Generar la migración**

```bash
python manage.py makemigrations sale
```

Resultado:
```
Migrations for 'sale':
  apps/sale/migrations/0001_initial.py
    + Create model Payment
    + Create model Sale
    + Create model SaleDetail
```

![makemigrations](evidencias/EVI-06-04-makemigrations.png)

**5. Migrar**

```bash
python manage.py migrate
```

Resultado:
```
Applying sale.0001_initial... OK
```

![migrate](evidencias/EVI-06-05-migrate.png)

**6. Verificar las tablas en MySQL**

```bash
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; SHOW TABLES;"
```

![Tablas creadas](evidencias/EVI-06-06-tablas-creadas.png)

```bash
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; DESCRIBE sales;"
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; DESCRIBE sale_details;"
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; DESCRIBE payments;"
```

![Estructura de las 3 tablas](evidencias/EVI-06-07-describe-tablas.png)

**7. Probar en el shell**

```python
from apps.catalog.models import Product
from apps.sale.models import Sale, SaleDetail, Payment
from decimal import Decimal
from django.utils import timezone
from django.db.models import ProtectedError

p = Product.objects.filter(sku="TEST-004").first()
print("Producto base:", p.id, p.name, "precio actual:", p.price)

sale = Sale.objects.create(
    client_id=None,
    date=timezone.now(),
    subtotal=Decimal("1000.00"),
    taxes=Decimal("190.00"),
    total=Decimal("1190.00"),
    status="paid",
)
print("Sale:", sale.id, sale.status, sale.total)

det = SaleDetail.objects.create(
    sale=sale,
    product=p,
    quantity=Decimal("2.00"),
    unit_price=Decimal("500.00"),
)
print("SaleDetail:", det.id, "unit_price:", det.unit_price, "total:", det.total)

pay = Payment.objects.create(
    reference_type="sale",
    reference_id=sale.id,
    method="cash",
    amount=Decimal("1190.00"),
    date=timezone.now(),
    status="completed",
)
print("Payment:", pay.id, pay.method, pay.amount)

# Precio histórico
p_orig_price = p.price
p.price = Decimal("9999.99")
p.save()
det.refresh_from_db()
print("Precio del producto cambió a:", p.price)
print("unit_price del detalle sigue siendo:", det.unit_price)

p.price = p_orig_price
p.save()

# PROTECT
try:
    sale.delete()
except ProtectedError:
    print("OK: rechazó borrar la venta con detalles")
```

Resultado:
```
Producto base: 6 Pan de prueba 4 precio actual: 1000.00
Sale: 1 paid 1190.00
SaleDetail: 1 unit_price: 500.00 total: 1000.00
Payment: 1 cash 1190.00
Precio del producto cambió a: 9999.99
unit_price del detalle sigue siendo: 500.00
OK: rechazó borrar la venta con detalles
```

![Pruebas en shell](evidencias/EVI-06-08-shell-test.png)

**8. Verificar los datos en MySQL**

```bash
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; SELECT id, client_id, date, subtotal, taxes, total, status FROM sales;"
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; SELECT id, header_id, item_id, quantity, unit_price, total, notes FROM sale_details;"
docker exec mysql-server mysql -u admin -p1704 -e "USE hornoraiz_django; SELECT id, reference_type, reference_id, method, amount, status FROM payments;"
```

![Datos insertados](evidencias/EVI-06-09-datos-mysql.png)

### Explicación

- **`Sale`** guarda la fecha, el `subtotal`, los `taxes`, el `total` y el `status` como `varchar(30)`. Su `client_id` es un `IntegerField` **sin FK**, porque las ventas de mostrador pueden no tener cliente registrado.
- **`SaleDetail`** tiene `unit_price` como columna, de modo que si el precio del producto cambia después, la venta conserva el valor histórico aplicado. El `total` se recalcula en `save()` para que no se persista un valor distinto de `unit_price × quantity`.
- **`Payment`** guarda la referencia polimórfica (`reference_type` + `reference_id`), el método de pago y el estado como `varchar(30)`.
- No hay `ManyToManyField`. La navegación es `sale.details.all()`.
- `PROTECT` impide eliminar una venta que tenga líneas de detalle.

```
Sale 1 ─────── N SaleDetail N ─────── 1 Product
```

### Criterios de aceptación

- **AC-06-01:** existen las tablas `sales`, `sale_details` y `payments`.
- **AC-06-02:** las FK de `SaleDetail` usan `PROTECT`.
- **AC-06-03:** `SaleDetail.total` se recalcula en `save()` a partir de `unit_price × quantity`.
- **AC-06-04:** no hay `ManyToManyField` hacia `Product`.
- **AC-06-05:** el `unit_price` guardado en el detalle no cambia aunque el precio del producto cambie después.

### Verificación

```bash
python manage.py migrate
python manage.py shell
```

![Pruebas en shell](evidencias/EVI-06-08-shell-test.png)

![Datos insertados](evidencias/EVI-06-09-datos-mysql.png)

### GATE

| **AC**   | **Verificación**                            | **Evidencia** | **Resultado** |
|----------|---------------------------------------------|---------------|---------------|
| AC-06-01 | tablas `sales`, `sale_details`, `payments`  | EVI-06-07     | PASS          |
| AC-06-02 | `on_delete=PROTECT` en `SaleDetail`         | EVI-06-07     | PASS          |
| AC-06-03 | `total` recalculado en `save()`             | EVI-06-08     | PASS          |
| AC-06-04 | ausencia de `ManyToManyField`               | EVI-06-03     | PASS          |
| AC-06-05 | precio histórico del detalle                | EVI-06-08     | PASS          |

---

## ISS-07 — Serializers y JSON camelCase

### Narrativa

Con los modelos de negocio de HornoRaíz ya implementados y migrados, el siguiente paso consiste en crear la capa de comunicación entre el backend y el frontend. Se instaló Django REST Framework, junto con `djangorestframework-camel-case` y `django-cors-headers`. Los campos del modelo siguen en `snake_case` (`created_at`, `unit_price`, `client_id`), pero la API los expone en `camelCase` (`createdAt`, `unitPrice`, `clientId`) sin modificar los modelos ni las columnas de MySQL. La conversión ocurre solo en el borde HTTP.

### Objetivo

Convertir los modelos de HornoRaíz en respuestas JSON y validar los datos recibidos por la API, utilizando nombres de campos `camelCase` sin modificar los modelos existentes.

### Requisitos

- ISS-06 superado: modelos de venta, detalle y pago implementados.
- Terminal con el entorno virtual `.venv` activo.
- Modelos y migraciones de HornoRaíz disponibles.

### Construcción

**1. Confirmar el entorno**

```bash
cd /root/bdii/Backend
source .venv/bin/activate
which python
```

![Entorno virtual activo](evidencias/EVI-07-01-venv-activo.png)

**2. Instalar los paquetes de la API**

```bash
python -m pip install "djangorestframework==3.17.2" "djangorestframework-camel-case==1.4.2" "django-cors-headers==4.9.0"
python -m pip freeze > requirements.txt
```

![Instalación de paquetes](evidencias/EVI-07-02-instalacion-paquetes.png)

**3. Parchear `config/settings/__init__.py`**

Se agregaron `rest_framework` y `corsheaders` a `INSTALLED_APPS`, el middleware de CORS, y la configuración `REST_FRAMEWORK` con renderers y parsers en camelCase.

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "apps.security.apps.SecurityConfig",
    "apps.catalog.apps.CatalogConfig",
    "apps.production.apps.ProductionConfig",
    "apps.sale.apps.SaleConfig",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

Debajo de `DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"`:

```python
CORS_ALLOW_ALL_ORIGINS = os.environ.get("CORS_ALLOW_ALL_ORIGINS", "True").strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
    ],
    "DEFAULT_PAGINATION_CLASS": None,
}
```

![config/settings/__init__.py](evidencias/EVI-07-03-settings.png)

**4. Serializers de `catalog`**

Se creó `apps/catalog/serializers.py` con `ProductSerializer`, `SupplySerializer`, `RecipeSerializer`, `RecipeSupplySerializer` y `PromotionSerializer`.

```python
from rest_framework import serializers

from apps.catalog.models import Product, Supply, Recipe, RecipeSupply, Promotion


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "sku",
            "name",
            "description",
            "price",
            "status",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "sku": {"max_length": 50},
            "name": {"min_length": 2, "max_length": 100},
            "description": {"required": False, "allow_null": True, "allow_blank": True},
        }

    def validate_description(self, value):
        if value is None or str(value).strip() == "":
            return None
        return value


class SupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply
        fields = [
            "id",
            "code",
            "name",
            "unit_of_measure",
            "min_stock",
            "status",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "code": {"max_length": 50},
            "name": {"min_length": 2, "max_length": 100},
            "unit_of_measure": {"max_length": 30},
        }


class RecipeSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = Recipe
        fields = [
            "id",
            "product",
            "product_name",
            "name",
            "description",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "product_name", "created_at", "updated_at"]
        extra_kwargs = {
            "name": {"min_length": 2, "max_length": 100},
            "description": {"required": False, "allow_null": True, "allow_blank": True},
        }

    def validate_description(self, value):
        if value is None or str(value).strip() == "":
            return None
        return value


class RecipeSupplySerializer(serializers.ModelSerializer):
    main_name = serializers.CharField(source="main.name", read_only=True)
    related_name = serializers.CharField(source="related.name", read_only=True)

    class Meta:
        model = RecipeSupply
        fields = [
            "id",
            "main",
            "main_name",
            "related",
            "related_name",
            "relation_data",
            "status",
        ]
        read_only_fields = ["id", "main_name", "related_name"]
        extra_kwargs = {
            "relation_data": {"required": False, "allow_null": True, "allow_blank": True},
        }


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = [
            "id",
            "name",
            "description",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
        extra_kwargs = {
            "name": {"min_length": 2, "max_length": 100},
            "description": {"required": False, "allow_null": True, "allow_blank": True},
        }

    def validate_description(self, value):
        if value is None or str(value).strip() == "":
            return None
        return value
```

![apps/catalog/serializers.py](evidencias/EVI-07-04-catalog-serializers.png)

**5. Serializers de `production`**

Se creó `apps/production/serializers.py` con `ProductionBatchSerializer` y `SupplyMovementSerializer`.

```python
from rest_framework import serializers

from apps.production.models import ProductionBatch, SupplyMovement


class ProductionBatchSerializer(serializers.ModelSerializer):
    recipe_name = serializers.CharField(source="recipe.name", read_only=True)

    class Meta:
        model = ProductionBatch
        fields = [
            "id",
            "recipe",
            "recipe_name",
            "name",
            "description",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "recipe_name", "created_at", "updated_at"]
        extra_kwargs = {
            "name": {"min_length": 2, "max_length": 100},
            "description": {"required": False, "allow_null": True, "allow_blank": True},
        }

    def validate_description(self, value):
        if value is None or str(value).strip() == "":
            return None
        return value


class SupplyMovementSerializer(serializers.ModelSerializer):
    supply_name = serializers.CharField(source="supply.name", read_only=True)
    production_batch_name = serializers.CharField(
        source="production_batch.name",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = SupplyMovement
        fields = [
            "id",
            "production_batch",
            "production_batch_name",
            "supply",
            "supply_name",
            "type",
            "date",
            "quantity",
            "notes",
            "status",
        ]
        read_only_fields = ["id", "supply_name", "production_batch_name"]
        extra_kwargs = {
            "production_batch": {"required": False, "allow_null": True},
            "notes": {"required": False, "allow_null": True, "allow_blank": True},
        }

    def validate_notes(self, value):
        if value is None or str(value).strip() == "":
            return None
        return value
```

![apps/production/serializers.py](evidencias/EVI-07-05-production-serializers.png)

**6. Serializers de `sale`**

Se creó `apps/sale/serializers.py` con `SaleSerializer`, `SaleDetailSerializer` y `PaymentSerializer`.

```python
from rest_framework import serializers

from apps.sale.models import Sale, SaleDetail, Payment


class SaleDetailSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = SaleDetail
        fields = [
            "id",
            "sale",
            "product",
            "product_name",
            "quantity",
            "unit_price",
            "total",
            "notes",
        ]
        read_only_fields = ["id", "product_name", "total"]
        extra_kwargs = {
            "notes": {"required": False, "allow_null": True, "allow_blank": True},
        }

    def validate_notes(self, value):
        if value is None or str(value).strip() == "":
            return None
        return value


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "reference_type",
            "reference_id",
            "method",
            "amount",
            "date",
            "status",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "reference_type": {"max_length": 50},
            "method": {"max_length": 50},
            "status": {"max_length": 30},
        }


class SaleSerializer(serializers.ModelSerializer):
    details = SaleDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Sale
        fields = [
            "id",
            "client_id",
            "date",
            "subtotal",
            "taxes",
            "total",
            "status",
            "details",
        ]
        read_only_fields = ["id", "details"]
        extra_kwargs = {
            "client_id": {"required": False, "allow_null": True},
        }
```

![apps/sale/serializers.py](evidencias/EVI-07-06-sale-serializers.png)

**7. Verificar la configuración**

```bash
python manage.py check
```

![Check exitoso](evidencias/EVI-07-07-check-ok.png)

**8. Probar el camelCase en el shell**

En el shell de Django hay que usar explícitamente `CamelCaseJSONRenderer()` porque el `JSONRenderer` plano no aplica la conversión. Cuando la respuesta sale por HTTP (a través de los ViewSets del ISS-08), DRF aplica automáticamente el renderer configurado.

```python
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from apps.catalog.serializers import ProductSerializer, RecipeSerializer, PromotionSerializer
from apps.catalog.models import Product, Recipe, Promotion
from decimal import Decimal

p = Product.objects.create(sku="ISS07-002", name="Producto ISS07-002", price=Decimal("500.00"))
json_p = CamelCaseJSONRenderer().render(ProductSerializer(p).data).decode("utf-8")
print("Product JSON:")
print(json_p)

r = Recipe.objects.create(product=p, name="Receta ISS07-002")
json_r = CamelCaseJSONRenderer().render(RecipeSerializer(r).data).decode("utf-8")
print("\nRecipe JSON:")
print(json_r)
assert "createdAt" in json_r
assert "created_at" not in json_r
print("✓ Recipe usa createdAt")

promo = Promotion.objects.create(name="Promo ISS07-002")
json_promo = CamelCaseJSONRenderer().render(PromotionSerializer(promo).data).decode("utf-8")
print("\nPromotion JSON:")
print(json_promo)
assert "createdAt" in json_promo
assert "created_at" not in json_promo
print("✓ Promotion usa createdAt")
```

Resultado:
```
Product JSON:
{"id":8,"sku":"ISS07-002","name":"Producto ISS07-002","description":null,"price":"500.00","status":true}

Recipe JSON:
{"id":6,"product":8,"productName":"Producto ISS07-002","name":"Receta ISS07-002",
 "description":null,"status":true,"createdAt":"2026-10-12T22:07:56.548399-05:00","updatedAt":"..."}
✓ Recipe usa createdAt

Promotion JSON:
{"id":6,"name":"Promo ISS07-002","description":null,"status":true,
 "createdAt":"2026-10-12T22:07:56.574800-05:00","updatedAt":"..."}
✓ Promotion usa createdAt
```

![Prueba camelCase en shell](evidencias/EVI-07-08-camelcase-test.png)

### Explicación

La conversión de nombres ocurre en el borde HTTP:

```
Python (created_at)  →  MySQL (created_at)  →  JSON API (createdAt)
                                            ←  Parser (createdAt)
```

Los serializers no usan `fields = "__all__"`: cada campo que se expone en la API se declara explícitamente. Los campos derivados (`product_name`, `productName`) se declaran de solo lectura con `CharField(source="...", read_only=True)` para no requerir queries adicionales del cliente.

El parser hace el camino inverso al recibir JSON. Los modelos y las columnas de MySQL permanecen en `snake_case`; no se renombran.

### Criterios de aceptación

- **AC-07-01:** el JSON de una receta o promoción contiene `createdAt` y no `created_at`.
- **AC-07-02:** los serializers exponen `productName`, `unitOfMeasure`, `minStock`, `unitPrice`, `referenceType` en `camelCase`.
- **AC-07-03:** los campos derivados (`productName`, `recipeName`) se incluyen sin requerir queries adicionales del cliente.

### Verificación

```bash
python manage.py check
python manage.py shell
```

![Check exitoso](evidencias/EVI-07-07-check-ok.png)

![Prueba camelCase en shell](evidencias/EVI-07-08-camelcase-test.png)

### GATE

| **AC**   | **Verificación**                     | **Evidencia** | **Resultado** |
|----------|--------------------------------------|---------------|---------------|
| AC-07-01 | `createdAt` presente en JSON         | EVI-07-08     | PASS          |
| AC-07-02 | campos derivados en `camelCase`      | EVI-07-04     | PASS          |
| AC-07-03 | `productName` sin query adicional    | EVI-07-08     | PASS          |