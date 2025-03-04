import json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.database import get_db
from core.exceptions import EstabelecimentoError, DatabaseValidationError
from repositories.estabelecimento import EstabelecimentoRepository
from schemas.estabelecimento import Estabelecimento, EstabelecimentoCreate, EstabelecimentoUpdate
import logging
router = APIRouter(
    prefix="/estabelecimentos",
    tags=["estabelecimentos"]
)

@router.get("/", response_model=List[Estabelecimento])
async def listar_estabelecimentos(
    db: AsyncSession = Depends(get_db)
) -> List[Estabelecimento]:
    
    repository = EstabelecimentoRepository(db)
    logging.info("Listando estabelecimentos")
    return await repository.get_all_with_endereco()

@router.get("/filtro")
async def filtrar_estabelecimentos(
    codigo_unidade: str = Query(None),
    codigo_cnes: str = Query(None),
    nome_fantasia_estabelecimento: str = Query(None),
    db: AsyncSession = Depends(get_db)
) -> dict:
    repository = EstabelecimentoRepository(db)
    filters = {}
    if codigo_unidade:
        filters["codigo_unidade"] = codigo_unidade
    if codigo_cnes:
        filters["codigo_cnes"] = codigo_cnes
    if nome_fantasia_estabelecimento:
        filters["nome_fantasia_estabelecimento"] = nome_fantasia_estabelecimento
    res = await repository.get_by_filters(filters)
    return {"res":[[str(key)+": "+str(value) for key, value in estabelecimento.__dict__.items() if (not key.startswith("_"))] for estabelecimento in res]}
    

@router.get("/paginated")
async def listar_estabelecimentos_p(
    page: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db)
) -> dict:
    repository = EstabelecimentoRepository(db)
    total = await repository.get_total_count()
    estabelecimentos = await repository.get_paginated(limit=limit, offset=page * limit) 
    total_pages = (total // limit) + 1
    estabelecimentos = [[str(key)+": "+str(value) for key, value in estabelecimento.__dict__.items()] for estabelecimento in estabelecimentos]
    return {
        "data": estabelecimentos,
        "pagination": {
            "total_pages": total_pages,
            "total": total,
            "offset": page,
            "limit": limit
        }
    }

@router.get("/{id}", response_model=Estabelecimento)
async def obter_estabelecimento(
    id: int, 
    db: AsyncSession = Depends(get_db)
) -> Estabelecimento:
    repository = EstabelecimentoRepository(db)
    estabelecimento = await repository.get_by_id_with_endereco(id)
    logging.info(f"Estabelecimento encontrado: {estabelecimento}")
    if not estabelecimento:
        logging.error(f"Estabelecimento com ID {id} não encontrado")
        raise HTTPException(
            status_code=404, 
            detail=EstabelecimentoError.NOT_FOUND
        )
    logging.info(f"Endereço do estabelecimento: {estabelecimento.endereco}")
    return estabelecimento

@router.post("/", response_model=Estabelecimento, status_code=201)
async def criar_estabelecimento(
    data: EstabelecimentoCreate, 
    db: AsyncSession = Depends(get_db)
) -> Estabelecimento:

    repository = EstabelecimentoRepository(db)
    logging.info(f"Criando estabelecimento: {data}")
    return await repository.create(data.model_dump())

@router.put("/{id}", response_model=Estabelecimento)
async def atualizar_estabelecimento(
    id: int, 
    data: EstabelecimentoUpdate, 
    db: AsyncSession = Depends(get_db)
) -> Estabelecimento:
    
    repository = EstabelecimentoRepository(db)
    estabelecimento = await repository.update(id, data.model_dump())
    logging.info(f"Estabelecimento atualizado: {estabelecimento}")
    if not estabelecimento:
        logging.error(f"Estabelecimento com ID {id} não encontrado")
        raise HTTPException(status_code=404, detail="Estabelecimento não encontrado")
    logging.info(f"Endereço do estabelecimento: {estabelecimento.endereco}")
    logging.info(f"Estabelecimento atualizado: {estabelecimento}")
    return estabelecimento

@router.delete("/{id}")
async def deletar_estabelecimento(
    id: int, 
    db: AsyncSession = Depends(get_db)
):
    repository = EstabelecimentoRepository(db)
    success = await repository.delete(id)
    logging.info(f"Estabelecimento deletado: {success}")
    if not success:
        logging.error(f"Estabelecimento com ID {id} não encontrado")
        raise HTTPException(
            status_code=404, 
            detail=EstabelecimentoError.NOT_FOUND
        )
    logging.info(f"Estabelecimento com ID {id} deletado com sucesso")
    return {"message": EstabelecimentoError.DELETED}