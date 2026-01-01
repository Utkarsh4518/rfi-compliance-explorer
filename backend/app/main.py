# backend/app/main.py

from fastapi import FastAPI
from app.models import AggregateSimulationRequest
from app.simulation import run_aggregate_simulation

app = FastAPI(
    title="RFI Compliance Explorer API",
    description="ITU-R aligned cross-band RFI simulation backend",
    version="1.0",
)


@app.post("/simulate/aggregate")
def simulate_aggregate(req: AggregateSimulationRequest):
    return run_aggregate_simulation(
        band_params=req.band_params,
        interferers=[i.dict() for i in req.interferers],
        time_samples=req.time_samples,
    )
