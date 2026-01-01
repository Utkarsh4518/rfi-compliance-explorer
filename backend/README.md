# Backend (RFI Compliance Explorer)

This folder contains a minimal FastAPI-based backend skeleton for the RFI Compliance Explorer project.

Quick start (from repository root):

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r backend/requirements.txt
```

2. Run the server with uvicorn:

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

3. Endpoints:
- `GET /health` — simple health check
- `POST /simulate` — run a simulation; accepts `SimulationRequest` and returns `SimulationResult`

The code is intentionally minimal; expand simulation logic, data models, and add tests as needed.
