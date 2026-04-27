
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from sqlalchemy import Column, BigInteger, Text, DECIMAL, Boolean, JSON, CheckConstraint, ForeignKey, Integer


class ProductoCategoria(SQLModel, table=True):
    
    __tablename__ = "producto_categoria"
    
    
    producto_id: int = Field(
        default=None,
        sa_column=Column(BigInteger(), ForeignKey("producto.id"), primary_key=True)
    )
    
    categoria_id: int = Field(
        default=None,
        sa_column=Column(BigInteger(), ForeignKey("categoria.id"), primary_key=True)
    )
    
    es_principal: bool = Field(
        default=False,
        sa_column=Column(Boolean(), nullable=False, default=False)
    )
    
    created_at: datetime = Field(default_factory=datetime.utcnow)



class ProductoIngrediente(SQLModel, table=True):
    
    __tablename__ = "producto_ingrediente"
    
    
    producto_id: int = Field(
        default=None,
        sa_column=Column(BigInteger(), ForeignKey("producto.id"), primary_key=True)
    )
    
    ingrediente_id: int = Field(
        default=None,
        sa_column=Column(BigInteger(), ForeignKey("ingrediente.id"), primary_key=True)
    )
    
    es_removible: bool = Field(
        default=False,
        sa_column=Column(Boolean(), nullable=False, default=False)
    )



class Producto(SQLModel, table=True):
    
    __tablename__ = "producto"
    
    __table_args__ = (
        CheckConstraint('precio_base >= 0', name='check_precio_base_positive'),
    )
    
    id: Optional[int] = Field(
        default=None,
        sa_column=Column(BigInteger(), primary_key=True, autoincrement=True)
    )
    
    nombre: str = Field(
        max_length=150,
        nullable=False
    )
    
    descripcion: Optional[str] = Field(
        default=None,
        sa_column=Column(Text(), nullable=True)
    )
    
    precio_base: float = Field(
        default=0.0,
        sa_column=Column(DECIMAL(10, 2), nullable=False),
    )
    
    imagenes_url: Optional[List[str]] = Field(
        default=None,
        sa_column=Column(JSON, nullable=True)
    )
    
    stock_cantidad: int = Field(
        default=0,
        sa_column=Column(Integer(), nullable=False, default=0)
    )
    
    disponible: bool = Field(
        default=True,
        sa_column=Column(Boolean(), nullable=False, default=True)
    )
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = Field(default=None)
    
    
    categorias: List["Categoria"] = Relationship(
        link_model=ProductoCategoria,
        back_populates="productos"
    )
    
    ingredientes: List["Ingrediente"] = Relationship(
        link_model=ProductoIngrediente,
        back_populates="productos"
    )
