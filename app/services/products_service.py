import pandas as pd
from .tools import tratar_nulos_mediana # Reutilizando lógica (DRY)

def tratar_produtos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica regras de padronização para produtos.
    """
    
    # 1. Tratamento de Categorias
    # Previne erro se a coluna vier toda nula ou numérica
    df['product_category_name'] = df['product_category_name'].fillna('indefinido')
    df['product_category_name'] = (
        df['product_category_name']
        .astype(str)
        .str.lower()
        .str.replace(' ', '_', regex=True)
    )
    
    # 2. Tratamento de Nulos (Numéricos)
    colunas_numericas_produtos = [
        'product_name_lenght', # Mantido 'lenght' pois é assim que está no seu CSV
        'product_description_lenght',
        'product_photos_qty',
        'product_weight_g',
        'product_length_cm',
        'product_height_cm',
        'product_width_cm'
    ]
    
    # Usa a função importada do tools.py em vez de reescrever a lógica
    df = tratar_nulos_mediana(df, colunas_numericas_produtos)
    
    # 3. Limpeza final para API
    df = df.where(pd.notnull(df), None)
        
    return df