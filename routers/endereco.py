from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.database import get_db
from repositories.endereco import EnderecoRepository
from repositories.estabelecimento import EstabelecimentoRepository
from schemas.endereco import Endereco, EnderecoCreate, EnderecoUpdate
import logging

router = APIRouter(
    prefix="/enderecos",
    tags=["enderecos"]
)

@router.get("/", response_model=List[Endereco])
async def listar_enderecos(
    db: AsyncSession = Depends(get_db)
) -> List[Endereco]:
    repository = EnderecoRepository(db)
    logging.info("Listando enderecos")
    return await repository.get_all()

@router.get("/filtro")
async def filtrar_enderecos(
    estabelecimento_id: int = Query(None),
    cep_estabelecimento: str = Query(None),
    bairro: str = Query(None),
    db: AsyncSession = Depends(get_db)
) -> dict:
    repository = EnderecoRepository(db)
    filters = {}
    if estabelecimento_id:
        filters["estabelecimento_id"] = estabelecimento_id
    if cep_estabelecimento:
        filters["cep_estabelecimento"] = cep_estabelecimento
    if bairro:
        filters["bairro"] = bairro
    res = await repository.get_by_filters(filters)
    return {"res":[[str(key)+": "+str(value) for key, value in endereco.__dict__.items() if (not key.startswith("_"))] for endereco in res]}

@router.get("/paginated")
async def listar_enderecos_paginados(
    page: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db)
) -> dict:
    repository = EnderecoRepository(db)
    total = await repository.get_total_count()
    enderecos = await repository.get_paginated(limit=limit, offset=page * limit)
    total_pages = (total // limit) + 1
    enderecos = [[str(key)+": "+str(value) for key, value in endereco.__dict__.items()] for endereco in enderecos]
    return {
        "data": enderecos,
        "pagination": {
            "total_pages": total_pages,
            "total": total,
            "offset": page,
            "limit": limit
        }
    }

@router.get("/{id}", response_model=Endereco)
async def obter_endereco(
    id: int,
    db: AsyncSession = Depends(get_db)
) -> Endereco:
    repository = EnderecoRepository(db)
    endereco = await repository.get_by_id(id)
    if not endereco:
        logging.error(f"Endereço com ID {id} não encontrado")
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
    logging.info(f"Estabelecimento encontrado: {estabelecimento}")
    if not estabelecimento:
        logging.error(f"Estabelecimento com ID {data.estabelecimento_id} não encontrado")
        raise HTTPException(
            status_code=404,
            detail=f"Estabelecimento com ID {data.estabelecimento_id} não encontrado"
        )
    
    # Verificar se já existe um endereço para este estabelecimento
    endereco_repo = EnderecoRepository(db)
    endereco_existente = await endereco_repo.get_by_estabelecimento_id(data.estabelecimento_id)
    logging.info(f"Endereço existente: {endereco_existente}")
    if endereco_existente:
        logging.error(f"Já existe um endereço cadastrado para o estabelecimento {data.estabelecimento_id}")
        raise HTTPException(
            status_code=400,
            detail=f"Já existe um endereço cadastrado para o estabelecimento {data.estabelecimento_id}"
        )

    # Se passou pelas validações, criar o endereço
    logging.info("Endereço criado com sucesso")
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
    logging.info(f"Estabelecimento encontrado: {estabelecimento}")
    if not estabelecimento:
        logging.error(f"Estabelecimento com ID {data.estabelecimento_id} não encontrado")
        raise HTTPException(
            status_code=404,
            detail=f"Estabelecimento com ID {data.estabelecimento_id} não encontrado"
        )

    # Verificar se já existe um endereço para este estabelecimento
    endereco_repo = EnderecoRepository(db)
    endereco_existente = await endereco_repo.get_by_estabelecimento_id(data.estabelecimento_id)
    logging.info(f"Endereço existente: {endereco_existente}")
    if endereco_existente and endereco_existente.id != id:
        logging.error(f"Já existe um endereço cadastrado para o estabelecimento {data.estabelecimento_id}")
        raise HTTPException(
            status_code=400,
            detail=f"Já existe um endereço cadastrado para o estabelecimento {data.estabelecimento_id}"
        )

    # Atualizar o endereço
    logging.info("Endereço atualizado com sucesso")
    endereco = await endereco_repo.update(id, data.model_dump())
    if not endereco:
        logging.error(f"Endereço com ID {id} não encontrado")
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return endereco

@router.delete("/{id}")
async def deletar_endereco(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    repository = EnderecoRepository(db)
    success = await repository.delete(id)
    logging.info(f"Endereço deletado com sucesso: {success}")
    if not success:
        logging.error(f"Endereço com ID {id} não encontrado")
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return {"message": "Endereço deletado com sucesso"}
