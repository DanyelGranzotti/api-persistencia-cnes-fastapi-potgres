from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from models.base import BaseModel
from datetime import datetime

class Mantenedora(BaseModel):
    __tablename__ = "mantenedoras"

    cnpj_mantenedora = Column(String, nullable=False, unique=True)
    nome_razao_social_mantenedora = Column(String, nullable=False)
    numero_telefone_mantenedora = Column(String, nullable=True)  
    codigo_banco = Column(String, nullable=True)  
    numero_agencia = Column(String, nullable=True)  
    numero_conta_corrente = Column(String, nullable=True)  
    data_criacao_mantenedora = Column(DateTime, default=datetime.utcnow)

    estabelecimentos = relationship(
        "Estabelecimento", 
        back_populates="mantenedora", 
        cascade="all, delete-orphan",
        passive_deletes=True
    )
