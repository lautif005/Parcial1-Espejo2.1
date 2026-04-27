
from typing import List, Optional, Any
from sqlmodel import select
from datetime import datetime

from core.repository import BaseRepository
from .models import Ingrediente
from .schemas import IngredienteCreate, IngredienteUpdate


class IngredienteRepository(BaseRepository[Ingrediente, IngredienteCreate, IngredienteUpdate]):
    
    def update(self, db_obj: Ingrediente, obj_in: IngredienteUpdate) -> Ingrediente:
        db_obj.updated_at = datetime.utcnow()
        return super().update(db_obj, obj_in)
