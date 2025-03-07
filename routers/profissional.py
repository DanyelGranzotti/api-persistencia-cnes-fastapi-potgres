from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
import logging
from schemas.profissional import Profissional
from repositories.profissional import ProfissionalRepository


router = APIRouter(
    prefix="/profissionais",
    tags=["profissionais"]
)

@router.get("/", response_model=List[Profissional])
async def listar_profissionals(
    db: AsyncSession = Depends(get_db)
) -> List[Profissional]:
    repository = ProfissionalRepository(db)
    logging.info("Listando todos os profissionais")
    return await repository.get_all()

@router.get("/filtro")
async def filtrar_profissionais(
    codigo_profissional_sus: str = Query(None),
    nome_profissional: str = Query(None),
    codigo_cns: str = Query(None),
    db: AsyncSession = Depends(get_db)
) -> dict:
    repository = ProfissionalRepository(db)
    filters = {}
    if codigo_profissional_sus:
        filters["codigo_profissional_sus"] = codigo_profissional_sus
    if nome_profissional:
        filters["nome_profissional"] = nome_profissional
    if codigo_cns:
        filters["codigo_cns"] = codigo_cns
    res = await repository.get_by_filters(filters)
    return {"res":[[str(key)+": "+str(value) for key, value in profissional.__dict__.items() if (not key.startswith("_"))] for profissional in res]}

@router.get("/paginated", response_model=dict)
async def listar_profissionais_paginados(
    page: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db)
) -> dict:
    repository = ProfissionalRepository(db)
    total = await repository.get_total_count()
    profissionais = await repository.get_paginated(limit=limit, offset=page * limit)
    total_pages = (total // limit) + 1
    profissionais = [[str(key)+": "+str(value) for key, value in profissional.__dict__.items()] for profissional in profissionais]
    return {
        "data": profissionais,
        "pagination": {
            "total_pages": total_pages,
            "total": total,
            "offset": page,
            "limit": limit
        }
    }

@router.post("/", response_model=Profissional, status_code=201)
async def criar_profissional(
    data: Profissional,
    db: AsyncSession = Depends(get_db)
) -> Profissional:
    repository = ProfissionalRepository(db)
    logging.info("Criando um novo profissional")
    return await repository.create(data)

@router.get("/{id}", response_model=Profissional)
async def obter_profissional(
    id: int,
    db: AsyncSession = Depends(get_db)
) -> Profissional:
    repository = ProfissionalRepository(db)
    profissional = await repository.get_by_id(id)
    logging.info(f"Obtendo profissional de id {id}")
    if not profissional:
        logging.error(f"Profissional de id {id} não encontrado")
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    logging.info(f"Profissional encontrado: {profissional}")
    return profissional

@router.put("/{id}", response_model=Profissional)
async def atualizar_profissional(
    id: int,
    data: Profissional,
    db: AsyncSession = Depends(get_db)
) -> Profissional:
    repository = ProfissionalRepository(db)
    profissional = await repository.get_by_id(id)
    logging.info(f"Atualizando profissional de id {id}")
    if not profissional:
        logging.error(f"Profissional de id {id} não encontrado")
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    logging.info(f"Profissional encontrado: {profissional}")
    prof = await repository.update(id, data)
    logging.info(f"Profissional atualizado: {prof}")
    return prof

@router.delete("/{id}", status_code=204)
async def deletar_profissional(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    repository = ProfissionalRepository(db)
    profissional = await repository.get_by_id(id)
    logging.info(f"Deletando profissional de id {id}")
    if not profissional:
        logging.error(f"Profissional de id {id} não encontrado")
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    logging.info(f"Profissional encontrado: {profissional}")
    await repository
    logging.info(f"Profissional de id {id} deletado com sucesso")
    return
