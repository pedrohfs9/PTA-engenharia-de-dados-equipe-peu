from fastapi import FastAPI
from app.routers import pedidos, products_router, vendedores, itens_pedidos

app = FastAPI(
    title="API de Engenharia de Dados - Desafio",
    version="1.0.0"
)

@app.get("/", tags=["Health"])
async def read_root():
    return {"message": "API Online e Operante"}

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

# --- Rotas Padronizadas (/api/v1) ---

# 1. Produtos (Usa a versão refatorada com Pydantic)
app.include_router(
    products_router.router, 
    prefix="/api/v1/produtos", 
    tags=["Produtos"]
)

# 2. Pedidos
app.include_router(
    pedidos.router, 
    prefix="/api/v1/pedidos", 
    tags=["Pedidos"]
)

# 3. Vendedores
app.include_router(
    vendedores.router,
    prefix="/api/v1/vendedores",
    tags=["Vendedores"]
)
