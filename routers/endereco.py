from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.database import get_db
from repositories.endereco import EnderecoRepository
from repositories.estabelecimento import EstabelecimentoRepository
from schemas.endereco import Endereco, EnderecoCreate, EnderecoUpdate

router = APIRouter(
    prefix="/enderecos",
    tags=["enderecos"]
)

@router.get("/", response_model=List[Endereco])
async def listar_enderecos(
    db: AsyncSession = Depends(get_db)
) -> List[Endereco]:
    repository = EnderecoRepository(db)
    return await repository.get_all()

@router.get("/{id}", response_model=Endereco)
async def obter_endereco(
    id: int,
    db: AsyncSession = Depends(get_db)
) -> Endereco:
    repository = EnderecoRepository(db)
    endereco = await repository.get_by_id(id)
    if not endereco:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return endereco

@router.post("/", response_model=Endereco, status_code=201)
async def criar_endereco(
    data: EnderecoCreate,
    db: AsyncSession = Depends(get_db)
) -> Endereco:
    # Primeiro, verificar se o estabelecimento existe
    estabelecimento_repo = EstabelecimentoRepository(db)
    estabelecimento = await estabelecimento_repo.get_by_id(data.estabelecimento_id)
    if not estabelecimento:
        raise HTTPException(
            status_code=404,
            detail=f"Estabelecimento com ID {data.estabelecimento_id} não encontrado"
        )
    
    # Verificar se já existe um endereço para este estabelecimento
    endereco_repo = EnderecoRepository(db)
    endereco_existente = await endereco_repo.get_by_estabelecimento_id(data.estabelecimento_id)
    if endereco_existente:
        raise HTTPException(
            status_code=400,
            detail=f"Já existe um endereço cadastrado para o estabelecimento {data.estabelecimento_id}"
        )

    # Se passou pelas validações, criar o endereço
    return await endereco_repo.create(data.model_dump())

@router.put("/{id}", response_model=Endereco)
async def atualizar_endereco(
    id: int,
    data: EnderecoUpdate,
    db: AsyncSession = Depends(get_db)
) -> Endereco:
    # Verificar se o estabelecimento existe
    estabelecimento_repo = EstabelecimentoRepository(db)
    estabelecimento = await estabelecimento_repo.get_by_id(data.estabelecimento_id)
    if not estabelecimento:
        raise HTTPException(
            status_code=404,
            detail=f"Estabelecimento com ID {data.estabelecimento_id} não encontrado"
        )

    # Verificar se já existe um endereço para este estabelecimento
    endereco_repo = EnderecoRepository(db)
    endereco_existente = await endereco_repo.get_by_estabelecimento_id(data.estabelecimento_id)
    if endereco_existente and endereco_existente.id != id:
        raise HTTPException(
            status_code=400,
            detail=f"Já existe um endereço cadastrado para o estabelecimento {data.estabelecimento_id}"
        )

    # Atualizar o endereço
    endereco = await endereco_repo.update(id, data.model_dump())
    if not endereco:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return endereco

@router.delete("/{id}")
async def deletar_endereco(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    repository = EnderecoRepository(db)
    success = await repository.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return {"message": "Endereço deletado com sucesso"}
