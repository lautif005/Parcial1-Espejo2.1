
from typing import List
from fastapi import HTTPException, status
from .uow import IngredienteUnitOfWork
from .schemas import IngredienteCreate, IngredienteUpdate
from .models import Ingrediente


class IngredienteService:
    
    @staticmethod
    def create_ingrediente(data: IngredienteCreate) -> Ingrediente:
        with IngredienteUnitOfWork() as uow:
            ingrediente_model = Ingrediente.model_validate(data)
            ingrediente = uow.ingrediente_repo.create(ingrediente_model)
            return ingrediente

    @staticmethod
    def get_ingredientes(skip: int = 0, limit: int = 100) -> List[Ingrediente]:
        with IngredienteUnitOfWork() as uow:
            return uow.ingrediente_repo.get_all(skip=skip, limit=limit)

    @staticmethod
    def get_ingrediente(ingrediente_id: int) -> Ingrediente:
        with IngredienteUnitOfWork() as uow:
            ingrediente = uow.ingrediente_repo.get_by_id(ingrediente_id)
            if not ingrediente:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ingrediente con ID {ingrediente_id} no encontrado."
                )
            return ingrediente

    @staticmethod
    def update_ingrediente(ingrediente_id: int, data: IngredienteUpdate) -> Ingrediente:
        with IngredienteUnitOfWork() as uow:
            ingrediente = uow.ingrediente_repo.get_by_id(ingrediente_id)
            if not ingrediente:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ingrediente con ID {ingrediente_id} no encontrado."
                )
            
            obj_data = data.model_dump(exclude_unset=True)
            for key, value in obj_data.items():
                setattr(ingrediente, key, value)
                
            updated_ingrediente = uow.ingrediente_repo.update(ingrediente)
            return updated_ingrediente

    @staticmethod
    def delete_ingrediente(ingrediente_id: int) -> None:
        with IngredienteUnitOfWork() as uow:
            ingrediente = uow.ingrediente_repo.get_by_id(ingrediente_id)
            if not ingrediente:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ingrediente con ID {ingrediente_id} no encontrado."
                )
            uow.ingrediente_repo.delete(ingrediente)
