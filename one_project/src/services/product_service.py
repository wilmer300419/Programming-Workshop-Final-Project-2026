# Importa HTTPException para poder generar respuestas de error
# con códigos HTTP específicos, por ejemplo 404 o 400.
from fastapi import HTTPException


# Importa las funciones encargadas de leer y escribir
# información en el archivo products.json.
from src.database.json_repository import (
    read_products,
    write_products
)


# Importa el modelo ProductCreate de Pydantic.
# Se utiliza para recibir y validar los datos de un producto.
from src.models.product import ProductCreate


# Importa el logger utilizado para registrar información,
# éxitos y errores durante la ejecución de los servicios.
from src.utils.logger import logger


# ============================================================
# OBTENER TODOS LOS PRODUCTOS
# ============================================================

def get_all_products():

    # Registra en el log que se inició la consulta
    # de todos los productos.
    logger.info(
        "START GET_ALL_PRODUCTS - Iniciando consulta de productos"
    )

    # Lee los productos almacenados en products.json.
    products = read_products()

    # Registra que la consulta fue exitosa e indica
    # cuántos productos fueron encontrados.
    logger.info(
        f"SUCCESS GET_ALL_PRODUCTS - "
        f"Consulta exitosa. Total productos: {len(products)}"
    )

    # Devuelve la lista de productos.
    return products


# ============================================================
# OBTENER UN PRODUCTO POR ID
# ============================================================

def get_product_by_id(product_id: int):

    # Registra el inicio de la búsqueda indicando
    # el ID que se está buscando.
    logger.info(
        f"START GET_PRODUCT - Buscando producto ID {product_id}"
    )

    # Obtiene todos los productos desde el archivo JSON.
    products = read_products()

    # Recorre cada producto de la lista.
    for product in products:

        # Comprueba si el ID del producto coincide
        # con el ID solicitado.
        if product["id"] == product_id:

            # Registra que el producto fue encontrado.
            logger.info(
                f"SUCCESS GET_PRODUCT - "
                f"Producto ID {product_id} encontrado"
            )

            # Devuelve el producto encontrado.
            return product

    # Si el ciclo termina sin encontrar el producto,
    # registra el error.
    logger.error(
        f"ERROR GET_PRODUCT - "
        f"Producto ID {product_id} no encontrado"
    )

    # Genera una excepción HTTP 404 indicando
    # que el producto no existe.
    raise HTTPException(
        status_code=404,
        detail="El producto no existe"
    )


# ============================================================
# CREAR UN PRODUCTO
# ============================================================

def create_product(product: ProductCreate):

    # Registra el inicio del proceso de creación
    # incluyendo el nombre del producto.
    logger.info(
        "START CREATE_PRODUCT - "
        f"Iniciando registro del producto '{product.nombre}'"
    )

    # Obtiene los productos actualmente almacenados.
    products = read_products()

    # Verifica que el nombre no esté compuesto únicamente
    # por espacios en blanco.
    if not product.nombre.strip():

        # Registra el error en el sistema de logs.
        logger.error(
            "ERROR CREATE_PRODUCT - "
            "El nombre del producto está vacío"
        )

        # Genera un error HTTP 400 porque los datos
        # enviados por el cliente no son válidos.
        raise HTTPException(
            status_code=400,
            detail="El nombre del producto es obligatorio"
        )

    # Comprueba si ya existen productos registrados.
    if products:

        # Obtiene el ID más grande de todos los productos
        # y le suma 1 para generar el nuevo ID.
        new_id = max(
            item["id"] for item in products
        ) + 1

    else:

        # Si no existen productos, el primer ID será 1.
        new_id = 1

    # Crea un diccionario con la información
    # del nuevo producto.
    new_product = {
        "id": new_id,
        "nombre": product.nombre,
        "categoria": product.categoria,
        "precio": product.precio,
        "stock": product.stock
    }

    # Agrega el nuevo producto a la lista.
    products.append(new_product)

    # Guarda la lista actualizada en products.json.
    write_products(products)

    # Registra que el producto fue creado correctamente.
    logger.info(
        f"SUCCESS CREATE_PRODUCT - "
        f"Producto registrado correctamente. ID {new_id}"
    )

    # Devuelve el producto recién creado.
    return new_product


# ============================================================
# ACTUALIZAR UN PRODUCTO
# ============================================================

def update_product(
    product_id: int,
    product: ProductCreate
):

    # Registra el inicio del proceso de actualización.
    logger.info(
        f"START UPDATE_PRODUCT - "
        f"Iniciando actualización del producto ID {product_id}"
    )

    # Obtiene todos los productos almacenados.
    products = read_products()

    # enumerate() permite obtener tanto la posición
    # del producto como sus datos.
    for index, item in enumerate(products):

        # Comprueba si el ID del producto actual
        # coincide con el ID que queremos actualizar.
        if item["id"] == product_id:

            # Crea un nuevo diccionario con los datos actualizados.
            #
            # Se mantiene el mismo ID y se reemplazan
            # los demás valores.
            updated_product = {
                "id": product_id,
                "nombre": product.nombre,
                "categoria": product.categoria,
                "precio": product.precio,
                "stock": product.stock
            }

            # Reemplaza el producto antiguo por el producto actualizado.
            products[index] = updated_product

            # Guarda los cambios en products.json.
            write_products(products)

            # Registra que la actualización fue exitosa.
            logger.info(
                f"SUCCESS UPDATE_PRODUCT - "
                f"Producto ID {product_id} actualizado correctamente"
            )

            # Devuelve el producto actualizado.
            return updated_product

    # Si no se encontró ningún producto con ese ID,
    # registra el error.
    logger.error(
        f"ERROR UPDATE_PRODUCT - "
        f"Producto ID {product_id} no encontrado"
    )

    # Devuelve un error HTTP 404.
    raise HTTPException(
        status_code=404,
        detail="El producto no existe"
    )


# ============================================================
# ELIMINAR UN PRODUCTO
# ============================================================

def delete_product(product_id: int):

    # Registra el inicio del proceso de eliminación.
    logger.info(
        f"START DELETE_PRODUCT - "
        f"Iniciando eliminación del producto ID {product_id}"
    )

    # Obtiene todos los productos almacenados.
    products = read_products()

    # Recorre los productos obteniendo tanto
    # la posición como los datos del producto.
    for index, product in enumerate(products):

        # Comprueba si el ID coincide con el producto
        # que se desea eliminar.
        if product["id"] == product_id:

            # pop() elimina el producto de la lista
            # y al mismo tiempo devuelve el producto eliminado.
            deleted_product = products.pop(index)

            # Guarda la lista actualizada en el archivo JSON.
            write_products(products)

            # Registra que la eliminación fue exitosa.
            logger.info(
                f"SUCCESS DELETE_PRODUCT - "
                f"Producto ID {product_id} eliminado correctamente"
            )

            # Devuelve el producto que fue eliminado.
            return deleted_product

    # Si no se encontró el producto, registra el error.
    logger.error(
        f"ERROR DELETE_PRODUCT - "
        f"Producto ID {product_id} no encontrado"
    )

    # Genera un error HTTP 404 indicando
    # que el producto solicitado no existe.
    raise HTTPException(
        status_code=404,
        detail="El producto no existe"
    )