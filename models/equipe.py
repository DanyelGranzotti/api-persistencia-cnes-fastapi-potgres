from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from models.base import BaseModel

class Equipe(BaseModel):
    __tablename__ = "equipes"

    codigo_equipe = Column(String, nullable=False, unique=True)
    nome_equipe = Column(String, nullable=False)
    tipo_equipe = Column(String, nullable=False)
    estabelecimento_id = Column(Integer, ForeignKey("estabelecimentos.id", ondelete="CASCADE"), nullable=False)

    profissionais = relationship("Profissional", secondary="equipeprofs", back_populates="equipes")
    estabelecimento = relationship("Estabelecimento", back_populates="equipe")