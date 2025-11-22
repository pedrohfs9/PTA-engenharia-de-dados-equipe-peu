from fastapi import APIRouter
import pandas as pd
from typing import List, Dict, Any
from app.services.products_service import tratar_produtos # Importa a função de tratamento

# Cria um novo roteador FastAPI
router = APIRouter()

@router.post("") # O endpoint será o prefixo definido no main.py, que é "/api/v1/produtos"
def processar_produtos_endpoint(dados_brutos: List[Dict[str, Any]]):
    """
    Recebe os dados brutos de Produtos via POST, processa-os e retorna o resultado limpo.
    Esta função será chamada pelo orquestrador N8N.
    """
    
    try:
        # 1. Converte a lista de dicionários (JSON) recebida em um DataFrame Pandas
        df_bruto = pd.DataFrame(dados_brutos)
        
        # 2. Chama a função de serviço que contém toda a lógica de limpeza
        df_limpo = tratar_produtos(df_bruto)
        
        # 3. Converte o DataFrame limpo de volta para uma lista de dicionários (JSON)
        dados_limpos_json = df_limpo.to_dict('records')
        
        # 4. Retorna a resposta padronizada
        return {"status": "success", "total_registros": len(dados_limpos_json), "data": dados_limpos_json}
    
    except Exception as e:
        # Retorna erro caso algo dê errado no processamento
        return {"status": "error", "message": f"Falha no processamento: {str(e)}"}