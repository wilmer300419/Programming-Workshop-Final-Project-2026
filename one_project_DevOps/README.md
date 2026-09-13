# API REST - Gestión de Productos

API REST desarrollada con **Python y FastAPI** para administrar productos mediante operaciones CRUD.
La información se almacena en un archivo **JSON**, sin utilizar una base de datos.

## Tecnologías

* Python
* FastAPI
* Uvicorn
* Pydantic
* JSON

## Estructura

```text
src/
├── database/    # Archivo JSON y manejo de datos
├── models/      # Modelos y validaciones
├── routes/      # Endpoints
├── services/    # Lógica del sistema
├── security/    # Seguridad
├── utils/       # Respuestas y utilidades
└── main.py      # Inicio de la API

requirements.txt
README.md
```

## Producto

| Campo     | Tipo    |
| --------- | ------- |
| id        | Entero  |
| nombre    | Texto   |
| categoria | Texto   |
| precio    | Decimal |
| stock     | Entero  |

## Endpoints

| Método | Endpoint         | Descripción           |
| ------ | ---------------- | --------------------- |
| GET    | `/products/`     | Consultar productos   |
| GET    | `/products/{id}` | Consultar un producto |
| POST   | `/products/`     | Registrar producto    |
| PUT    | `/products/{id}` | Actualizar producto   |
| DELETE | `/products/{id}` | Eliminar producto     |

## Validaciones

* El nombre es obligatorio.
* El precio debe ser mayor que `0`.
* El stock no puede ser negativo.
* El ID es generado automáticamente y es único.
* Los productos inexistentes generan `404 Not Found`.

## Instalación

Crear y activar el entorno virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn src.main:app --reload
```

La API estará disponible en:

```text
http://127.0.0.1:8000
```

### Documentación

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Autores

* **Esteban Salvador Guzman**
* **Santiago Santana Nieto**
* **Wilmer Andrés Capera Hernández**
* **Jairo Esteban Ojeda Ramirez**
