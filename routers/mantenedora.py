from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.database import get_db
from repositories.mantenedora import MantenedoraRepository
from schemas.mantenedora import Mantenedora, MantenedoraCreate, MantenedoraUpdate

router = APIRouter(
    prefix="/mantenedoras",
    tags=["mantenedoras"]
)

@router.get("/", response_model=List[Mantenedora])
async def listar_mantenedoras(
    db: AsyncSession = Depends(get_db)
) -> List[Mantenedora]:
    repository = MantenedoraRepository(db)
    return await repository.get_all()

@router.post("/", response_model=Mantenedora, status_code=201)
async def criar_mantenedora(
    data: MantenedoraCreate,
    db: AsyncSession = Depends(get_db)
) -> Mantenedora:
    repository = MantenedoraRepository(db)
    return await repository.create(data.model_dump())

@router.get("/{id}", response_model=Mantenedora)
async def obter_mantenedora(
    id: int,
    db: AsyncSession = Depends(get_db)
) -> Mantenedora:
    repository = MantenedoraRepository(db)
    mantenedora = await repository.get_by_id(id)
    if not mantenedora:
        raise HTTPException(status_code=404, detail="Mantenedora não encontrada")
    return mantenedora

@router.put("/{id}", response_model=Mantenedora)
async def atualizar_mantenedora(
    id: int,
    data: MantenedoraUpdate,
    db: AsyncSession = Depends(get_db)
) -> Mantenedora:
    repository = MantenedoraRepository(db)
    mantenedora = await repository.get_by_id(id)
    if not mantenedora:
        raise HTTPException(status_code=404, detail="Mantenedora não encontrada")
    return await repository.update(id, data.model_dump())

@router.delete("/{id}", status_code=204)
async def deletar_mantenedora(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    repository = MantenedoraRepository(db)
    mantenedora = await repository.get_by_id(id)
    if not mantenedora:
        raise HTTPException(status_code=404, detail="Mantenedora não encontrada")
    await repository.delete(id)
    return

@router.get("/filtro", response_model=List[Mantenedora])
async def filtrar_mantenedoras(
    cnpj_mantenedora: str = Query(None),
    nome_razao_social_mantenedora: str = Query(None),
    db: AsyncSession = Depends(get_db)
):
    repository = MantenedoraRepository(db)
    filters = {}
    if cnpj_mantenedora:
        filters["cnpj_mantenedora"] = cnpj_mantenedora
    if nome_razao_social_mantenedora:
        filters["nome_razao_social_mantenedora"] = nome_razao_social_mantenedora
    return await repository.get_all(filters)