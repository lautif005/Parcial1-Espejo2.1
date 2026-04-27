
from typing import List, Optional, Any
from sqlmodel import Session, select
from datetime import datetime

from core.repository import BaseRepository
from .models import Categoria
from .schemas import CategoriaCreate, CategoriaUpdate


class CategoriaRepository(BaseRepository[Categoria, CategoriaCreate, CategoriaUpdate]):
    
    def get_by_id(self, id: Any) -> Optional[Categoria]:
        statement = select(Categoria).where(
            Categoria.id == id,
            Categoria.deleted_at == None
        )
        return self.session.exec(statement).first()
        

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Categoria]:
        statement = select(Categoria).where(
            Categoria.deleted_at == None
        ).offset(skip).limit(limit)
        
        return self.session.exec(statement).all()
        

    def update(self, db_obj: Categoria, obj_in: CategoriaUpdate) -> Categoria:
        db_obj.updated_at = datetime.utcnow()
        
        return super().update(db_obj, obj_in)
        

    def delete(self, db_obj: Categoria) -> None:
        db_obj.deleted_at = datetime.utcnow()
        
        self.session.add(db_obj)
        
        self.session.flush()
        
        
