# rfi/scenario.py

import numpy as np
from typing import Dict, Any, List

from rfi.itu_models import (
    compute_thermal_noise_dbw,
    free_space_path_loss_db,
    compute_interference_power_dbw,
    compute_aggregate_interference_dbw,
    compute_epfd_dbw_m2_mhz,
    compute_carrier_to_interference_db,
    compute_snr_with_interference_db,
    compute_off_axis_gain_s1528_db,
    generate_log_normal_interference_samples_dbw,
    compute_time_fraction_exceeded,
)

# ---------------------------------------------------------------------
# Default constants (kept simple and explicit)
# ---------------------------------------------------------------------

T_SYS_K = 250.0          # System noise temperature [K]
BW_HZ = 1e6              # Receiver bandwidth [Hz]
L_ATM_DB_NOMINAL = 0.0   # Atmospheric loss ignored (RFI focus)

# ---------------------------------------------------------------------
# Main scenario engine
# ---------------------------------------------------------------------

def run_multi_entry_rfi_scenario(
    band_params: Dict[str, Any],
    interferer_list: List[Dict[str, Any]],
    time_sim_samples: int = 1000,
) -> Dict[str, Any]:
    """
    Runs an ITU-R S.1325-compliant aggregate RFI scenario with
    SA.1157-style statistical evaluation.

    Parameters
    ----------
    band_params : dict
        Must contain:
        - f_ghz
        - d_km
        - EIRP_dbw
        - G_rx_db
        - theta_3db

    interferer_list : list of dict
        Each interferer must contain:
        - EIRP_int_dbw
        - d_km
        - theta_off_axis_deg
        Optional:
        - sigma_db
        - duty_cycle

    time_sim_samples : int
        Number of Monte Carlo samples for statistical analysis

    Returns
    -------
    dict
        Deterministic link metrics + statistical exceedance results
    """

    # -------------------------------------------------------------
    # 1. Baseline carrier and noise
    # -------------------------------------------------------------

    f_ghz = band_params["f_ghz"]
    d_km = band_params["d_km"]

    N_dbw = compute_thermal_noise_dbw(T_SYS_K, BW_HZ)
    L_fs_db = free_space_path_loss_db(f_ghz, d_km)

    C_dbw = (
        band_params["EIRP_dbw"]
        - L_fs_db
        - L_ATM_DB_NOMINAL
        + band_params["G_rx_db"]
    )

    baseline_snr_db = C_dbw - N_dbw

    # -------------------------------------------------------------
    # 2. Deterministic aggregate interference (S.1325)
    # -------------------------------------------------------------

    I_single_powers_dbw = []
    epfd_single_values_db = []

    for i_params in interferer_list:
        L_fs_int_db = free_space_path_loss_db(f_ghz, i_params["d_km"])

        g_rx_off_axis_db = compute_off_axis_gain_s1528_db(
            g_max=band_params["G_rx_db"],
            theta_deg=i_params["theta_off_axis_deg"],
            theta_3db=band_params["theta_3db"],
        )

        I_single_dbw = compute_interference_power_dbw(
            eirp_int_dbw=i_params["EIRP_int_dbw"],
            l_fs_int_db=L_fs_int_db,
            l_atm_db=L_ATM_DB_NOMINAL,
            g_rx_off_axis_db=g_rx_off_axis_db,
        )
        I_single_powers_dbw.append(I_single_dbw)

        epfd_single_db = compute_epfd_dbw_m2_mhz(
            eirp_int_dbw=i_params["EIRP_int_dbw"],
            g_rx_off_axis_db=g_rx_off_axis_db,
            l_fs_int_db=L_fs_int_db,
            d_km=i_params["d_km"],
            bandwidth_mhz=BW_HZ / 1e6,
        )
        epfd_single_values_db.append(epfd_single_db)

    I_aggregate_dbw = compute_aggregate_interference_dbw(I_single_powers_dbw)
    epfd_aggregate_db = compute_aggregate_interference_dbw(epfd_single_values_db)

    C_I_db = compute_carrier_to_interference_db(C_dbw, I_aggregate_dbw)
    SNR_with_I_db = compute_snr_with_interference_db(C_dbw, N_dbw, I_aggregate_dbw)
    SNR_loss_db = baseline_snr_db - SNR_with_I_db

    # -------------------------------------------------------------
    # 3. Statistical analysis (SA.1157-style)
    # -------------------------------------------------------------

    # Use aggregate I as the mean of the log-normal process
    sigma_db = interferer_list[0].get("sigma_db", 4.0)
    duty_cycle = interferer_list[0].get("duty_cycle", 1.0)

    i_samples_dbw = generate_log_normal_interference_samples_dbw(
        mean_dbw=I_aggregate_dbw,
        std_dev_db=sigma_db,
        num_samples=time_sim_samples,
        duty_cycle=duty_cycle,
    )

    snr_with_i_samples_db = np.array([
        compute_snr_with_interference_db(C_dbw, N_dbw, i_dbw)
        for i_dbw in i_samples_dbw
    ])

    snr_loss_samples_db = baseline_snr_db - snr_with_i_samples_db

    # -------------------------------------------------------------
    # 4. Assemble results
    # -------------------------------------------------------------

    results = {
        "Baseline SNR (dB)": baseline_snr_db,
        "I_Aggregate (dBW)": I_aggregate_dbw,
        "C/I_Aggregate (dB)": C_I_db,
        "SNR with I_Agg (dB)": SNR_with_I_db,
        "SNR Loss (dB)": SNR_loss_db,
        "epfd_Aggregate (dBW/m2/MHz)": epfd_aggregate_db,

        # Statistical outputs
        "P(SNR Loss > 1 dB) (%)": compute_time_fraction_exceeded(
            snr_loss_samples_db, 1.0
        ),
        "P(SNR Loss > 3 dB) (%)": compute_time_fraction_exceeded(
            snr_loss_samples_db, 3.0
        ),
        "P(SNR Loss > 6 dB) (%)": compute_time_fraction_exceeded(
            snr_loss_samples_db, 6.0
        ),

        # IMPORTANT: expose full sample set for CCDFs & web plots
        "SNR_Loss_Samples_dB": snr_loss_samples_db,
    }

    return results

def run_dynamic_rfi_scenario(
    band_params: Dict[str, Any],
    interferer_params: Dict[str, Any],
    time_s: np.ndarray,
):
    """
    Time-varying RFI scenario.
    Returns SNR loss as a function of time.
    """

    f_ghz = band_params["f_ghz"]
    d_km = band_params["d_km"]
    G_rx = band_params["G_rx_db"]
    theta_3db = band_params["theta_3db"]

    # Baseline carrier and noise
    N_dbw = compute_thermal_noise_dbw(T_SYS_K, BW_HZ)
    L_fs_db = free_space_path_loss_db(f_ghz, d_km)

    C_dbw = (
        band_params["EIRP_dbw"]
        - L_fs_db
        - L_ATM_DB_NOMINAL
        + G_rx
    )

    baseline_snr_db = C_dbw - N_dbw

    snr_loss_time = []

    for t in time_s:
        theta_t = interferer_params["theta0_deg"] + interferer_params["omega_deg_s"] * t
        d_t = interferer_params["d0_km"] + interferer_params["v_km_s"] * t

        L_fs_int = free_space_path_loss_db(f_ghz, d_t)

        G_rx_off = compute_off_axis_gain_s1528_db(
            g_max=G_rx,
            theta_deg=theta_t,
            theta_3db=theta_3db,
        )

        I_dbw = compute_interference_power_dbw(
            eirp_int_dbw=interferer_params["EIRP_int_dbw"],
            l_fs_int_db=L_fs_int,
            l_atm_db=0.0,
            g_rx_off_axis_db=G_rx_off,
        )

        snr_with_i = compute_snr_with_interference_db(
            C_dbw, N_dbw, I_dbw
        )

        snr_loss_time.append(baseline_snr_db - snr_with_i)

    return np.array(snr_loss_time)
