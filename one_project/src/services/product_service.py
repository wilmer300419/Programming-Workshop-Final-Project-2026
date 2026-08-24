from fastapi import HTTPException

from src.database.json_repository import (
    read_products,
    write_products
)

from src.models.product import (
    ProductCreate,
    ProductResponse
)


def get_all_products():

    products = read_products()

    return products


def get_product_by_id(product_id: int):

    products = read_products()

    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(
        status_code=404,
        detail="El producto no existe"
    )


def create_product(product: ProductCreate):

    products = read_products()

    # Verificar que el nombre no esté vacío
    if not product.nombre.strip():
        raise HTTPException(
            status_code=400,
            detail="El nombre del producto es obligatorio"
        )

    # Generar ID
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

    return new_product


def update_product(
    product_id: int,
    product: ProductCreate
):

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

            return updated_product

    raise HTTPException(
        status_code=404,
        detail="El producto no existe"
    )


def delete_product(product_id: int):

    products = read_products()

    for index, product in enumerate(products):

        if product["id"] == product_id:

            deleted_product = products.pop(index)

            write_products(products)

            return deleted_product

    raise HTTPException(
        status_code=404,
        detail="El producto no existe"
    )