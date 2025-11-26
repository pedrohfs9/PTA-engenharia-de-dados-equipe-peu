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
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class Vendedores_bruto(BaseModel):
    seller_id: str
    seller_zip_code_prefix: Optional[Any] = None
    seller_city: Optional[str] = None
    seller_state: Optional[str] = None
    
    class Config:
        extra = "allow" 

class Vendedores_processado(BaseModel):
    seller_id: str
    seller_zip_code_prefix: str
    seller_city: str
    seller_state: str


class Itensdepedidos_bruto(BaseModel):
    order_id: str
    order_item_id: Optional[Any] = None
    product_id: str
    seller_id: str
    shipping_limit_date: Optional[Any] = None
    price: Optional[Any] = None
    freight_value: Optional[Any] = None
    
    class Config:
        extra = "allow"

class Itensdepedidos_processado(BaseModel):
    order_id: str
    order_item_id: int
    product_id: str
    seller_id: str
    shipping_limit_date: datetime
    price: float
    freight_value: float
