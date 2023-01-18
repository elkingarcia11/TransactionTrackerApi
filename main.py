from fastapi import FastAPI
from routers import login, transactions

app = FastAPI()
app.include_router(login.router)
app.include_router(transactions.router)