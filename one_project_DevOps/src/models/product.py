from pydantic import BaseModel, Field


# Modelo base que contiene los atributos comunes de un producto.
# Hereda de BaseModel de Pydantic para permitir la validación
# automática de los datos.
class ProductBase(BaseModel):

    # Nombre del producto.
    # "..." indica que el campo es obligatorio.
    # min_length=1 evita que se envíe un nombre vacío.
    nombre: str = Field(
        ...,
        min_length=1,
        description="Nombre del producto"
    )

    # Categoría a la que pertenece el producto.
    # El campo es obligatorio y debe contener al menos un carácter.
    categoria: str = Field(
        ...,
        min_length=1,
        description="Categoría del producto"
    )

    # Precio del producto.
    # Debe ser un número decimal (float).
    # gt=0 significa que el precio debe ser estrictamente mayor que 0.
    precio: float = Field(
        ...,
        gt=0,
        description="Precio del producto. Debe ser mayor que 0"
    )

    # Cantidad de productos disponibles.
    # Debe ser un número entero (int).
    # ge=0 permite el valor 0, pero no valores negativos.
    stock: int = Field(
        ...,
        ge=0,
        description="Cantidad disponible. No puede ser negativa"
    )


# Modelo utilizado para crear un nuevo producto.
# Hereda todos los atributos y validaciones de ProductBase.
#
# "pass" indica que no se agregan atributos adicionales.
class ProductCreate(ProductBase):
    pass


# Modelo utilizado para representar un producto como respuesta.
# Hereda los atributos y validaciones de ProductBase.
class ProductResponse(ProductBase):

    # Identificador único del producto.
    # Es un número entero y permite identificar cada producto.
    id: int