from pydantic import BaseModel
from typing import List, Literal


class BandParams(BaseModel):
    f_ghz: float
    d_km: float
    EIRP_dbw: float
    G_rx_db: float
    theta_3db: float


class Interferer(BaseModel):
    EIRP_int_dbw: float
    d_km: float
    theta_off_axis_deg: float
    sigma_db: float = 4.0
    duty_cycle: float = 1.0


class AggregateSimulationRequest(BaseModel):
    band_params: BandParams
    interferers: List[Interferer]
    service_type: Literal["deep-space", "near-earth"]
    time_samples: int = 10000
