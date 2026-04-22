from core.uow import BaseUnitOfWork
from .repository import CategoriaRepository
from .models import Categoria

class CategoriaUnitOfWork(BaseUnitOfWork):
    def __enter__(self):
        super().__enter__()
        self.categoria_repo = CategoriaRepository(Categoria, self.session)
        return self
