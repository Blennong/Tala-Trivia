# Tala Trivia API

API para un juego de Trivia construida con FastAPI y PostgreSQL.

## Tecnologías usadas 

Stack:
  -FastAPI (Python)
  -PostgreSQL
  
Puedes revisar las librerías en el archivo requirementss.txt

## Requisitos

- Docker y Docker Compose instalados

## Cómo levantar la aplicación con Docker

1. Clonar este repositorio

```bash
git clone https://github.com/tu_usuario/tala-trivia-api.git
cd tala-trivia-api

2. Crea un archivo .env a partir del archivo de ejemplo (.env.example)

3. Levanta los servicios con Docker:
docker-compose up --build
La API estará disponible en:
http://localhost:8000

## Documentación interactiva

FastAPI genera automáticamente una documentación interactiva que puedes visitar en:
http://localhost:8000/docs
