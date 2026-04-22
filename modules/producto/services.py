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
            producto = uow.producto_repo.create(data)
            uow.session.commit()
            uow.session.refresh(producto)
            return producto

    @staticmethod
    def get_productos(skip: int = 0, limit: int = 100, disponible: Optional[bool] = None) -> List[Producto]:
        with ProductoUnitOfWork() as uow:
            productos = uow.producto_repo.get_all(skip=skip, limit=limit, disponible=disponible)
            # Forzar la carga perezosa de las relaciones antes de cerrar la UoW
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
            
            # Forzar la carga perezosa de las relaciones antes de cerrar la UoW
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
            
            updated_producto = uow.producto_repo.update(producto, data)
            uow.session.commit()
            uow.session.refresh(updated_producto)
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
            uow.session.commit()

    @staticmethod
    def link_categoria(producto_id: int, categoria_id: int) -> dict:
        with ProductoUnitOfWork() as uow:
            producto = uow.producto_repo.get_by_id(producto_id)
            if not producto:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Producto con ID {producto_id} no encontrado.")
            
            categoria = uow.session.get(Categoria, categoria_id)
            if not categoria:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Categoría con ID {categoria_id} no encontrada.")
            
            link = uow.session.get(ProductoCategoria, {"producto_id": producto_id, "categoria_id": categoria_id})
            if link:
                return {"message": "El producto ya estaba vinculado a esta categoría."}
            
            new_link = ProductoCategoria(producto_id=producto_id, categoria_id=categoria_id, es_principal=False)
            uow.session.add(new_link)
            uow.session.commit()
            return {"message": "Registro en ProductoCategoria creado exitosamente."}

    @staticmethod
    def link_ingrediente(producto_id: int, ingrediente_id: int) -> dict:
        with ProductoUnitOfWork() as uow:
            producto = uow.producto_repo.get_by_id(producto_id)
            if not producto:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Producto con ID {producto_id} no encontrado.")
            
            ingrediente = uow.session.get(Ingrediente, ingrediente_id)
            if not ingrediente:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ingrediente con ID {ingrediente_id} no encontrado.")
            
            link = uow.session.get(ProductoIngrediente, {"producto_id": producto_id, "ingrediente_id": ingrediente_id})
            if link:
                return {"message": "El producto ya contaba con este ingrediente."}
            
            new_link = ProductoIngrediente(producto_id=producto_id, ingrediente_id=ingrediente_id, es_removible=False)
            uow.session.add(new_link)
            uow.session.commit()
            return {"message": "Registro en ProductoIngrediente creado exitosamente."}
