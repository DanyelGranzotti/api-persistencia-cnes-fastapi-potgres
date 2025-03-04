from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
import logging

from schemas.equipe import Equipe
from repositories.equipe import EquipeRepository

router = APIRouter(
    prefix="/equipes",
    tags=["equipes"]
)

@router.get("/", response_model=List[Equipe])
async def listar_equipes(
    db: AsyncSession = Depends(get_db)
) -> List[Equipe]:
    repository = EquipeRepository(db)
    logging.info("Listando equipes")
    return await repository.get_all()

@router.post("/", response_model=Equipe, status_code=201)
async def criar_equipe(
    data: Equipe,
    db: AsyncSession = Depends(get_db)
) -> Equipe:
    repository = EquipeRepository(db)
    logging.info(f"Criando equipe: {data}")
    return await repository.create(data)

@router.get("/{id}", response_model=Equipe)
async def obter_equipe(
    id: int,
    db: AsyncSession = Depends(get_db)
) -> Equipe:
    repository = EquipeRepository(db)
    equipe = await repository.get_by_id(id)
    logging.info(f"Obtendo equipe com ID {id}")
    if not equipe:
        logging.error(f"Equipe com ID {id} não encontrada")
        raise HTTPException(status_code=404, detail="Equipe não encontrada")
    return equipe

@router.put("/{id}", response_model=Equipe)
async def atualizar_equipe(
    id: int,
    data: Equipe,
    db: AsyncSession = Depends(get_db)
) -> Equipe:
    repository = EquipeRepository(db)
    equipe = await repository.get_by_id(id)
    logging.info(f"Atualizando equipe com ID {id}")
    if not equipe:
        logging.error(f"Equipe com ID {id} não encontrada")
        raise HTTPException(status_code=404, detail="Equipe não encontrada")
    logging.info(f"Equipe encontrada: {equipe}")
    
    equipe = await repository.update(id, data)
    logging.info(f"Equipe atualizada: {equipe}")
    return equipe


@router.delete("/{id}", status_code=204)
async def deletar_equipe(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    repository = EquipeRepository(db)
    equipe = await repository.get_by_id(id)
    logging.info(f"Deletando equipe com ID {id}")
    if not equipe:
        logging.error(f"Equipe com ID {id} não encontrada")
        raise HTTPException(status_code=404, detail="Equipe não encontrada")
    await repository.delete(id)
    logging.info(f"Equipe com ID {id} deletada")
    return

@router.get("/{id}/profissionais", response_model=Equipe)
async def obter_equipe_com_profissionais(
    id: int,
    db: AsyncSession = Depends(get_db)
) -> Equipe:
    repository = EquipeRepository(db)
    equipe = await repository.get_with_profissionais(id)
    logging.info(f"Obtendo equipe com ID {id} e seus profissionais")
    print("\n")
    print(equipe)
    print("===================================\n")
    if not equipe:
        logging.error(f"Equipe com ID {id} não encontrada")
        raise HTTPException(status_code=404, detail="Equipe não encontrada")
    logging.info(f"Equipe com ID {id} e seus profissionais obtida")
    return equipe

@router.get("/filtro", response_model=List[Equipe])
async def filtrar_equipes(
    codigo_equipe: str = Query(None),
    nome_equipe: str = Query(None),
    tipo_equipe: str = Query(None),
    db: AsyncSession = Depends(get_db)
) -> List[Equipe]:
    repository = EquipeRepository(db)
    filters = {}
    if codigo_equipe:
        filters["codigo_equipe"] = codigo_equipe
    if nome_equipe:
        filters["nome_equipe"] = nome_equipe
    if tipo_equipe:
        filters["tipo_equipe"] = tipo_equipe
    return await repository.get_by_filters(filters)

@router.get("/paginated", response_model=dict)
async def listar_equipes_paginadas(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    db: AsyncSession = Depends(get_db)
):
    repository = EquipeRepository(db)
    total = await repository.get_total_count()
    equipes = await repository.get_paginated(limit=limit, offset=(page - 1) * limit)
    total_pages = (total + limit - 1) // limit
    return {
        "data": equipes,
        "pagination": {
            "total_pages": total_pages,
            "total": total,
            "offset": page,
            "limit": limit
        }
    }
