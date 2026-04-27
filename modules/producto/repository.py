
from typing import List, Optional, Any
from sqlmodel import select
from datetime import datetime

from core.repository import BaseRepository
from .models import Producto
from .schemas import ProductoCreate, ProductoUpdate


class ProductoRepository(BaseRepository[Producto, ProductoCreate, ProductoUpdate]):
    


    def get_all(self, skip: int = 0, limit: int = 100, disponible: Optional[bool] = None) -> List[Producto]:
        query = select(Producto).where(Producto.deleted_at == None)
        
        if disponible is not None:
            query = query.where(Producto.disponible == disponible)
        
        query = query.offset(skip).limit(limit)
        return self.session.exec(query).all()

    def update(self, db_obj: Producto) -> Producto:
        db_obj.updated_at = datetime.utcnow()
        return super().update(db_obj)
