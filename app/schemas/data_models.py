from typing import Optional, List
from pydantic import BaseModel

# Modelo para a ENTRADA e SAÍDA dos dados de Produtos
# Este modelo usa Optional para colunas que podem ser nulas na entrada,
# antes do tratamento.
class ProductData(BaseModel):
    product_id: str
    product_category_name: Optional[str] = None
    product_name_lenght: Optional[float] = None
    product_description_lenght: Optional[float] = None
    product_photos_qty: Optional[float] = None
    product_weight_g: Optional[float] = None
    product_length_cm: Optional[float] = None
    product_height_cm: Optional[float] = None
    product_width_cm: Optional[float] = None

# Modelo para o corpo da requisição que é uma lista de produtos
class ProductList(BaseModel):
    data: List[ProductData]