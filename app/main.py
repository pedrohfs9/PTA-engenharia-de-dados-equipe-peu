from fastapi import FastAPI
import uvicorn
from app.routers import example_router
from app.routers import products_router
from app.routers import example_router, vendedores, itens_pedidos

app = FastAPI(
    title="API de Tratamento de Dados - Desafio 1",
    description="API que recebe dados brutos, os trata e os devolve limpos.",
    version="1.0.0"
)

@app.get("/", description="Mensagem de boas-vindas da API.")
async def read_root():
    return {"message": "Bem-vindo à API de Tratamento de Dados!"}

@app.get("/health", description="Verifica a saúde da API.")
async def health_check():
    return {"status": "ok"}

app.include_router(example_router, prefix="/example", tags=["Example"])
app.include_router(products_router, prefix="/api/v1/produtos", tags=["Tratamento de Dados - Produtos"])
app.include_router(vendedores.router)
app.include_router(itens_pedidos.router)
