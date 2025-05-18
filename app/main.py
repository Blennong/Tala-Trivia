from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.database import Base, engine
from app.models import models

from app.routers import user, auth, trivia, question, trivia_question, attempts, rankings

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(trivia.router)
app.include_router(question.router)
app.include_router(trivia_question.router)
app.include_router(attempts.router)
app.include_router(rankings.router)

@app.get("/")
def read_root():
    return {"Bienvenidos a TalaTrivia API"}

# Swagger config
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="TalaTrivia API",
        version="1.0.0",
        description="API de trivias protegida con JWT",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"HTTPBearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
