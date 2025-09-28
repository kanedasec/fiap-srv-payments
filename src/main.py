from fastapi import FastAPI
from src.adapters.http.api import router

app = FastAPI(title="fiap-srv-payment", version="1.0.0")
app.include_router(router)
