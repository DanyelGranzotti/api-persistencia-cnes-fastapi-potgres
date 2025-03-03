from typing import List
from fastapi import APIRouter, Depends, HTTPException
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
