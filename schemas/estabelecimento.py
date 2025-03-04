from pydantic import BaseModel, Field, field_validator
from schemas.endereco import Endereco
import re

class EstabelecimentoBase(BaseModel):
    codigo_unidade: str = Field(
        example="123456",
        min_length=1,
        max_length=25,
        description="Código único da unidade"
    )
    codigo_cnes: str = Field(
        example="7891011",
        min_length=7,
        max_length=7,
        description="Código CNES do estabelecimento"
    )
    cnpj_mantenedora: str = Field(
        example="12345678901234",
        min_length=1,
        max_length=30,
        description="CNPJ da mantenedora"
    )
    nome_razao_social_estabelecimento: str = Field(
        example="Hospital São José LTDA",
        min_length=3,
        max_length=255,
        description="Razão social do estabelecimento"
    )
    nome_fantasia_estabelecimento: str = Field(
        example="Hospital São José",
        min_length=3,
        max_length=255,
        description="Nome fantasia do estabelecimento"
    )
    numero_telefone_estabelecimento: str | None = Field(
        default=None,
        example="(85) 3219-1234",
        max_length=20,
        description="Número de telefone do estabelecimento"
    )
    email_estabelecimento: str | None = Field(
        default=None,
        example="contato@saojose.com.br",
        max_length=255,
        description="Email do estabelecimento"
    )

class EstabelecimentoCreate(EstabelecimentoBase):
    mantenedora_id: int

class EstabelecimentoUpdate(EstabelecimentoBase):
    mantenedora_id: int

class Estabelecimento(EstabelecimentoBase):
    id: int
    mantenedora_id: int
    endereco: Endereco | None = None

    class Config:
        from_attributes = True
