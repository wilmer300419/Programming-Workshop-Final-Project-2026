from fastapi import HTTPException

from src.database.json_repository import (
    read_products,
    write_products
)

from src.models.product import ProductCreate

from src.utils.logger import logger


def get_all_products():

    logger.info(
        "START GET_ALL_PRODUCTS - Iniciando consulta de productos"
    )

    products = read_products()

    logger.info(
        f"SUCCESS GET_ALL_PRODUCTS - "
        f"Consulta exitosa. Total productos: {len(products)}"
    )

    return products


def get_product_by_id(product_id: int):

    logger.info(
        f"START GET_PRODUCT - Buscando producto ID {product_id}"
    )

    products = read_products()

    for product in products:

        if product["id"] == product_id:

            logger.info(
                f"SUCCESS GET_PRODUCT - "
                f"Producto ID {product_id} encontrado"
            )

            return product

    logger.error(
        f"ERROR GET_PRODUCT - "
        f"Producto ID {product_id} no encontrado"
    )

    raise HTTPException(
        status_code=404,
        detail="El producto no existe"
    )


def create_product(product: ProductCreate):

    logger.info(
        "START CREATE_PRODUCT - "
        f"Iniciando registro del producto '{product.nombre}'"
    )

    products = read_products()

    if not product.nombre.strip():

        logger.error(
            "ERROR CREATE_PRODUCT - "
            "El nombre del producto está vacío"
        )

        raise HTTPException(
            status_code=400,
            detail="El nombre del producto es obligatorio"
        )

    if products:

        new_id = max(
            item["id"] for item in products
        ) + 1

    else:

        new_id = 1

    new_product = {
        "id": new_id,
        "nombre": product.nombre,
        "categoria": product.categoria,
        "precio": product.precio,
        "stock": product.stock
    }

    products.append(new_product)

    write_products(products)

    logger.info(
        f"SUCCESS CREATE_PRODUCT - "
        f"Producto registrado correctamente. ID {new_id}"
    )

    return new_product



def update_product(
    product_id: int,
    product: ProductCreate
):

    logger.info(
        f"START UPDATE_PRODUCT - "
        f"Iniciando actualización del producto ID {product_id}"
    )

    products = read_products()

    for index, item in enumerate(products):

        if item["id"] == product_id:

            updated_product = {
                "id": product_id,
                "nombre": product.nombre,
                "categoria": product.categoria,
                "precio": product.precio,
                "stock": product.stock
            }

            products[index] = updated_product

            write_products(products)

            logger.info(
                f"SUCCESS UPDATE_PRODUCT - "
                f"Producto ID {product_id} actualizado correctamente"
            )

            return updated_product

    logger.error(
        f"ERROR UPDATE_PRODUCT - "
        f"Producto ID {product_id} no encontrado"
    )

    raise HTTPException(
        status_code=404,
        detail="El producto no existe"
    )



def delete_product(product_id: int):

    logger.info(
        f"START DELETE_PRODUCT - "
        f"Iniciando eliminación del producto ID {product_id}"
    )

    products = read_products()

    for index, product in enumerate(products):

        if product["id"] == product_id:

            deleted_product = products.pop(index)

            write_products(products)

            logger.info(
                f"SUCCESS DELETE_PRODUCT - "
                f"Producto ID {product_id} eliminado correctamente"
            )

            return deleted_product

    logger.error(
        f"ERROR DELETE_PRODUCT - "
        f"Producto ID {product_id} no encontrado"
    )

    raise HTTPException(
        status_code=404,
        detail="El producto no existe"
    )
