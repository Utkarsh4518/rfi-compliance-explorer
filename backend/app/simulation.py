from .models import SimulationRequest, SimulationResult
from datetime import datetime

def run_simulation(req: SimulationRequest) -> SimulationResult:
    """Placeholder simulation logic.

    Current simple rule: compliant if power_dbm <= threshold_dbm (default 10 dBm).
    Returns a SimulationResult with details for debugging and UI display.
    """
    threshold_dbm = req.parameters.get("threshold_dbm", 10.0)
    compliant = req.power_dbm <= threshold_dbm
    details = {
        "frequency_mhz": req.frequency_mhz,
        "power_dbm": req.power_dbm,
        "threshold_dbm": threshold_dbm,
        "duration_s": req.duration_s,
    }
    return SimulationResult(compliant=compliant, details=details, timestamp=datetime.utcnow().isoformat() + "Z")
