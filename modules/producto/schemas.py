
from pydantic import BaseModel, Field
from typing import Optional, List

from modules.categoria.schemas import CategoriaOut
from modules.ingrediente.schemas import IngredienteOut


class ProductoBase(BaseModel):
    nombre: str = Field(..., max_length=150)
    descripcion: Optional[str] = None
    precio_base: float = Field(..., ge=0, description="El precio mínimo en la carta debe ser mayor o igual a cero")
    imagenes_url: Optional[List[str]] = Field(default=None, description="Arreglo con de las imágenes del producto")
    stock_cantidad: int = Field(default=0, description="Cantidad de stock disponible")
    disponible: bool = Field(default=True, description="Estado en el servicio (en carta)")


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, max_length=150)
    descripcion: Optional[str] = None
    precio_base: Optional[float] = Field(default=None, ge=0)
    imagenes_url: Optional[List[str]] = None
    stock_cantidad: Optional[int] = None
    disponible: Optional[bool] = None


class ProductoOut(ProductoBase):
    id: int

    class Config:
        from_attributes = True


class ProductoReadWithRelations(ProductoOut):
    categorias: List[CategoriaOut] = []
    ingredientes: List[IngredienteOut] = []

    class Config:
        from_attributes = True
