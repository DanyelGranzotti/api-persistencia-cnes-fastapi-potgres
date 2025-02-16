from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.database import get_db, init_models, engine, Base
from routers import estabelecimento, endereco, mantenedora

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthcheck")
async def healthcheck(db=Depends(get_db)):
    return {"status": "healthy", "database": "connected"}

# Include routers
app.include_router(estabelecimento.router)
app.include_router(endereco.router)
app.include_router(mantenedora.router)
