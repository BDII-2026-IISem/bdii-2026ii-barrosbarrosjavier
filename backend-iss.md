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