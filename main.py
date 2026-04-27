
from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel

from core.database import engine

from modules.categoria.routers import router as categoria_router
from modules.ingrediente.routers import router as ingrediente_router
from modules.producto.routers import router as producto_router

from modules.categoria.models import Categoria
from modules.ingrediente.models import Ingrediente
from modules.producto.models import Producto, ProductoCategoria, ProductoIngrediente


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    SQLModel.metadata.create_all(engine)
    
    yield
    
    engine.dispose()



app = FastAPI(
    title="Backend Food Store - Sistema de Catálogo y Productos",
    description="Resolución de la evaluación orientada a Arquitectura de Software Limpia utilizando SQLModel estricto y Unit Of Work.",
    version="1.0.0",
    
    lifespan=lifespan
)



app.include_router(categoria_router)
app.include_router(ingrediente_router)
app.include_router(producto_router)



@app.get("/", tags=["Health"])
def health_check():
    return {"message": "El Backend de Food Store está en ejecución correctamente. Visualiza el abanico de endpoints visitando /docs."}
