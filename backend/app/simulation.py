"""
simulation.py

Core simulation logic for the RFI Compliance Explorer.
This module contains NO plotting and NO printing.
It only computes and returns numerical results.

Aligned with:
- ITU-R S.1325-3 (aggregate interference, CI statistics)
- ITU-R SA.609 / SA.1157 (probabilistic SNR-loss interpretation)
"""

from typing import List, Dict

import numpy as np

# Import your existing RFI engine
from rfi.scenario import run_multi_entry_rfi_scenario
from rfi.itu_models import (
    compute_thermal_noise_dbw,
    free_space_path_loss_db,
    compute_off_axis_gain_s1528_db,
    compute_interference_power_dbw,
    compute_snr_with_interference_db,
    compute_time_fraction_exceeded,
)

# ---------------------------------------------------------------------
# Band configurations (taken directly from your notebook)
# ---------------------------------------------------------------------

DKM_GEO = 35786.0  # km

BAND_CONFIGS: Dict[str, Dict] = {
    "S-band": {
        "f_ghz": 2.25,
        "d_km": DKM_GEO,
        "EIRP_dbw": 26.0,
        "G_rx_db": 30.0,
        "theta_3db": 2.0,
        "T_sys_k": 320.0,
        "B_Hz": 1e6,
        "service": "SRS near-Earth (SA.609)",
    },
    "X-band": {
        "f_ghz": 8.00,
        "d_km": DKM_GEO,
        "EIRP_dbw": 30.0,
        "G_rx_db": 35.0,
        "theta_3db": 1.5,
        "T_sys_k": 250.0,
        "B_Hz": 1e6,
        "service": "SRS deep-space (SA.1157)",
    },
    "Ku-band": {
        "f_ghz": 14.25,
        "d_km": DKM_GEO,
        "EIRP_dbw": 45.0,
        "G_rx_db": 40.0,
        "theta_3db": 1.0,
        "T_sys_k": 600.0,
        "B_Hz": 5e6,
        "service": "FSS GEO gateway (S.1325)",
    },
    "K-band": {
        "f_ghz": 20.0,
        "d_km": DKM_GEO,
        "EIRP_dbw": 50.0,
        "G_rx_db": 45.0,
        "theta_3db": 0.8,
        "T_sys_k": 700.0,
        "B_Hz": 10e6,
        "service": "FSS high-frequency",
    },
    "Ka-band": {
        "f_ghz": 30.0,
        "d_km": DKM_GEO,
        "EIRP_dbw": 55.0,
        "G_rx_db": 50.0,
        "theta_3db": 0.6,
        "T_sys_k": 800.0,
        "B_Hz": 20e6,
        "service": "FSS / feeder link",
    },
}

# ---------------------------------------------------------------------
# Phase-2 Aggregate RFI Scenario
# ---------------------------------------------------------------------

def run_aggregate_scenario(
    band: str,
    interferers: List[Dict],
    time_samples: int = 10000,
) -> Dict:
    """
    Run an aggregate multi-interferer RFI scenario for a given band.

    Parameters
    ----------
    band : str
        One of ["S-band", "X-band", "Ku-band", "K-band", "Ka-band"]
    interferers : list of dict
        Each dict must contain:
        - EIRP_int_dbw
        - d_km
        - theta_off_axis_deg
        - sigma_db
        - duty_cycle
    time_samples : int
        Number of Monte Carlo samples

    Returns
    -------
    dict
        Key link metrics and exceedance probabilities
    """

    if band not in BAND_CONFIGS:
        raise ValueError(f"Unknown band: {band}")

    cfg = BAND_CONFIGS[band]

    band_params = {
        "f_ghz": cfg["f_ghz"],
        "d_km": cfg["d_km"],
        "EIRP_dbw": cfg["EIRP_dbw"],
        "G_rx_db": cfg["G_rx_db"],
        "theta_3db": cfg["theta_3db"],
    }

    # Delegate heavy lifting to your validated engine
    result = run_multi_entry_rfi_scenario(
        band_params=band_params,
        interferer_list=interferers,
        time_sim_samples=time_samples,
    )

    # Add explicit ITU-style exceedance metrics (standardised)
    snr_loss_samples = result["SNR_Loss_Samples_dB"]

    exceedance = {
        "P_SNR_loss_gt_1dB_pct": compute_time_fraction_exceeded(
            snr_loss_samples, threshold_db=1.0
        ),
        "P_SNR_loss_gt_3dB_pct": compute_time_fraction_exceeded(
            snr_loss_samples, threshold_db=3.0
        ),
        "P_SNR_loss_gt_6dB_pct": compute_time_fraction_exceeded(
            snr_loss_samples, threshold_db=6.0
        ),
    }

    return {
        "band": band,
        "service": cfg["service"],
        "baseline_snr_db": result["Baseline SNR (dB)"],
        "ci_aggregate_db": result["C/I_Aggregate (dB)"],
        "snr_with_interference_db": result["SNR with I_Agg (dB)"],
        "snr_loss_db": result["SNR Loss (dB)"],
        "exceedance": exceedance,
        "epfd_aggregate_dbw_m2_mhz": result["epfd_Aggregate (dBW/m2/MHz)"],
    }

# ---------------------------------------------------------------------
# Placeholder for Dynamic X-band (added next, not yet wired)
# ---------------------------------------------------------------------

def run_dynamic_xband_pass():
    """
    Dynamic X-band N-GSO pass (SA.1157-style).
    Implemented in next step once aggregate pipeline is stable.
    """
    raise NotImplementedError("Dynamic X-band scenario not yet implemented")
