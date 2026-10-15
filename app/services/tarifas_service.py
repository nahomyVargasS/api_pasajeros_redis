from app.db.mongo import db
from app.cache.redis import redis_cache
from app.config import settings

@redis_cache(ttl_seconds=settings.redis_ttl)
async def get_all_tarifas():
    return await db.tarifas.find().to_list()


async def get_tarifas_vigentes(codigo_ruta: str):
    # 1. Buscar la fecha de vigencia más reciente de esa ruta
    ultima = await db.tarifas.find_one(
        {"codigo_ruta": codigo_ruta},
        sort=[("fecha_vigencia", -1)],
    )
    if ultima is None:
        return []

    # 2. Traer todas las tarifas de la ruta con esa misma fecha
    return await db.tarifas.find(
        {"codigo_ruta": codigo_ruta, "fecha_vigencia": ultima["fecha_vigencia"]},
        {"_id": 0},
    ).to_list()


@redis_cache(ttl_seconds=settings.redis_ttl)
async def get_resumen_tarifas(codigo_ruta: str, anno: int):
    tarifas = await get_tarifas_vigentes(codigo_ruta)
    if not tarifas:
        return None

    # Promedio de pasajeros (regulares + adulto mayor) por ramal en el año
    pipeline = [
        {"$match": {"codigo_ruta": codigo_ruta, "anno": anno}},
        {
            "$group": {
                "_id": "$codigo_ramal",
                "promedio": {
                    "$avg": {
                        "$add": [
                            {"$ifNull": ["$pasajeros_regulares", 0]},
                            {"$ifNull": ["$pasajeros_adulto_mayor", 0]},
                        ]
                    }
                },
            }
        },
    ]
    ramales = await (await db.passengers.aggregate(pipeline)).to_list()

    promedio = (
        round(sum(r["promedio"] for r in ramales) / len(ramales), 2)
        if ramales
        else None
    )

    return {
        "codigo_ruta": codigo_ruta,
        "nombre_ruta": tarifas[0]["nombre_ruta"],
        "anno_pasajeros": anno,
        "tarifas_vigentes": tarifas,
        "ramales_considerados": len(ramales),
        "promedio_pasajeros": promedio,
    }