# backend/app/simulation.py

from typing import Dict, Any, List
from rfi.scenario import run_multi_entry_rfi_scenario


def run_aggregate_simulation(
    band_params: Dict[str, Any],
    interferers: List[Dict[str, Any]],
    time_samples: int = 10000,
) -> Dict[str, Any]:
    """
    Backend-safe wrapper around the RFI engine.
    Returns JSON-serialisable results.
    """

    result = run_multi_entry_rfi_scenario(
        band_params=band_params,
        interferer_list=interferers,
        time_sim_samples=time_samples,
    )

    # Convert numpy arrays to lists (FastAPI requirement)
    if "SNR_Loss_Samples_dB" in result:
        result["SNR_Loss_Samples_dB"] = result["SNR_Loss_Samples_dB"].tolist()

    return result
