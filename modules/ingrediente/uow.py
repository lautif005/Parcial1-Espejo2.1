
from core.uow import BaseUnitOfWork
from .repository import IngredienteRepository
from .models import Ingrediente


class IngredienteUnitOfWork(BaseUnitOfWork):
    
    def __enter__(self):
        super().__enter__()
        self.ingrediente_repo = IngredienteRepository(Ingrediente, self.session)
        return self
