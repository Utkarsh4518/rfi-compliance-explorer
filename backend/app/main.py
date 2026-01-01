from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import (
    AggregateSimulationRequest,
    DynamicSimulationRequest,
)
from .simulation import (
    run_aggregate_simulation,
    run_dynamic_simulation,
)

app = FastAPI(
    title="RFI Compliance Explorer API",
    description="ITU-R aligned cross-band RFI simulation backend",
    version="1.0",
)

# -------------------------------------------------
# CORS (required for frontend at localhost:5173)
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Aggregate / Monte Carlo / CCDF (OPTION B)
# -------------------------------------------------
@app.post("/simulate/aggregate")
def simulate_aggregate(req: AggregateSimulationRequest):
    return run_aggregate_simulation(
        band_params=req.band_params,
        interferers=[i.dict() for i in req.interferers],
        service_type=req.service_type,
        time_samples=req.time_samples,
    )

# -------------------------------------------------
# Dynamic / Time-domain (OPTION A)
# -------------------------------------------------
@app.post("/simulate/dynamic")
def simulate_dynamic(req: DynamicSimulationRequest):
    return run_dynamic_simulation(
        band_params=req.band_params,
        interferer=req.interferer,
        service_type=req.service_type,
        duration_s=req.duration_s,
        time_step_s=req.time_step_s,
    )
