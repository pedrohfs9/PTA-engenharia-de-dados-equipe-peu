from fastapi import APIRouter, HTTPException
from typing import List

# Importamos os novos modelos e a lógica
from app.services.tools import processar_dataset_pedidos
from app.schemas.example import OrderInput, OrderProcessed

router = APIRouter(prefix="/etl", tags=["ETL Pipeline"])

@router.post("/processar_pedidos", response_model=List[OrderProcessed])
def processar_pedidos_endpoint(payload: List[OrderInput]):
    """
    Endpoint tipado:
    - Entrada: Valida se o JSON tem os campos de OrderInput.
    - Saída: Garante que o retorno siga o formato OrderProcessed.
    """
    try:
        print(f"Recebidos {len(payload)} registros.")
        
        # Converte a lista de modelos Pydantic para lista de dicionários puros
        # para o Pandas poder ler.
        dados_brutos = [item.model_dump() for item in payload]
        
        # Processa
        dados_tratados = processar_dataset_pedidos(dados_brutos)
        
        return dados_tratados
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")