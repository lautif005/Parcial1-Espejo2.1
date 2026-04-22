from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, BigInteger, Boolean, Text

class Ingrediente(SQLModel, table=True):
    __tablename__ = "ingrediente"
    
    id: Optional[int] = Field(default=None, sa_column=Column(BigInteger(), primary_key=True, autoincrement=True))
    nombre: str = Field(max_length=100, unique=True, nullable=False)
    descripcion: Optional[str] = Field(default=None, sa_column=Column(Text(), nullable=True))
    es_alergeno: bool = Field(default=False, sa_column=Column(Boolean(), nullable=False, default=False))
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
