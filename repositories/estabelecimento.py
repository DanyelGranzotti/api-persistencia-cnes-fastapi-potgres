from sqlalchemy import select, update, func
from typing import List
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from repositories.base import BaseRepository
from models.estabelecimento import Estabelecimento
from models.mantenedora import Mantenedora

class EstabelecimentoRepository(BaseRepository[Estabelecimento]):
    def __init__(self, session):
        super().__init__(session, Estabelecimento)

    async def create(self, data: dict) -> Estabelecimento:
        try:
            # Get mantenedora_id from cnpj
            if 'cnpj_mantenedora' in data:
                query = select(Mantenedora.id).where(
                    Mantenedora.cnpj_mantenedora == data['cnpj_mantenedora']
                )
                result = await self.session.execute(query)
                mantenedora_id = result.scalar_one_or_none()
                
                if not mantenedora_id:
                    raise HTTPException(status_code=400, detail="Mantenedora não encontrada")
                
                # Keep both cnpj and id
                estabelecimento_data = {
                    "codigo_unidade": data["codigo_unidade"],
                    "codigo_cnes": data["codigo_cnes"],
                    "cnpj_mantenedora": data["cnpj_mantenedora"],  # Keep the CNPJ
                    "nome_razao_social_estabelecimento": data["nome_razao_social_estabelecimento"],
                    "nome_fantasia_estabelecimento": data["nome_fantasia_estabelecimento"],
                    "numero_telefone_estabelecimento": data["numero_telefone_estabelecimento"],
                    "email_estabelecimento": data["email_estabelecimento"],
                    "mantenedora_id": mantenedora_id
                }
            else:
                estabelecimento_data = data

            # Create entity
            entity = self.model(**estabelecimento_data)
            self.session.add(entity)
            await self.session.flush()
            await self.session.refresh(entity)
            
            # Get fresh copy with relationships
            query = select(self.model).options(
                selectinload(self.model.endereco)
            ).where(self.model.id == entity.id)
            result = await self.session.execute(query)
            return result.scalar_one()
            
        except IntegrityError as e:
            await self.session.rollback()
            print(f"IntegrityError: {str(e)}")  # Add debug print
            if 'estabelecimentos_codigo_unidade_key' in str(e):
                raise HTTPException(status_code=400, detail="Código da unidade já existe")
            if 'estabelecimentos_codigo_cnes_key' in str(e):
                raise HTTPException(status_code=400, detail="Código CNES já existe")
            raise HTTPException(status_code=400, detail=f"Erro ao criar estabelecimento: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")  # Add debug print
            raise HTTPException(status_code=400, detail=f"Erro inesperado: {str(e)}")

    async def update(self, id: int, data: dict) -> Estabelecimento | None:
        try:
            query = update(self.model).where(
                self.model.id == id
            ).values(**data).returning(self.model)
            result = await self.session.execute(query)
            await self.session.flush()
            
            # Get fresh copy with relationships
            entity = result.scalar_one_or_none()
            if entity:
                query = select(self.model).options(
                    selectinload(self.model.endereco)
                ).where(self.model.id == id)
                result = await self.session.execute(query)
                return result.scalar_one()
            return None
            
        except IntegrityError as e:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail="Erro ao atualizar estabelecimento")

    async def get_all_with_endereco(self) -> list[Estabelecimento]:
        query = select(self.model).options(selectinload(self.model.endereco))
        result = await self.session.execute(query)
        print(result.scalars().unique())
        return list(result.scalars().unique())
    
    async def get_by_id_with_endereco(self, id: int) -> Estabelecimento | None:
        query = select(self.model).options(selectinload(self.model.endereco)).where(self.model.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_codigo_unidade(self, codigo: str) -> Estabelecimento | None:
        query = select(self.model).where(self.model.codigo_unidade == codigo)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_codigo_cnes(self, codigo: str) -> Estabelecimento | None:
        query = select(self.model).where(self.model.codigo_cnes == codigo)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_filters(self, filters: dict) -> list[Estabelecimento]:
        query = select(Estabelecimento)
        print(filters)
        for key, value in filters.items():
            print(key, value)
            query = query.where(getattr(Estabelecimento, key) == value)
        print("bejhcbjhcb")
        result = await self.session.execute(query)
        print("\n", query, "\n")
        return result.scalars().all()

    async def get_total_count(self) -> int:
        query = select(func.count()).select_from(Estabelecimento)
        result = await self.session.execute(query)
        return result.scalar()
    
    async def get_paginated(self, limit: int, offset: int) -> List[Estabelecimento]:
        query = select(Estabelecimento).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()