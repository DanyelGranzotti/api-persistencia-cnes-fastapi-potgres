from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db

from schemas.profissional import Profissional
from repositories.profissional import ProfissionalRepository


router = APIRouter(
    prefix="/profissionais",
    tags=["profissionais"]
)

@router.get("/", response_model=List[Profissional])
async def listar_enderecos(
    db: AsyncSession = Depends(get_db)
) -> List[Profissional]:
    repository = ProfissionalRepository(db)
    return await repository.get_all()

@router.post("/", response_model=Profissional, status_code=201)
async def criar_endereco(
    data: Profissional,
    db: AsyncSession = Depends(get_db)
) -> Profissional:
    repository = ProfissionalRepository(db)
    return await repository.create(data)

@router.get("/{id}", response_model=Profissional)
async def obter_endereco(
    id: int,
    db: AsyncSession = Depends(get_db)
) -> Profissional:
    repository = ProfissionalRepository(db)
    endereco = await repository.get_by_id(id)
    if not endereco:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return endereco

@router.put("/{id}", response_model=Profissional)
async def atualizar_endereco(
    id: int,
    data: Profissional,
    db: AsyncSession = Depends(get_db)
) -> Profissional:
    repository = ProfissionalRepository(db)
    endereco = await repository.get_by_id(id)
    if not endereco:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return await repository.update(id, data)

@router.delete("/{id}", status_code=204)
async def deletar_endereco(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    repository = ProfissionalRepository(db)
    endereco = await repository.get_by_id(id)
    if not endereco:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    await repository
    return

@router.get("/filtro", response_model=List[Profissional])
async def filtrar_profissionais(
    codigo_profissional_sus: str = Query(None),
    nome_profissional: str = Query(None),
    codigo_cns: str = Query(None),
    db: AsyncSession = Depends(get_db)
):
    repository = ProfissionalRepository(db)
    filters = {}
    if codigo_profissional_sus:
        filters["codigo_profissional_sus"] = codigo_profissional_sus
    if nome_profissional:
        filters["nome_profissional"] = nome_profissional
    if codigo_cns:
        filters["codigo_cns"] = codigo_cns
    return await repository.get_all(filters)

@router.get("/paginated", response_model=List[Profissional])
async def listar_profissionais_paginados(
    page: int = Query(1),
    limit: int = Query(10),
    db: AsyncSession = Depends(get_db)
):
    repository = ProfissionalRepository(db)
    total = await repository.count()
    profissionais = await repository.get_paginated(limit=limit, offset=page * limit)
    current_page = (page // limit) + 1
    total_pages = (page // limit) + 1
    return {
        "data": profissionais,
        "pagination": {
            "total_pages": total_pages,
            "current_page": current_page,
            "total": total,
            "offset": page,
            "limit": limit
        }
    }