from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.database import get_db
from core.exceptions import EstabelecimentoError, DatabaseValidationError
from repositories.estabelecimento import EstabelecimentoRepository
from schemas.estabelecimento import Estabelecimento, EstabelecimentoCreate, EstabelecimentoUpdate

router = APIRouter(
    prefix="/estabelecimentos",
    tags=["estabelecimentos"]
)

@router.get("/", response_model=List[Estabelecimento])
async def listar_estabelecimentos(
    db: AsyncSession = Depends(get_db)
) -> List[Estabelecimento]:

    repository = EstabelecimentoRepository(db)
    return await repository.get_all_with_endereco()

@router.get("/{id}", response_model=Estabelecimento)
async def obter_estabelecimento(
    id: int, 
    db: AsyncSession = Depends(get_db)
) -> Estabelecimento:

    repository = EstabelecimentoRepository(db)
    estabelecimento = await repository.get_by_id_with_endereco(id)
    if not estabelecimento:
        raise HTTPException(
            status_code=404, 
            detail=EstabelecimentoError.NOT_FOUND
        )
    return estabelecimento

@router.post("/", response_model=Estabelecimento, status_code=201)
async def criar_estabelecimento(
    data: EstabelecimentoCreate, 
    db: AsyncSession = Depends(get_db)
) -> Estabelecimento:

    repository = EstabelecimentoRepository(db)
    return await repository.create(data.model_dump())

@router.put("/{id}", response_model=Estabelecimento)
async def atualizar_estabelecimento(
    id: int, 
    data: EstabelecimentoUpdate, 
    db: AsyncSession = Depends(get_db)
) -> Estabelecimento:
    
    repository = EstabelecimentoRepository(db)
    estabelecimento = await repository.update(id, data.model_dump())
    if not estabelecimento:
        raise HTTPException(status_code=404, detail="Estabelecimento não encontrado")
    return estabelecimento

@router.delete("/{id}")
async def deletar_estabelecimento(
    id: int, 
    db: AsyncSession = Depends(get_db)
):
    repository = EstabelecimentoRepository(db)
    success = await repository.delete(id)
    if not success:
        raise HTTPException(
            status_code=404, 
            detail=EstabelecimentoError.NOT_FOUND
        )
    return {"message": EstabelecimentoError.DELETED}
