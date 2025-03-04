from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
import logging

from models.equipeprof import EquipeProf
from repositories.equipeprofs import EquipeProfRepository

router = APIRouter(
    prefix="/equipeprofs",
    tags=["equipeprofs"]
)

@router.get("/", response_model=List[EquipeProf])
async def listar_equipeprofs(
    db: AsyncSession = Depends(get_db)
) -> List[EquipeProf]:
    repository = EquipeProfRepository(db)
    logging.info("Listando equipeprofs")
    return await repository.get_all()

@router.get("/filtro")
async def filtrar_equipeprofs(
    equipe_id: int = Query(None),
    profissional_id: int = Query(None),
    db: AsyncSession = Depends(get_db)
) -> dict:
    repository = EquipeProfRepository(db)
    filters = {}
    if equipe_id:
        filters["equipe_id"] = equipe_id
    if profissional_id:
        filters["profissional_id"] = profissional_id
    res = await repository.get_by_filters(filters)
    return {"res":[[str(key)+": "+str(value) for key, value in equipeprof.__dict__.items() if (not key.startswith("_"))] for equipeprof in res]}

@router.get("/paginated")
async def listar_equipeprofs_paginados(
    page: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db)
) -> dict:
    repository = EquipeProfRepository(db)
    total = await repository.get_total_count()
    equipeprofs = await repository.get_paginated(limit=limit, offset=page * limit)
    total_pages = (total // limit) + 1
    equipeprofs = [[str(key)+": "+str(value) for key, value in equipeprof.__dict__.items()] for equipeprof in equipeprofs]
    return {
        "data": equipeprofs,
        "pagination": {
            "total_pages": total_pages,
            "total": total,
            "offset": page,
            "limit": limit
        }
    }

@router.post("/", response_model=EquipeProf, status_code=201)
async def criar_equipeprof(
    data: EquipeProf,
    db: AsyncSession = Depends(get_db)
) -> EquipeProf:
    repository = EquipeProfRepository(db)
    logging.info("Criando equipeprof")
    return await repository.create(data)

@router.get("/{id}", response_model=EquipeProf)
async def obter_equipeprof(
    id: int,
    db: AsyncSession = Depends(get_db)
) -> EquipeProf:
    repository = EquipeProfRepository(db)
    equipeprof = await repository.get_by_id(id)
    logging.info(f"Obtendo equipeprof com ID {id}")
    if not equipeprof:
        logging.error(f"EquipeProf com ID {id} não encontrada")
        raise HTTPException(status_code=404, detail="EquipeProf não encontrada")
    logging.info(f"EquipeProf encontrada: {equipeprof}")
    return equipeprof

@router.put("/{id}", response_model=EquipeProf)
async def atualizar_equipeprof(
    id: int,
    data: EquipeProf,
    db: AsyncSession = Depends(get_db)
) -> EquipeProf:
    repository = EquipeProfRepository(db)
    equipeprof = await repository.get_by_id(id)
    logging.info(f"Atualizando equipeprof com ID {id}")
    if not equipeprof:
        logging.error(f"EquipeProf com ID {id} não encontrada")
        raise HTTPException(status_code=404, detail="EquipeProf não encontrada")
    
    equipeprof = await repository.update(id, data)
    logging.info(f"EquipeProf atualizada: {equipeprof}")
    return equipeprof

@router.delete("/{id}", status_code=204)
async def deletar_equipeprof(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    repository = EquipeProfRepository(db)
    equipeprof = await repository.get_by_id(id)
    logging.info(f"Deletando equipeprof com ID {id}")
    if not equipeprof:
        logging.error(f"EquipeProf com ID {id} não encontrada")
        raise HTTPException(status_code=404, detail="EquipeProf não encontrada")
    logging.info(f"EquipeProf deletada: {equipeprof}")
    await repository.delete(id)
    return
