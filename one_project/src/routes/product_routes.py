from fastapi import APIRouter, status

from src.models.product import ProductCreate
from src.services.product_service import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product
)

from src.utils.response import success_response


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Consultar todos los productos"
)
def get_products():

    products = get_all_products()

    return success_response(
        "Productos consultados correctamente",
        products
    )


@router.get(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    summary="Consultar un producto"
)
def get_product(product_id: int):

    product = get_product_by_id(product_id)

    return success_response(
        "Producto encontrado correctamente",
        product
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un producto"
)
def create_new_product(product: ProductCreate):

    new_product = create_product(product)

    return success_response(
        "Producto registrado correctamente",
        new_product
    )


@router.put(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    summary="Actualizar un producto"
)
def update_existing_product(
    product_id: int,
    product: ProductCreate
):

    updated_product = update_product(
        product_id,
        product
    )

    return success_response(
        "Producto actualizado correctamente",
        updated_product
    )


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar un producto"
)
def delete_existing_product(product_id: int):

    deleted_product = delete_product(product_id)

    return success_response(
        "Producto eliminado correctamente",
        deleted_product
    )