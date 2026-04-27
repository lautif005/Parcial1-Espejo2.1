
from typing import List, Optional
from fastapi import HTTPException, status
from sqlmodel import select
from .uow import ProductoUnitOfWork
from .schemas import ProductoCreate, ProductoUpdate
from .models import Producto, ProductoCategoria, ProductoIngrediente
from modules.categoria.models import Categoria
from modules.ingrediente.models import Ingrediente


class ProductoService:
    
    @staticmethod
    def create_producto(data: ProductoCreate) -> Producto:
        with ProductoUnitOfWork() as uow:
            producto_model = Producto.model_validate(data)
            producto = uow.producto_repo.create(producto_model)
            return producto

    @staticmethod
    def get_productos(skip: int = 0, limit: int = 100, disponible: Optional[bool] = None) -> List[Producto]:
        with ProductoUnitOfWork() as uow:
            productos = uow.producto_repo.get_all(skip=skip, limit=limit, disponible=disponible)
            
            for p in productos:
                _ = p.categorias
                _ = p.ingredientes
            return productos

    @staticmethod
    def get_producto(producto_id: int) -> Producto:
        with ProductoUnitOfWork() as uow:
            producto = uow.producto_repo.get_by_id(producto_id)
            if not producto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Producto con ID {producto_id} no encontrado."
                )
            
            _ = producto.categorias
            _ = producto.ingredientes
            return producto

    @staticmethod
    def update_producto(producto_id: int, data: ProductoUpdate) -> Producto:
        with ProductoUnitOfWork() as uow:
            producto = uow.producto_repo.get_by_id(producto_id)
            if not producto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Producto con ID {producto_id} no encontrado."
                )
            
            obj_data = data.model_dump(exclude_unset=True)
            for key, value in obj_data.items():
                setattr(producto, key, value)
                
            updated_producto = uow.producto_repo.update(producto)
            return updated_producto

    @staticmethod
    def delete_producto(producto_id: int) -> None:
        with ProductoUnitOfWork() as uow:
            producto = uow.producto_repo.get_by_id(producto_id)
            if not producto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Producto con ID {producto_id} no encontrado."
                )
            uow.producto_repo.delete(producto)


    @staticmethod
    def link_categoria(producto_id: int, categoria_id: int) -> dict:
        with ProductoUnitOfWork() as uow:
            producto = uow.producto_repo.get_by_id(producto_id)
            if not producto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Producto con ID {producto_id} no encontrado."
                )
            
            categoria = uow.session.get(Categoria, categoria_id)
            if not categoria:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Categoría con ID {categoria_id} no encontrada."
                )
            
            link = uow.session.get(ProductoCategoria, {"producto_id": producto_id, "categoria_id": categoria_id})
            if link:
                return {"message": "El producto ya estaba vinculado a esta categoría."}
            
            new_link = ProductoCategoria(
                producto_id=producto_id,
                categoria_id=categoria_id,
                es_principal=False
            )
            uow.session.add(new_link)
            return {"message": "Registro en ProductoCategoria creado exitosamente."}

    @staticmethod
    def link_ingrediente(producto_id: int, ingrediente_id: int) -> dict:
        with ProductoUnitOfWork() as uow:
            producto = uow.producto_repo.get_by_id(producto_id)
            if not producto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Producto con ID {producto_id} no encontrado."
                )
            
            ingrediente = uow.session.get(Ingrediente, ingrediente_id)
            if not ingrediente:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ingrediente con ID {ingrediente_id} no encontrado."
                )
            
            link = uow.session.get(ProductoIngrediente, {"producto_id": producto_id, "ingrediente_id": ingrediente_id})
            if link:
                return {"message": "El producto ya contaba con este ingrediente."}
            
            new_link = ProductoIngrediente(
                producto_id=producto_id,
                ingrediente_id=ingrediente_id,
                es_removible=False
            )
            uow.session.add(new_link)
            return {"message": "Registro en ProductoIngrediente creado exitosamente."}
