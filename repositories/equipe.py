from sqlalchemy import select, update, func
from typing import List
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from models.estabelecimento import Estabelecimento
from repositories.base import BaseRepository
from models.equipe import Equipe

class EquipeRepository(BaseRepository[Equipe]):
    def __init__(self, session):
        super().__init__(session, Equipe)
    
    async def create(self, data: dict) -> Equipe:
        try:
            query = select(Estabelecimento.id).where(
                    Estabelecimento.codigo_unidade == str(data['codigo_unidade'])
                )
            result = await self.session.execute(query)
            estabelecimento_id = result.scalar_one_or_none()
            if not estabelecimento_id:
                raise HTTPException(
                    status_code=400,
                    detail="Estabelecimento não encontrado"
                )
            data['estabelecimento_id'] = estabelecimento_id
            entity = self.model(**data)
            self.session.add(entity)
            await self.session.flush()
            await self.session.refresh(entity)
            return entity
        except IntegrityError as e:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail=e)
    
    async def get_all(self) -> list[Equipe]:
        query = select(self.model)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update(self, id: int, data: dict) -> Equipe | None:
        try:
            return await super().update(id, data)
        except IntegrityError as e:
            if 'equipes_profissional_id_fkey' in str(e):
                raise HTTPException(
                    status_code=400,
                    detail="Profissional não encontrado ou já possui uma equipe cadastrada"
                )
            raise
    
    async def get_with_profissionais(self, id: int) -> Equipe:
        query = select(Equipe).options(selectinload(Equipe.profissionais)).where(Equipe.id == id)
        result = await self.session.execute(query)
        print(result)
        return result.scalar_one_or_none()
    
    async def get_by_profissional_id(self, profissional_id: int) -> Equipe | None:
        query = select(self.model).where(self.model.profissional_id == profissional_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def delete(self, id: int):
        query = self.model.__table__.delete().where(self.model.id == id)
        await self.session.execute(query)
        await self.session.flush()

    async def get_by_filters(self, filters: dict) -> List[Equipe]:
        query = select(Equipe)
        for key, value in filters.items():
            query = query.where(getattr(Equipe, key) == value)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_total_count(self) -> int:
        query = select(func.count()).select_from(Equipe)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_paginated(self, limit: int, offset: int) -> List[Equipe]:
        query = select(Equipe).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()