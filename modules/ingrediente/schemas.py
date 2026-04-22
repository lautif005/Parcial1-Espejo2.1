from pydantic import BaseModel, Field
from typing import Optional

class IngredienteBase(BaseModel):
    nombre: str = Field(..., max_length=100, description="Nombre descriptivo del ingrediente")
    descripcion: Optional[str] = Field(default=None, description="Descripción del ingrediente")
    es_alergeno: bool = Field(default=False, description="Bandera true/false si denota ser alérgeno")

class IngredienteCreate(IngredienteBase):
    pass

class IngredienteUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, max_length=100)
    descripcion: Optional[str] = Field(default=None)
    es_alergeno: Optional[bool] = Field(default=None)

class IngredienteOut(IngredienteBase):
    id: int

    class Config:
        from_attributes = True
