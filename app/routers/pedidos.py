from fastapi import APIRouter, HTTPException
from typing import List

# Importando a lógica 
from app.services.tools import processar_dataset_pedidos
from app.schemas.data_models import OrderInput, OrderProcessed

router = APIRouter(prefix="/etl", tags=["ETL Pipeline"])

@router.post("/processar_pedidos", response_model=List[OrderProcessed])
def processar_pedidos_endpoint(payload: List[OrderInput]):
    try:
        # Converter Pydantic -> Dict
        dados_brutos = [item.model_dump() for item in payload]
        
        # Processar
        dados_tratados = processar_dataset_pedidos(dados_brutos)
        
        return dados_tratados
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro em pedidos: {str(e)}")