from typing import List, Optional, Any
from sqlmodel import select
from datetime import datetime

from core.repository import BaseRepository
from .models import Producto
from .schemas import ProductoCreate, ProductoUpdate

class ProductoRepository(BaseRepository[Producto, ProductoCreate, ProductoUpdate]):
    
    def get_by_id(self, id: Any) -> Optional[Producto]:
        statement = select(Producto).where(Producto.id == id, Producto.deleted_at == None)
        return self.session.exec(statement).first()

    def get_all(self, skip: int = 0, limit: int = 100, disponible: Optional[bool] = None) -> List[Producto]:
        query = select(Producto).where(Producto.deleted_at == None)
        
        if disponible is not None:
            query = query.where(Producto.disponible == disponible)
            
        query = query.offset(skip).limit(limit)
        return self.session.exec(query).all()

    def update(self, db_obj: Producto, obj_in: ProductoUpdate) -> Producto:
        db_obj.updated_at = datetime.utcnow()
        return super().update(db_obj, obj_in)

    def delete(self, db_obj: Producto) -> None:
        db_obj.deleted_at = datetime.utcnow()
        self.session.add(db_obj)
        self.session.flush()
