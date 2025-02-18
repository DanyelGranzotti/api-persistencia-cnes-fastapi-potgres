from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from models.base import BaseModel

class Estabelecimento(BaseModel):
    __tablename__ = "estabelecimentos"

    codigo_unidade = Column(String, nullable=False, unique=True)
    codigo_cnes = Column(String, nullable=False, unique=True)
    nome_razao_social_estabelecimento = Column(String, nullable=False)
    nome_fantasia_estabelecimento = Column(String, nullable=False)
    numero_telefone_estabelecimento = Column(String, nullable=True)
    email_estabelecimento = Column(String, nullable=True)
    
    # Change ForeignKey definition
    mantenedora_id = Column(Integer, ForeignKey("mantenedoras.id", ondelete="CASCADE"), nullable=False)
    cnpj_mantenedora = Column(String, nullable=False)
    
    mantenedora = relationship("Mantenedora", back_populates="estabelecimentos")
    endereco = relationship("Endereco", back_populates="estabelecimento", uselist=False)
    equipe = relationship("Equipe", back_populates="estabelecimento", uselist=False)
