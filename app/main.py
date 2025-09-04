from fastapi import FastAPI
from app.database.db import Base, engine
from app.routers import product


Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Project")


app.include_router(product.router)
