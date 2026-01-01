# backend/app/simulation.py

from typing import Dict, Any, List
from fastapi import HTTPException
from rfi.scenario import run_multi_entry_rfi_scenario
from backend.app.models import BandParams


# ---------------------------------
# Mapping from service to ITU rule
# ---------------------------------
ITU_RULES = {
    "deep-space": {
        "standard": "ITU-R SA.1157",
        "threshold_db": 6.0,
        "max_time_fraction_pct": 2.0,
    },
    "near-earth": {
        "standard": "ITU-R SA.609",
        "threshold_db": 1.0,
        "max_time_fraction_pct": 0.1,
    },
}


def evaluate_itu_compliance(
    snr_loss_samples_db,
    threshold_db: float,
    max_time_fraction_pct: float,
    standard_name: str,
):
    """
    Evaluate ITU-style probabilistic compliance:
    P(SNR loss > threshold) <= max_time_fraction
    """
    total = len(snr_loss_samples_db)
    exceeded = (snr_loss_samples_db > threshold_db).sum()
    observed_pct = 100.0 * exceeded / total

    return {
        "standard": standard_name,
        "threshold_db": threshold_db,
        "max_time_fraction_pct": max_time_fraction_pct,
        "observed_time_fraction_pct": round(observed_pct, 3),
        "status": "COMPLIANT"
        if observed_pct <= max_time_fraction_pct
        else "NON-COMPLIANT",
    }


def run_aggregate_simulation(
    band_params: BandParams,
    interferers: List[Dict[str, Any]],
    service_type: str,
    time_samples: int = 10000,
) -> Dict[str, Any]:
    """
    Backend-safe wrapper around the RFI engine.
    Returns JSON-serialisable results.
    """

    # -------------------------------
    # Run physics engine
    # -------------------------------
    try:
        result = run_multi_entry_rfi_scenario(
            band_params=band_params.model_dump(),
            interferer_list=interferers,
            time_sim_samples=time_samples,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # -------------------------------
    # ITU compliance evaluation
    # -------------------------------
    snr_loss_samples = result["SNR_Loss_Samples_dB"]

    sa1157_verdict = evaluate_itu_compliance(
        snr_loss_samples_db=snr_loss_samples,
        threshold_db=6.0,
        max_time_fraction_pct=2.0,
        standard_name="ITU-R SA.1157",
    )

    sa609_verdict = evaluate_itu_compliance(
        snr_loss_samples_db=snr_loss_samples,
        threshold_db=1.0,
        max_time_fraction_pct=0.1,
        standard_name="ITU-R SA.609",
    )

    result["compliance"] = {
        "SA.1157": sa1157_verdict,
        "SA.609": sa609_verdict,
    }

    # -------------------------------
    # Select authoritative verdict
    # -------------------------------
    if service_type not in ITU_RULES:
        result["overall_compliance"] = {
            "standard": "UNKNOWN",
            "status": "INVALID_SERVICE_TYPE",
        }
    elif service_type == "deep-space":
        result["overall_compliance"] = sa1157_verdict
    elif service_type == "near-earth":
        result["overall_compliance"] = sa609_verdict

    # -------------------------------
    # Make JSON-safe
    # -------------------------------
    if "SNR_Loss_Samples_dB" in result:
        result["SNR_Loss_Samples_dB"] = result[
            "SNR_Loss_Samples_dB"
        ].tolist()

    return result
