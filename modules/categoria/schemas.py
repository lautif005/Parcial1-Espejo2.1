from pydantic import BaseModel, Field
from typing import Optional

class CategoriaBase(BaseModel):
    nombre: str = Field(..., max_length=100, description="Nombre de la categoría")
    descripcion: Optional[str] = Field(default=None, description="Descripción extendida")
    imagen_url: Optional[str] = Field(default=None, description="URL de la imagen")
    parent_id: Optional[int] = Field(default=None, description="ID de la categoría padre (si aplica)")

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, max_length=100)
    descripcion: Optional[str] = Field(default=None)
    imagen_url: Optional[str] = Field(default=None)
    parent_id: Optional[int] = Field(default=None)

class CategoriaOut(CategoriaBase):
    id: int

    class Config:
        from_attributes = True
