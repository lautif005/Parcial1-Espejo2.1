from fastapi import APIRouter, status, Path, Query
from typing import List, Annotated
from .schemas import CategoriaCreate, CategoriaUpdate, CategoriaOut
from .services import CategoriaService

router = APIRouter(prefix="/categorias", tags=["Categorías"])

@router.post("/", response_model=CategoriaOut, status_code=status.HTTP_201_CREATED)
def create_categoria(categoria: CategoriaCreate):
    return CategoriaService.create_categoria(categoria)

@router.get("/", response_model=List[CategoriaOut], status_code=status.HTTP_200_OK)
def get_categorias(
    skip: Annotated[int, Query(ge=0, description="Número de registros a omitir")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Límite de registros a retornar")] = 100
):
    return CategoriaService.get_categorias(skip=skip, limit=limit)

@router.get("/{categoria_id}", response_model=CategoriaOut, status_code=status.HTTP_200_OK)
def get_categoria(
    categoria_id: Annotated[int, Path(gt=0, description="ID de la categoría a obtener")]
):
    return CategoriaService.get_categoria(categoria_id)

@router.patch("/{categoria_id}", response_model=CategoriaOut, status_code=status.HTTP_200_OK)
def update_categoria(
    categoria: CategoriaUpdate,
    categoria_id: Annotated[int, Path(gt=0, description="ID de la categoría a actualizar")]
):
    return CategoriaService.update_categoria(categoria_id, categoria)

@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_categoria(
    categoria_id: Annotated[int, Path(gt=0, description="ID de la categoría a eliminar")]
):
    CategoriaService.delete_categoria(categoria_id)
    return None
