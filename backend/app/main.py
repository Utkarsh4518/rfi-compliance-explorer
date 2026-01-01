from fastapi import FastAPI
from .models import SimulationRequest, SimulationResult
from .simulation import run_simulation

app = FastAPI(title="RFI Compliance Explorer - Backend")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/simulate", response_model=SimulationResult)
async def simulate(req: SimulationRequest):
    """Run a compliance simulation based on the request payload."""
    result = run_simulation(req)
    return result
