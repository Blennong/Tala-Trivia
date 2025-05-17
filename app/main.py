from typing import Optional
from fastapi import FastAPI

from app.database import Base, engine
from app.models import models

app = FastAPI()

# Crear tablas automáticamente si no existen
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}