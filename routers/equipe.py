from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db

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
    return await repository.get_all()

@router.post("/", response_model=Equipe, status_code=201)
async def criar_equipe(
    data: Equipe,
    db: AsyncSession = Depends(get_db)
) -> Equipe:
    repository = EquipeRepository(db)
    return await repository.create(data)

@router.get("/{id}", response_model=Equipe)
async def obter_equipe(
    id: int,
    db: AsyncSession = Depends(get_db)
) -> Equipe:
    repository = EquipeRepository(db)
    equipe = await repository.get_by_id(id)
    if not equipe:
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
    if not equipe:
        raise HTTPException(status_code=404, detail="Equipe não encontrada")
    return await repository.update(id, data)

@router.delete("/{id}", status_code=204)
async def deletar_equipe(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    repository = EquipeRepository(db)
    equipe = await repository.get_by_id(id)
    if not equipe:
        raise HTTPException(status_code=404, detail="Equipe não encontrada")
    await repository.delete(id)
    return

@router.get("/{id}/profissionais", response_model=Equipe)
async def obter_equipe_com_profissionais(
    id: int,
    db: AsyncSession = Depends(get_db)
) -> Equipe:
    repository = EquipeRepository(db)
    equipe = await repository.get_with_profissionais(id)
    print("\n")
    print(equipe)
    print("===================================\n")
    if not equipe:
        raise HTTPException(status_code=404, detail="Equipe não encontrada")
    return equipe