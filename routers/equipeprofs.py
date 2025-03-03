from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db

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
    return await repository.get_all()

@router.post("/", response_model=EquipeProf, status_code=201)
async def criar_equipeprof(
    data: EquipeProf,
    db: AsyncSession = Depends(get_db)
) -> EquipeProf:
    repository = EquipeProfRepository(db)
    return await repository.create(data)

@router.get("/{id}", response_model=EquipeProf)
async def obter_equipeprof(
    id: int,
    db: AsyncSession = Depends(get_db)
) -> EquipeProf:
    repository = EquipeProfRepository(db)
    equipeprof = await repository.get_by_id(id)
    if not equipeprof:
        raise HTTPException(status_code=404, detail="EquipeProf não encontrada")
    return equipeprof

@router.put("/{id}", response_model=EquipeProf)
async def atualizar_equipeprof(
    id: int,
    data: EquipeProf,
    db: AsyncSession = Depends(get_db)
) -> EquipeProf:
    repository = EquipeProfRepository(db)
    equipeprof = await repository.get_by_id(id)
    if not equipeprof:
        raise HTTPException(status_code=404, detail="EquipeProf não encontrada")
    return await repository.update(id, data)

@router.delete("/{id}", status_code=204)
async def deletar_equipeprof(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    repository = EquipeProfRepository(db)
    equipeprof = await repository.get_by_id(id)
    if not equipeprof:
        raise HTTPException(status_code=404, detail="EquipeProf não encontrada")
    await repository.delete(id)
    return