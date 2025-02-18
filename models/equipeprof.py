from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from models.base import BaseModel

class EquipeProf(BaseModel):
    __tablename__ = "equipeprofs"

    equipe_id = Column(Integer, ForeignKey("equipes.id", ondelete="CASCADE"), nullable=False)
    profissional_id = Column(Integer, ForeignKey("profissionais.id", ondelete="CASCADE"), nullable=False)