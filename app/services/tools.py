import pandas as pd
import unicodedata
import numpy as np
from datetime import datetime

# --- FUNÇÕES UTILITÁRIAS REUTILIZÁVEIS ---

def converter_para_float(df: pd.DataFrame, colunas: list):
    for col in colunas:
        if col in df.columns:
            # Remove vírgulas e converte para numérico
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(',', '.', regex=False), 
                errors='coerce'
            )
    return df

def tratar_nulos_mediana(df: pd.DataFrame, colunas: list):
    """
    Preenche nulos com a mediana. 
    Usada tanto para Produtos quanto para Pedidos/Itens.
    """
    for col in colunas:
        if col in df.columns:
            # Garante conversão numérica antes da mediana
            df[col] = pd.to_numeric(df[col], errors='coerce')
            mediana = df[col].median()
            df[col] = df[col].fillna(mediana)
    return df

def tratar_data(df: pd.DataFrame, colunas: list):
    """
    Converte strings para datetime.
    CRÍTICO: dayfirst=True adicionado para suportar formato BR (DD/MM/AAAA) do CSV.
    """
    for col in colunas:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True)
    return df

def padronizar_texto(df: pd.DataFrame, colunas: list) -> pd.DataFrame:
    def _limpar(texto):
        if pd.isna(texto): return ""
        nfkd = unicodedata.normalize('NFKD', str(texto))
        sem_acento = "".join([c for c in nfkd if not unicodedata.combining(c)])
        return sem_acento.upper().strip()

    for col in colunas:
        if col in df.columns:
            df[col] = df[col].apply(_limpar)
    return df

# --- LÓGICA ESPECÍFICA DE PEDIDOS ---

def processar_dataset_pedidos(dados_brutos: list) -> list:
    df = pd.DataFrame(dados_brutos)
    if df.empty: return []

    # 1. Converter datas (Blinda contra formatos mistos)
    cols_temporais = [
        'order_purchase_timestamp', 'order_approved_at',
        'order_delivered_carrier_date', 'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]
    df = tratar_data(df, cols_temporais)

    # 2. Padronizar status
    if 'order_status' in df.columns:
        df['order_status'] = df['order_status'].astype(str).str.lower().str.strip()
        mapa_status = {
            'delivered': 'entregue', 'invoiced': 'faturado', 'shipped': 'enviado',
            'processing': 'em processamento', 'unavailable': 'indisponível',
            'canceled': 'cancelado', 'created': 'criado', 'approved': 'aprovado'
        }
        df['order_status'] = df['order_status'].replace(mapa_status)

    # 3. Métricas de Negócio
    # Verifica se colunas existem antes de calcular para evitar KeyError
    if {'order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date'}.issubset(df.columns):
        df['tempo_entrega_dias'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.days
        df['tempo_entrega_estimado_dias'] = (df['order_estimated_delivery_date'] - df['order_purchase_timestamp']).dt.days
        
        # Só calcula diferença se as colunas anteriores foram criadas com sucesso
        if 'tempo_entrega_dias' in df.columns:
            df['diferenca_entrega_dias'] = df['tempo_entrega_dias'] - df['tempo_entrega_estimado_dias']
            
            condicoes = [
                df['order_delivered_customer_date'].isna(),
                df['diferenca_entrega_dias'] <= 0,
                df['diferenca_entrega_dias'] > 0
            ]
            valores = ['Não Entregue', 'Sim', 'Não']
            df['entrega_no_prazo'] = np.select(condicoes, valores, default='Indefinido')

    # 4. Preparação para JSON (NaN -> None)
    df = df.where(pd.notnull(df), None)

    return df.to_dict(orient='records')