from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.database import get_db
from repositories.mantenedora import MantenedoraRepository
from schemas.mantenedora import Mantenedora, MantenedoraCreate, MantenedoraUpdate
import logging

router = APIRouter(
    prefix="/mantenedoras",
    tags=["mantenedoras"]
)

@router.get("/", response_model=List[Mantenedora])
async def listar_mantenedoras(
    db: AsyncSession = Depends(get_db)
) -> List[Mantenedora]:
    repository = MantenedoraRepository(db)
    logging.info("Listando mantenedoras")
    return await repository.get_all()

@router.get("/filtro", response_model=List[Mantenedora])
async def filtrar_mantenedoras(
    cnpj_mantenedora: str = Query(None),
    nome_razao_social_mantenedora: str = Query(None),
    db: AsyncSession = Depends(get_db)
) -> List[Mantenedora]:
    repository = MantenedoraRepository(db)
    filters = {}
    if cnpj_mantenedora:
        filters["cnpj_mantenedora"] = cnpj_mantenedora
    if nome_razao_social_mantenedora:
        filters["nome_razao_social_mantenedora"] = nome_razao_social_mantenedora
    return await repository.get_by_filters(filters)

@router.get("/paginated", response_model=dict)
async def listar_mantenedoras_paginadas(
    page: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: AsyncSession = Depends(get_db)
):
    repository = MantenedoraRepository(db)
    total = await repository.get_total_count()
    mantenedoras = await repository.get_paginated(limit=limit, offset=(page - 1) * limit)
    total_pages = (total + limit - 1) // limit
    return {
        "data": mantenedoras,
        "pagination": {
            "total_pages": total_pages,
            "total": total,
            "offset": page,
            "limit": limit
        }
    }

@router.post("/", response_model=Mantenedora, status_code=201)
async def criar_mantenedora(
    data: MantenedoraCreate,
    db: AsyncSession = Depends(get_db)
) -> Mantenedora:
    repository = MantenedoraRepository(db)
    logging.info("Criando mantenedora")
    return await repository.create(data.model_dump())

@router.get("/{id}", response_model=Mantenedora)
async def obter_mantenedora(
    id: int,
    db: AsyncSession = Depends(get_db)
) -> Mantenedora:
    repository = MantenedoraRepository(db)
    mantenedora = await repository.get_by_id(id)
    logging.info(f"Obtendo mantenedora de id {id}")
    if not mantenedora:
        logging.error(f"Mantenedora de id {id} não encontrada")
        raise HTTPException(status_code=404, detail="Mantenedora não encontrada")
    logging.info(f"Mantenedora de id {id} encontrada")
    return mantenedora

@router.put("/{id}", response_model=Mantenedora)
async def atualizar_mantenedora(
    id: int,
    data: MantenedoraUpdate,
    db: AsyncSession = Depends(get_db)
) -> Mantenedora:
    repository = MantenedoraRepository(db)
    mantenedora = await repository.get_by_id(id)
    logging.info(f"Atualizando mantenedora de id {id}")
    if not mantenedora:
        logging.error(f"Mantenedora de id {id} não encontrada")
        raise HTTPException(status_code=404, detail="Mantenedora não encontrada")
    logging.info(f"Mantenedora de id {id} encontrada")
    mantenedora = await repository.update(id, data.model_dump())
    logging.info(f"Mantenedora de id {id} atualizada")
    return mantenedora

@router.delete("/{id}", status_code=204)
async def deletar_mantenedora(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    repository = MantenedoraRepository(db)
    mantenedora = await repository.get_by_id(id)
    logging.info(f"Deletando mantenedora de id {id}")
    if not mantenedora:
        logging.error(f"Mantenedora de id {id} não encontrada")
        raise HTTPException(status_code=404, detail="Mantenedora não encontrada")
    logging.info(f"Mantenedora de id {id} encontrada")
    logging.info(f"Mantenedora de id {id} deletada")
    await repository.delete(id)
    return
