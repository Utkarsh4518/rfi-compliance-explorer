from typing import Dict, Any, List
import numpy as np
from fastapi import HTTPException

from backend.app.models import BandParams
from rfi.scenario import (
    run_multi_entry_rfi_scenario,
    run_dynamic_rfi_scenario,
)

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

def compute_ccdf(samples_db, num_points=200):
    """
    Compute CCDF: P(SNR loss > x)
    Returns arrays suitable for plotting.
    """
    samples = np.array(samples_db)
    x_vals = np.linspace(
        samples.min(),
        samples.max(),
        num_points
    )

    ccdf = [
        np.mean(samples > x)
        for x in x_vals
    ]

    return {
        "snr_loss_db": x_vals.tolist(),
        "ccdf": ccdf,
    }


def evaluate_itu_compliance(
    snr_loss_samples_db,
    threshold_db: float,
    max_time_fraction_pct: float,
    standard_name: str,
):
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


# ============================================================
# OPTION 2: Dynamic scenario wrapper
# ============================================================

def run_dynamic_simulation(
    band_params: BandParams,
    interferer: Dict[str, Any],
    service_type: str,
    duration_s: float,
    time_step_s: float,
) -> Dict[str, Any]:

    time_s = np.arange(0.0, duration_s, time_step_s)

    try:
        snr_loss_time = run_dynamic_rfi_scenario(
            band_params=band_params.model_dump(),
            interferer_params=interferer,
            time_s=time_s,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    rule = ITU_RULES[service_type]

    verdict = evaluate_itu_compliance(
        snr_loss_samples_db=snr_loss_time,
        threshold_db=rule["threshold_db"],
        max_time_fraction_pct=rule["max_time_fraction_pct"],
        standard_name=rule["standard"],
    )

    return {
        "time_s": time_s.tolist(),
        "snr_loss_db": snr_loss_time.tolist(),
        "overall_compliance": verdict,
    }


# ============================================================
# OPTION 1: Static aggregate scenario (unchanged)
# ============================================================

def run_aggregate_simulation(
    band_params: BandParams,
    interferers: List[Dict[str, Any]],
    service_type: str,
    time_samples: int = 10000,
) -> Dict[str, Any]:

    try:
        result = run_multi_entry_rfi_scenario(
            band_params=band_params.model_dump(),
            interferer_list=interferers,
            time_sim_samples=time_samples,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    snr_loss_samples = result["SNR_Loss_Samples_dB"]

    ccdf_data = compute_ccdf(snr_loss_samples)

    result["ccdf"] = ccdf_data


    sa1157_verdict = evaluate_itu_compliance(
        snr_loss_samples, 6.0, 2.0, "ITU-R SA.1157"
    )
    sa609_verdict = evaluate_itu_compliance(
        snr_loss_samples, 1.0, 0.1, "ITU-R SA.609"
    )

    result["compliance"] = {
        "SA.1157": sa1157_verdict,
        "SA.609": sa609_verdict,
    }

    result["overall_compliance"] = (
        sa1157_verdict if service_type == "deep-space" else sa609_verdict
    )

    result["SNR_Loss_Samples_dB"] = result["SNR_Loss_Samples_dB"].tolist()

    return result
