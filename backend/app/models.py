# backend/app/models.py

from pydantic import BaseModel
from typing import List


class Interferer(BaseModel):
    EIRP_int_dbw: float
    d_km: float
    theta_off_axis_deg: float
    sigma_db: float = 4.0
    duty_cycle: float = 1.0


class AggregateSimulationRequest(BaseModel):
    band_params: dict
    interferers: List[Interferer]
    time_samples: int = 10000
