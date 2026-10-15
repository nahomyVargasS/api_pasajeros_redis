from fastapi import APIRouter, HTTPException

from app.models.tarifa_model import TarifaModel
from app.services.tarifas_service import (
    get_all_tarifas,
    get_resumen_tarifas,
    get_tarifas_vigentes,
)
router = APIRouter(prefix="/tarifas", tags=["Tarifas"])


@router.get("/", response_model=list[TarifaModel])
async def listar_tarifas():
    return await get_all_tarifas()

@router.get("/{codigo_ruta}/resumen")
async def resumen_tarifas(codigo_ruta: str, anno: int = 2024):
    resumen = await get_resumen_tarifas(codigo_ruta, anno)
    if resumen is None:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    return resumen


@router.get("/{codigo_ruta}")
async def tarifas_por_ruta(codigo_ruta: str):
    tarifas = await get_tarifas_vigentes(codigo_ruta)
    if not tarifas:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    return tarifas