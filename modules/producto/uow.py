from core.uow import BaseUnitOfWork
from .repository import ProductoRepository
from .models import Producto


class ProductoUnitOfWork(BaseUnitOfWork):
    
    def __enter__(self):
        super().__enter__()
        self.producto_repo = ProductoRepository(Producto, self.session)
        return self
