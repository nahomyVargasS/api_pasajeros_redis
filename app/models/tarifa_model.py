from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

# Ver nota abajo sobre este import
from app.models.ruta_model import ObjectIdStr


class TarifaModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[ObjectIdStr] = Field(default=None, alias="_id")
    codigo_ruta: str
    nombre_ruta: str
    nombre_fraccionamiento: str
    km_por_viaje: Optional[float] = None
    tarifa_regular: float
    tarifa_adulto_mayor: Optional[float] = None
    resolucion: str
    fecha_resolucion: Optional[datetime] = None
    gaceta: Optional[int] = None
    alcance: Optional[int] = None
    fecha_gaceta: Optional[datetime] = None
    fecha_vigencia: datetime
    expediente: Optional[str] = None
    operadores: Optional[str] = None
    cedulas: Optional[str] = None