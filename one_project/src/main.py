from fastapi import FastAPI

from src.routes.product_routes import router as product_router


# Crea la instancia principal de la API.
app = FastAPI(
    title="API REST - Gestión de Productos",
    description=(
        "API REST desarrollada con Python y FastAPI "
        "para administrar productos."
    ),
    version="1.0.0"
)


# Registra las rutas relacionadas con los productos.
app.include_router(product_router)


# Define la respuesta de la ruta principal de la API.
@app.get("/")
def root():

    return {
        "success": True,
        "message": "API de productos funcionando correctamente"
    }