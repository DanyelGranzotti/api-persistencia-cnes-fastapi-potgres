from pydantic import BaseModel, Field, field_validator

class EnderecoBase(BaseModel):
    latitude: str | None = Field(
        default=None,
        example="-3.7436",
        description="Latitude do estabelecimento"
    )
    longitude: str | None = Field(
        default=None,
        example="-38.5229",
        description="Longitude do estabelecimento"
    )
    cep_estabelecimento: str = Field(
        example="60000000",
        min_length=8,
        max_length=8,
        description="CEP do estabelecimento"
    )
    bairro: str = Field(
        example="Centro",
        min_length=2,
        max_length=100,
        description="Bairro do estabelecimento"
    )
    logradouro: str = Field(
        example="Rua Principal",
        min_length=2,
        max_length=255,
        description="Logradouro do estabelecimento"
    )
    numero: str = Field(
        example="123",
        max_length=10,
        description="Número do estabelecimento"
    )
    complemento: str | None = Field(
        default=None,
        example="Sala 101",
        max_length=100,
        description="Complemento do endereço"
    )
    estabelecimento_id: int = Field(description="ID do estabelecimento relacionado")

    @field_validator('cep_estabelecimento')
    def validate_cep(cls, v):
        if not v.isdigit():
            raise ValueError('CEP deve conter apenas números')
        if len(v) != 8:
            raise ValueError('CEP deve ter 8 dígitos')
        return v

class EnderecoCreate(EnderecoBase):
    pass

class EnderecoUpdate(EnderecoBase):
    pass

class Endereco(EnderecoBase):
    id: int

    class Config:
        from_attributes = True
