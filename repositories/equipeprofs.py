from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from models.equipe import Equipe
from models.profissional import Profissional
from repositories.base import BaseRepository
from models.equipeprof import EquipeProf
from typing import List

class EquipeProfRepository(BaseRepository[EquipeProf]):
    def __init__(self, session):
        super().__init__(session, EquipeProf)
    
    async def create(self, data: dict) -> EquipeProf:
        try:
            query = select(Profissional.id).where(
                    Profissional.codigo_profissional_sus == data['codigo_profissional_sus']
                )
            result = await self.session.execute(query)
            profissional_id = result.scalar_one_or_none()
            if not profissional_id:
                raise HTTPException(
                    status_code=400,
                    detail="Profissional não encontrado"
                )
            data['profissional_id'] = profissional_id
            query = select(Equipe.id).where(
                    Equipe.codigo_equipe == data['codigo_equipe']
                )
            result = await self.session.execute(query)
            equipe_id = result.scalar_one_or_none()
            if not equipe_id:
                raise HTTPException(
                    status_code=400,
                    detail="Equipe não encontrada"
                )
            data['equipe_id'] = equipe_id

            data.pop('codigo_equipe')
            data.pop('codigo_profissional_sus')
            entity = self.model(**data)
            self.session.add(entity)
            await self.session.flush()
            await self.session.refresh(self.model)
            return entity
        except IntegrityError as e:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail=e)
    
    async def get_all(self) -> list[EquipeProf]:
        query = select(self.model)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update(self, id: int, data: dict) -> EquipeProf | None:
        try:
            return await super().update(id, data)
        except IntegrityError as e:
            if 'equipes_profissional_id_fkey' in str(e):
                raise HTTPException(
                    status_code=400,
                    detail="Profissional não encontrado ou já possui uma equipe cadastrada"
                )
            raise
    
    async def get_by_profissional_id(self, profissional_id: int) -> EquipeProf | None:
        query = select(self.model).where(self.model.profissional_id == profissional_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def delete(self, id: int):
        query = self.model.__table__.delete().where(self.model.id == id)
        await self.session.execute(query)
        await self
    
    async def get_by_filters(self, filters: dict) -> List[EquipeProf]:
        query = select(EquipeProf)
        for key, value in filters.items():
            query = query.where(getattr(EquipeProf, key) == value)
        result = await self.session.execute(query)
        return result.scalars().all

    async def get_total_count(self) -> int:
        query = select(func.count()).select_from(EquipeProf)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_paginated(self, limit: int, offset: int) -> List[EquipeProf]:
        query = select(EquipeProf).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()