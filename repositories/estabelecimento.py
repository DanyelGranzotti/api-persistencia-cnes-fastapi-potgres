from sqlalchemy import select
from repositories.base import BaseRepository
from models.estabelecimento import Estabelecimento

class EstabelecimentoRepository(BaseRepository[Estabelecimento]):
    def __init__(self, session):
        super().__init__(session, Estabelecimento)
    
    async def get_by_codigo_unidade(self, codigo: str) -> Estabelecimento | None:
        query = select(self.model).where(self.model.codigo_unidade == codigo)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_codigo_cnes(self, codigo: str) -> Estabelecimento | None:
        query = select(self.model).where(self.model.codigo_cnes == codigo)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
