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
    seller_zip_code_prefix: int
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