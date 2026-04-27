
from typing import Generic, TypeVar, Type, List, Optional, Any
from sqlmodel import Session, select
from pydantic import BaseModel
from datetime import datetime


ModelType = TypeVar("ModelType")

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)

UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)




class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    
    def __init__(self, model: Type[ModelType], session: Session):
        self.model = model
        self.session = session

    def create(self, db_obj: ModelType) -> ModelType:
        self.session.add(db_obj)
        self.session.flush()
        self.session.refresh(db_obj)
        return db_obj

    def get_by_id(self, id: Any) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id)
        if hasattr(self.model, "deleted_at"):
            query = query.where(self.model.deleted_at == None)
        return self.session.exec(query).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        query = select(self.model)
        if hasattr(self.model, "deleted_at"):
            query = query.where(self.model.deleted_at == None)
        return self.session.exec(query.offset(skip).limit(limit)).all()

    def update(self, db_obj: ModelType) -> ModelType:
        self.session.add(db_obj)
        self.session.flush()
        self.session.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: ModelType) -> None:
        if hasattr(db_obj, "deleted_at"):
            db_obj.deleted_at = datetime.utcnow()
            self.session.add(db_obj)
            self.session.flush()
        else:
            self.session.delete(db_obj)
            self.session.flush()
