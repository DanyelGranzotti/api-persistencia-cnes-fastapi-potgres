from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from repositories.base import BaseRepository
from models.endereco import Endereco
from typing import List

class EnderecoRepository(BaseRepository[Endereco]):
    def __init__(self, session):
        super().__init__(session, Endereco)
    
    async def create(self, data: dict) -> Endereco:
        try:
            return await super().create(data)
        except IntegrityError as e:
            if 'enderecos_estabelecimento_id_fkey' in str(e):
                raise HTTPException(
                    status_code=400,
                    detail="Estabelecimento não encontrado ou já possui um endereço cadastrado"
                )
            raise

    async def update(self, id: int, data: dict) -> Endereco | None:
        try:
            return await super().update(id, data)
        except IntegrityError as e:
            if 'enderecos_estabelecimento_id_fkey' in str(e):
                raise HTTPException(
                    status_code=400,
                    detail="Estabelecimento não encontrado ou já possui um endereço cadastrado"
                )
            raise
    
    async def get_by_estabelecimento_id(self, estabelecimento_id: int) -> Endereco | None:
        query = select(self.model).where(self.model.estabelecimento_id == estabelecimento_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_filters(self, filters: dict) -> List[Endereco]:
        query = select(Endereco)
        for key, value in filters.items():
            query = query.where(getattr(Endereco, key) == value)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_total_count(self) -> int:
        query = select(func.count()).select_from(Endereco)
        result = await self.session.execute(query)
        return result.scalar()
    
    async def get_paginated(self, limit: int, offset: int) -> List[Endereco]:
        query = select(Endereco).limit(limit).offset((offset))
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_all(self) -> list[Endereco]:
        print("\n Entrou no get_all de endereco \n")
        query = select(self.model)
        result = await self.session.execute(query)
        print("\n Resultado do get_all de endereco \n")
        return result.scalars().all()
