from typing import Optional
from fastapi import FastAPI

from app.database import Base, engine
from app.models import models
from app.routers import user
from app.routers import auth

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"Bienvenidos a TalaTrivia API"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}