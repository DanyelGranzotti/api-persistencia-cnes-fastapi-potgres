from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from models.base import BaseModel
from datetime import datetime

class Mantenedora(BaseModel):
    __tablename__ = "mantenedoras"

    cnpj_mantenedora = Column(String(14), nullable=False, unique=True)
    nome_razao_social_mantenedora = Column(String(255), nullable=False)
    numero_telefone_mantenedora = Column(String(20))
    codigo_banco = Column(String(3), nullable=False)
    numero_agencia = Column(String(10), nullable=False)
    numero_conta_corrente = Column(String(20), nullable=False)
    data_criacao_mantenedora = Column(DateTime, default=datetime.utcnow)
    
    estabelecimentos = relationship(
        "Estabelecimento", 
        back_populates="mantenedora", 
        cascade="all, delete-orphan",
        passive_deletes=True
    )
