# Importa APIRouter para crear y agrupar las rutas de la API.
# También importa status para utilizar los códigos HTTP de forma descriptiva.
from fastapi import APIRouter, status


# Importa el modelo ProductCreate, utilizado para validar
# los datos recibidos al crear o actualizar un producto.
from src.models.product import ProductCreate


# Importa las funciones del servicio de productos.
# Estas funciones contienen la lógica de negocio y el acceso
# a los datos de los productos.
from src.services.product_service import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product
)


# Importa una función encargada de construir respuestas
# estandarizadas para la API.
from src.utils.response import success_response


# Crea un router para agrupar todas las rutas relacionadas
# con los productos.
#
# prefix="/products":
# Todas las rutas de este router comenzarán con /products.
#
# tags=["Products"]:
# Agrupa estas rutas bajo "Products" en la documentación
# automática de FastAPI (Swagger).
router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# ============================================================
# GET - CONSULTAR TODOS LOS PRODUCTOS
# ============================================================

# Define una ruta GET para consultar todos los productos.
#
# La ruta final será:
# GET /products/
#
# status_code=200 indica que la consulta fue exitosa.
#
# summary es el texto que aparecerá en la documentación
# automática de FastAPI.
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Consultar todos los productos"
)
def get_products():

    # Llama al servicio encargado de obtener todos
    # los productos registrados.
    products = get_all_products()

    # Retorna una respuesta estandarizada indicando
    # que la consulta fue realizada correctamente.
    return success_response(
        "Productos consultados correctamente",
        products
    )


# ============================================================
# GET - CONSULTAR UN PRODUCTO POR ID
# ============================================================

# Define una ruta GET para consultar un producto específico.
#
# La ruta final será:
# GET /products/{product_id}
#
# {product_id} es un parámetro dinámico que representa
# el identificador del producto.
@router.get(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    summary="Consultar un producto"
)
def get_product(product_id: int):

    # Busca el producto utilizando el ID recibido.
    #
    # ": int" indica que FastAPI espera que product_id
    # sea un número entero.
    product = get_product_by_id(product_id)

    # Retorna el producto encontrado utilizando
    # la estructura de respuesta estandarizada.
    return success_response(
        "Producto encontrado correctamente",
        product
    )


# ============================================================
# POST - CREAR UN PRODUCTO
# ============================================================

# Define una ruta POST para registrar un nuevo producto.
#
# La ruta final será:
# POST /products/
#
# HTTP_201_CREATED indica que un nuevo recurso
# fue creado correctamente.
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un producto"
)
def create_new_product(product: ProductCreate):

    # Recibe los datos del producto mediante el modelo
    # ProductCreate.
    #
    # FastAPI utiliza Pydantic para validar automáticamente
    # los datos recibidos antes de ejecutar esta función.
    #
    # Luego envía el producto al servicio encargado
    # de realizar la creación.
    new_product = create_product(product)

    # Retorna el producto creado mediante una
    # respuesta estandarizada.
    return success_response(
        "Producto registrado correctamente",
        new_product
    )


# ============================================================
# PUT - ACTUALIZAR UN PRODUCTO
# ============================================================

# Define una ruta PUT para actualizar un producto existente.
#
# La ruta final será:
# PUT /products/{product_id}
#
# Recibe el ID del producto y los nuevos datos.
@router.put(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    summary="Actualizar un producto"
)
def update_existing_product(
    product_id: int,
    product: ProductCreate
):

    # Llama al servicio encargado de actualizar el producto.
    #
    # Se envían dos parámetros:
    # 1. product_id -> identifica qué producto actualizar.
    # 2. product -> contiene los nuevos datos.
    updated_product = update_product(
        product_id,
        product
    )

    # Retorna el producto actualizado utilizando
    # la estructura estándar de respuesta.
    return success_response(
        "Producto actualizado correctamente",
        updated_product
    )


# ============================================================
# DELETE - ELIMINAR UN PRODUCTO
# ============================================================

# Define una ruta DELETE para eliminar un producto.
#
# La ruta final será:
# DELETE /products/{product_id}
@router.delete(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar un producto"
)
def delete_existing_product(product_id: int):

    # Llama al servicio encargado de eliminar
    # el producto utilizando su identificador.
    deleted_product = delete_product(product_id)

    # Retorna información sobre el producto eliminado
    # mediante la respuesta estandarizada.
    return success_response(
        "Producto eliminado correctamente",
        deleted_product
    )