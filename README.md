# TodoAPI

Una API RESTful para gestionar tareas (todos) desarrollada con **FastAPI** y **MongoDB**. Permite crear, leer, actualizar y eliminar tareas, con soporte para pruebas automatizadas y despliegue en Railway.

## Requisitos previos

- **Python 3.10+**
- **MongoDB** (local o en la nube, por ejemplo, MongoDB Atlas)
- **Git** (para clonar el repositorio)
- Acceso a una terminal (bash, PowerShell, etc.)

## Configuración del entorno

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
```

### 2. Crear y activar un entorno virtual

Crea un entorno virtual para aislar las dependencias:

```bash
# En Linux/MacOS
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

Instala las dependencias de producción y desarrollo:

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

- `requirements.txt`: Dependencias necesarias para ejecutar la API (FastAPI, Uvicorn, Motor, etc.).
- `requirements-dev.txt`: Dependencias para pruebas (Pytest, Pytest-Asyncio, HTTPX).

### 4. Configurar variables de entorno

Encontraras un archivo env.example en app/core/.env.example con el cual podrás agregar las variables de entorno.

```bash
MONGODB_URL="url"
DATABASE_NAME=database_name
COLLECTION_NAME=collection_name
```

- `MONGODB_URL`: URL de conexión a tu base de datos MongoDB (cámbiala si usas MongoDB Atlas).
- `MONGODATABASE`: Nombre de la base de datos (por ejemplo, `todo_db`).
- `COLLECTION_NAME`: Nombre de la Colección (por ejemplo, `todos`).

Asegúrate de que tu servidor MongoDB esté corriendo localmente o accesible en la nube.(En mi caso use Atlas)

## Ejecutar la aplicación

Para iniciar la API localmente, desde el root ejecuta:

```bash
uvicorn app.main:app --reload
```

- La API estará disponible en `http://localhost:8000`.
- Accede a la documentación interactiva en `http://localhost:8000/docs`.

## Ejecutar los tests

Para correr las pruebas automatizadas:

```bash
pytest -s -v tests/
```

- Los tests usan una base de datos de prueba (`todo_db_test`) definida en `tests/conftest.py`.
- Asegúrate de que MongoDB esté corriendo y que `MONGODB_URL` esté configurado en `.env`.

## Despliegue

La API está desplegada en Railway y accesible en:

**[todo-api-production-877c.up.railway.app](todo-api-production-877c.up.railway.app)**

- La ruta raíz (`/`) redirige automáticamente a `/docs` para mostrar la documentación interactiva.
- Consulta los endpoints disponibles en la documentación Swagger.
