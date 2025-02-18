from fastapi import HTTPException

class DatabaseError:
    UNIQUE_VIOLATION = "23505"  # Código PostgreSQL para violação de unicidade

class EstabelecimentoError:
    NOT_FOUND = "Estabelecimento não encontrado"
    CODIGO_UNIDADE_EXISTS = "Já existe um estabelecimento com este código de unidade"
    CODIGO_CNES_EXISTS = "Já existe um estabelecimento com este código CNES"
    INVALID_CNPJ = "CNPJ inválido"
    DELETED = "Estabelecimento deletado com sucesso"
    UNIQUE_VIOLATION_MAPPING = {
        "estabelecimentos_codigo_unidade_key": "Já existe um estabelecimento com este código de unidade",
        "estabelecimentos_codigo_cnes_key": "Já existe um estabelecimento com este código CNES"
    }

class ProfissionalError:
    NOT_FOUND = "Profissional não encontrado"
    CODIGO_PROF_SUS_EXISTS = "Já existe um profissional com este código do profissional SUS"
    UNIQUE_VIOLATION_MAPPING = {
        "profissionais_codigo_profissional_sus_key": "Já existe um profissional com este código do profissional SUS"
    }

class DatabaseValidationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)
