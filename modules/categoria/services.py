from typing import List
from fastapi import HTTPException, status
from .uow import CategoriaUnitOfWork
from .schemas import CategoriaCreate, CategoriaUpdate
from .models import Categoria

class CategoriaService:
    
    @staticmethod
    def create_categoria(data: CategoriaCreate) -> Categoria:
        with CategoriaUnitOfWork() as uow:
            if data.parent_id is not None:
                parent = uow.categoria_repo.get_by_id(data.parent_id)
                if not parent:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Categoría padre con ID {data.parent_id} no encontrada."
                    )
            
            categoria = uow.categoria_repo.create(data)
            uow.session.commit()
            uow.session.refresh(categoria)
            return categoria

    @staticmethod
    def get_categorias(skip: int = 0, limit: int = 100) -> List[Categoria]:
        with CategoriaUnitOfWork() as uow:
            return uow.categoria_repo.get_all(skip=skip, limit=limit)

    @staticmethod
    def get_categoria(categoria_id: int) -> Categoria:
        with CategoriaUnitOfWork() as uow:
            categoria = uow.categoria_repo.get_by_id(categoria_id)
            if not categoria:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Categoría con ID {categoria_id} no encontrada."
                )
            return categoria

    @staticmethod
    def update_categoria(categoria_id: int, data: CategoriaUpdate) -> Categoria:
        with CategoriaUnitOfWork() as uow:
            categoria = uow.categoria_repo.get_by_id(categoria_id)
            if not categoria:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Categoría con ID {categoria_id} no encontrada."
                )
            
            if data.parent_id is not None and data.parent_id != categoria.parent_id:
                parent = uow.categoria_repo.get_by_id(data.parent_id)
                if not parent:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Categoría padre con ID {data.parent_id} no encontrada."
                    )
                if data.parent_id == categoria.id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Una categoría no puede ser padre de sí misma."
                    )

            updated_categoria = uow.categoria_repo.update(categoria, data)
            uow.session.commit()
            uow.session.refresh(updated_categoria)
            return updated_categoria

    @staticmethod
    def delete_categoria(categoria_id: int) -> None:
        with CategoriaUnitOfWork() as uow:
            categoria = uow.categoria_repo.get_by_id(categoria_id)
            if not categoria:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Categoría con ID {categoria_id} no encontrada."
                )
            uow.categoria_repo.delete(categoria)
            uow.session.commit()
