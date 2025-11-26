import pandas as pd
from typing import List, Dict, Any

def tratar_produtos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Função que aplica as regras de padronização e tratamento de nulos
    para o dataset de Produtos (olist_products_dataset).
    """
    
    # 1. TRATAMENTO DE CATEGORIAS (Texto e Nulos)
    df['product_category_name'] = (
        df['product_category_name']
        .str.lower()
        .str.replace(' ', '_', regex=True)
    )
    df['product_category_name'] = df['product_category_name'].fillna('indefinido') # 
    
    # 2. TRATAMENTO DE NULOS (NUMÉRICOS PELA MEDIANA)
    colunas_numericas_produtos = [
        'product_name_lenght',
        'product_description_lenght',
        'product_photos_qty',
        'product_weight_g',
        'product_length_cm',
        'product_height_cm',
        'product_width_cm'
    ]
    
    for coluna in colunas_numericas_produtos:
        # Valores nulos em colunas numéricas devem ser substituídos pela mediana 
        mediana_valor = df[coluna].median()
        df[coluna] = df[coluna].fillna(mediana_valor)
        
    # Retorna o DataFrame limpo para ser usado pela API
    return df