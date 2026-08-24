from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    nombre: str = Field(
        ...,
        min_length=1,
        description="Nombre del producto"
    )

    categoria: str = Field(
        ...,
        min_length=1,
        description="Categoría del producto"
    )

    precio: float = Field(
        ...,
        gt=0,
        description="Precio del producto. Debe ser mayor que 0"
    )

    stock: int = Field(
        ...,
        ge=0,
        description="Cantidad disponible. No puede ser negativa"
    )


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int