import csv
import asyncio
from datetime import datetime
from typing import Dict, List
import os
from fastapi import HTTPException
from core.database import get_direct_session, init_models
from repositories.equipe import EquipeRepository
from repositories.equipeprofs import EquipeProfRepository
from repositories.mantenedora import MantenedoraRepository
from repositories.estabelecimento import EstabelecimentoRepository
from repositories.endereco import EnderecoRepository
from repositories.profissional import ProfissionalRepository

def read_csv_file(file_path: str) -> List[Dict]:
    encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
    
    for encoding in encodings:
        try:
            data = []
            with open(file_path, 'r', encoding=encoding) as file:
                reader = csv.reader(file, delimiter=';', quotechar='"')
                headers = next(reader)  # Skip header row
                
                for row in reader:
                    record = {}
                    for index, value in enumerate(row):
                        record[headers[index]] = value.strip() if value else None
                    data.append(record)
            return data
        except UnicodeDecodeError:
            continue
    
    raise ValueError(f"Could not read file {file_path} with any of the attempted encodings")

async def create_mantenedora(repo: MantenedoraRepository, data: Dict) -> Dict:
    try:
        date_str = data["TO_CHAR(DT_PREENCHIMENTO,'DD/MM/YYYY')"]
        if date_str:
            try:
                created_date = datetime.strptime(date_str, '%d/%m/%Y')
            except ValueError:
                created_date = None
        else:
            created_date = None

        mantenedora = {
            "cnpj_mantenedora": data["NU_CNPJ_MANTENEDORA"],
            "nome_razao_social_mantenedora": data["NO_RAZAO_SOCIAL"],
            "numero_telefone_mantenedora": data["NU_TELEFONE"],
            "codigo_banco": data["CO_BANCO"],
            "numero_agencia": data["NU_AGENCIA"], 
            "numero_conta_corrente": data["NU_CONTA_CORRENTE"],
            "data_criacao_mantenedora": created_date
        }

        return await repo.create(mantenedora)
    except Exception as e:
        print(f"Error creating mantenedora: {str(e)}")
        return None

async def create_estabelecimento_with_endereco(
    estab_repo: EstabelecimentoRepository,
    end_repo: EnderecoRepository,
    estab_data: Dict,
    mant_data: Dict
) -> Dict:
    try:
        estabelecimento = {
            "codigo_unidade": estab_data["CO_UNIDADE"],
            "codigo_cnes": estab_data["CO_CNES"],
            "cnpj_mantenedora": mant_data["NU_CNPJ_MANTENEDORA"],
            "nome_razao_social_estabelecimento": estab_data["NO_RAZAO_SOCIAL"],
            "nome_fantasia_estabelecimento": estab_data["NO_FANTASIA"],
            "numero_telefone_estabelecimento": estab_data["NU_TELEFONE"],
            "email_estabelecimento": estab_data.get("NO_EMAIL")
        }

        try:
            estab_result = await estab_repo.create(estabelecimento)
            if not estab_result:
                print(f"Error creating estabelecimento: {estabelecimento['codigo_unidade']}")
                return None

            # Convert latitude and longitude to float
            latitude = float(estab_data.get("NU_LATITUDE")) if estab_data.get("NU_LATITUDE") else None
            longitude = float(estab_data.get("NU_LONGITUDE")) if estab_data.get("NU_LONGITUDE") else None

            endereco = {
                "estabelecimento_id": estab_result.id,
                "latitude": latitude,
                "longitude": longitude,
                "cep_estabelecimento": estab_data["CO_CEP"],
                "bairro": estab_data["NO_BAIRRO"],
                "logradouro": estab_data["NO_LOGRADOURO"],
                "numero": estab_data["NU_ENDERECO"],
                "complemento": estab_data["NO_COMPLEMENTO"]
            }

            await end_repo.create(endereco)
            return estab_result

        except ValueError as ve:
            print(f"Error converting coordinates: {str(ve)}")
            return None
        except HTTPException as he:
            print(f"HTTP Error: {he.detail}")
            return None

    except Exception as e:
        print(f"Error processing estabelecimento: {str(e)}")
        return None

async def create_equipe(eqipe_repo: EquipeRepository, data: Dict) -> Dict:
    try:
        equipe = {
            "codigo_equipe": data["SEQ_EQUIPE"],
            "nome_equipe": data["NO_EQUIPE"],
            "tipo_equipe": data["TP_EQUIPE"],
            "codigo_unidade": data["CO_UNIDADE"]
        }

        return await eqipe_repo.create(equipe)
    except Exception as e:
        print(f"Error creating equipe: {str(e)}")
        return None

async def create_profissional(profRepo: ProfissionalRepository, data: Dict) -> Dict:
    try:
        profissional = {
            "codigo_profissional_sus": data["CO_PROFISSIONAL_SUS"],
            "nome_profissional": data["NO_PROFISSIONAL"],
            "codido_cns": data["CO_CNS"],
            "situacao_profissional_cadsus": data["ST_NMPROF_CADSUS"],
        }

        return await profRepo.create(profissional)
    except Exception as e:
        print(f"Error creating profissional: {str(e)}")
        return None

async def create_equipe_profissional(repo: EquipeProfRepository, data: Dict) -> Dict:
    try:
        equipe_profissional = {
            "codigo_equipe": data["SEQ_EQUIPE"],
            "codigo_profissional_sus": data["CO_PROFISSIONAL_SUS"]
        }

        return await repo.create(equipe_profissional)
    except Exception as e:
        print(f"Error creating equipe profissional: {str(e)}")
        return None

async def main():
    await init_models()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mantenedoras = read_csv_file(os.path.join(current_dir, 'tbMantenedora202501.csv'))
    estabelecimentos = read_csv_file(os.path.join(current_dir, 'tbEstabelecimento202501.csv'))
    equipes = read_csv_file(os.path.join(current_dir, 'tbEquipe.csv'))
    profissionais = read_csv_file(os.path.join(current_dir, 'tbProf.csv'))
    equipeprofs = read_csv_file(os.path.join(current_dir, 'tbEquipeProf.csv'))

    async with await get_direct_session() as session:
        mant_repo = MantenedoraRepository(session)
        estab_repo = EstabelecimentoRepository(session)
        end_repo = EnderecoRepository(session)

        for mant in mantenedoras:
            await create_mantenedora(mant_repo, mant)
        
        for estab in estabelecimentos:
            mant = next((m for m in mantenedoras if m["NU_CNPJ_MANTENEDORA"] == estab["NU_CNPJ_MANTENEDORA"]), None)
            
            if not mant:
                print(f"Warning: Mantenedora not found for estabelecimento {estab['CO_UNIDADE']} with CNPJ {estab['NU_CNPJ_MANTENEDORA']}")
                continue
                
            await create_estabelecimento_with_endereco(estab_repo, end_repo, estab, mant)
        
        for equipe in equipes:
            await create_equipe(EquipeRepository(session), equipe)
        
        for prof in profissionais:
            await create_profissional(ProfissionalRepository(session), prof)
        
        for eqprof in equipeprofs:
            await create_equipe_profissional(EquipeProfRepository(session), eqprof)

        await session.commit()

if __name__ == "__main__":
    asyncio.run(main())
