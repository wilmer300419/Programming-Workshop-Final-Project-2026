from fastapi import FastAPI

from src.routes.product_routes import router as product_router


app = FastAPI(
    title="API REST - Gestión de Productos",
    description=(
        "API REST desarrollada con Python y FastAPI "
        "para administrar productos."
    ),
    version="1.0.0"
)


app.include_router(product_router)


@app.get("/")
def root():

    return {
        "success": True,
        "message": "API de productos funcionando correctamente"
    }