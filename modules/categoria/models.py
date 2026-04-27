
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from sqlalchemy import Column, BigInteger, Text, ForeignKey


class Categoria(SQLModel, table=True):
    
    __tablename__ = "categoria"
    
    id: Optional[int] = Field(
        default=None,
        sa_column=Column(BigInteger(), primary_key=True, autoincrement=True),
    )
    
    parent_id: Optional[int] = Field(
        default=None,
        sa_column=Column(BigInteger(), ForeignKey("categoria.id"), nullable=True),
    )
    
    nombre: str = Field(
        max_length=100,
        unique=True,
        nullable=False,
    )
    
    descripcion: Optional[str] = Field(
        default=None,
        sa_column=Column(Text(), nullable=True),
    )
    
    imagen_url: Optional[str] = Field(
        default=None,
        sa_column=Column(Text(), nullable=True),
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )
    
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
    )
    
    deleted_at: Optional[datetime] = Field(
        default=None,
    )
    
    
    parent: Optional["Categoria"] = Relationship(
        back_populates="subcategorias",
        sa_relationship_kwargs=dict(remote_side="Categoria.id"),
    )
    
    subcategorias: List["Categoria"] = Relationship(
        back_populates="parent",
    )
    
    productos: List["Producto"] = Relationship(
        back_populates="categorias"
    )
    
