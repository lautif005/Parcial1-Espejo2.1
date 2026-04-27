
from fastapi import APIRouter, status, Path, Query
from typing import List, Annotated
from .schemas import IngredienteCreate, IngredienteUpdate, IngredienteOut
from .services import IngredienteService

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])

@router.post("/", response_model=IngredienteOut, status_code=status.HTTP_201_CREATED)
def create_ingrediente(ingrediente: IngredienteCreate):
    return IngredienteService.create_ingrediente(ingrediente)

@router.get("/", response_model=List[IngredienteOut], status_code=status.HTTP_200_OK)
def get_ingredientes(
    skip: Annotated[int, Query(ge=0, description="Número de registros a omitir")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Límite de registros a retornar")] = 100
):
    return IngredienteService.get_ingredientes(skip=skip, limit=limit)

@router.get("/{ingrediente_id}", response_model=IngredienteOut, status_code=status.HTTP_200_OK)
def get_ingrediente(
    ingrediente_id: Annotated[int, Path(gt=0, description="ID del ingrediente a obtener")]
):
    return IngredienteService.get_ingrediente(ingrediente_id)

@router.patch("/{ingrediente_id}", response_model=IngredienteOut, status_code=status.HTTP_200_OK)
def update_ingrediente(
    ingrediente: IngredienteUpdate,
    ingrediente_id: Annotated[int, Path(gt=0, description="ID del ingrediente a actualizar")]
):
    return IngredienteService.update_ingrediente(ingrediente_id, ingrediente)

@router.delete("/{ingrediente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingrediente(
    ingrediente_id: Annotated[int, Path(gt=0, description="ID del ingrediente a eliminar")]
):
    IngredienteService.delete_ingrediente(ingrediente_id)
    return None
