from pydantic import BaseModel
from typing import Dict, Any

class SimulationRequest(BaseModel):
    frequency_mhz: float
    power_dbm: float
    duration_s: float = 1.0
    parameters: Dict[str, Any] = {}

class SimulationResult(BaseModel):
    compliant: bool
    details: Dict[str, Any]
    timestamp: str
