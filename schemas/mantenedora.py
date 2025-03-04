from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import re

class MantenedoraBase(BaseModel):
    cnpj_mantenedora: str = Field(
        example="12345678901234",
        min_length=1,
        max_length=30,
        description="CNPJ da mantenedora"
    )
    nome_razao_social_mantenedora: str = Field(
        example="Mantenedora LTDA",
        min_length=1,
        max_length=255,
        description="Razão social da mantenedora"
    )
    numero_telefone_mantenedora: str | None = Field(
        default=None,
        example="(85) 3219-1234",
        max_length=20,
        description="Número de telefone da mantenedora"
    )
    codigo_banco: str | None = Field(
        default=None,
        example="001",
        min_length=1,
        max_length=30,
        description="Código do banco"
    )
    numero_agencia: str | None = Field(
        default=None,
        example="1234",
        max_length=10,
        description="Número da agência"
    )
    numero_conta_corrente: str | None = Field(
        default=None,
        example="123456-7",
        max_length=20,
        description="Número da conta corrente"
    )

class MantenedoraCreate(MantenedoraBase):
    pass

class MantenedoraUpdate(MantenedoraBase):
    pass

class Mantenedora(MantenedoraBase):
    id: int
    data_criacao_mantenedora: datetime

    class Config:
        from_attributes = True
