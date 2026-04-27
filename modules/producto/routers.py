
from fastapi import APIRouter, status, Path, Query
from typing import List, Annotated, Optional
from .schemas import ProductoCreate, ProductoUpdate, ProductoOut, ProductoReadWithRelations
from .services import ProductoService

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post("/", response_model=ProductoOut, status_code=status.HTTP_201_CREATED)
def create_producto(producto: ProductoCreate):
    return ProductoService.create_producto(producto)

@router.get("/", response_model=List[ProductoReadWithRelations], status_code=status.HTTP_200_OK)
def get_productos(
    skip: Annotated[int, Query(ge=0, description="Registros a omitir (paginación)")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Límite de registros a traer (paginación, max 100)")] = 100,
    disponible: Annotated[Optional[bool], Query(description="Filtrar por productos según si están explícitamente disponibles en carta")] = None
):
    return ProductoService.get_productos(skip=skip, limit=limit, disponible=disponible)

@router.get("/{producto_id}", response_model=ProductoReadWithRelations, status_code=status.HTTP_200_OK)
def get_producto(
    producto_id: Annotated[int, Path(gt=0, description="ID numérico único del producto")]
):
    return ProductoService.get_producto(producto_id)

@router.patch("/{producto_id}", response_model=ProductoOut, status_code=status.HTTP_200_OK)
def update_producto(
    producto: ProductoUpdate,
    producto_id: Annotated[int, Path(gt=0, description="ID del producto a modificar")]
):
    return ProductoService.update_producto(producto_id, producto)

@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producto(
    producto_id: Annotated[int, Path(gt=0, description="ID del producto que será eliminado (soft)")]
):
    ProductoService.delete_producto(producto_id)
    return None

@router.post("/{producto_id}/categorias/{categoria_id}", status_code=status.HTTP_201_CREATED)
def link_categoria(
    producto_id: Annotated[int, Path(gt=0, description="ID del producto")],
    categoria_id: Annotated[int, Path(gt=0, description="ID de la categoría a vincular")]
):
    return ProductoService.link_categoria(producto_id, categoria_id)

@router.post("/{producto_id}/ingredientes/{ingrediente_id}", status_code=status.HTTP_201_CREATED)
def link_ingrediente(
    producto_id: Annotated[int, Path(gt=0, description="ID del producto")],
    ingrediente_id: Annotated[int, Path(gt=0, description="ID del ingrediente a vincular")]
):
    return ProductoService.link_ingrediente(producto_id, ingrediente_id)
