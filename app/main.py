from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.cache.redis import check_redis_connection, redis_client
from app.db.mongo import client
from app.routes import cache, pasajeros, tarifas


@asynccontextmanager
async def lifespan(app: FastAPI):
    await client.admin.command("ping")
    print("MongoDB: conexión OK")
    await check_redis_connection()
    yield
    await redis_client.aclose()
    await client.close()


app = FastAPI(
    title="API de Pasajeros",
    description="Consulta de rutas de transporte público",
    version="2.0.0",
    lifespan=lifespan,
)

app.include_router(pasajeros.router, prefix="/api")
app.include_router(cache.router, prefix="/api")
app.include_router(tarifas.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Pasajeros Movilizados"}
