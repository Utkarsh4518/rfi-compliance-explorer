# rfi/itu_models.py (FINAL, COMPLETE VERSION)

import numpy as np
from typing import List

# --- 1. Link Budget & Noise Helpers (P.525) ---

def compute_thermal_noise_dbw(T_sys_k, BW_hz):
    """Computes Thermal Noise Power (N = kTB) in dBW."""
    k_boltzmann = 1.380649e-23
    N_watts = k_boltzmann * T_sys_k * BW_hz
    return 10 * np.log10(N_watts)

def free_space_path_loss_db(f_ghz: float, d_km: float) -> float:
    """ITU-R P.525: Free-Space Path Loss (L_fs) formula (32.45 + 20logf_MHz + 20logd_km)."""
    f_mhz = f_ghz * 1000.0
    return 32.45 + 20 * np.log10(f_mhz) + 20 * np.log10(d_km)

# --- 2. S.1528 Antenna Model ---

def compute_off_axis_gain_s1528_db(g_max: float, theta_deg: float, theta_3db: float) -> float:
    """Simplified ITU-R S.1528 satellite antenna pattern for off-axis discrimination."""
    theta_edge = 2.5 * theta_3db
    
    if theta_deg < theta_edge:
        # G(theta) ≈ G_max - 12 * (theta / theta_3db)^2
        g_off_axis = g_max - 12 * (theta_deg / theta_3db)**2
    else:
        # G(theta) ≈ G_max - 30 (Side-lobe floor)
        g_off_axis = g_max - 30.0 
    
    return g_off_axis

# --- 3. S.1325 Interference & SNR Functions (Single and Aggregate) ---

def compute_interference_power_dbw(
    eirp_int_dbw: float, 
    l_fs_int_db: float, 
    l_atm_db: float, 
    g_rx_off_axis_db: float, 
    l_mise_db: float = 0.0
) -> float:
    """ITU-R S.1325-3 Section 3: Interference power calculation."""
    return eirp_int_dbw - l_fs_int_db - l_atm_db + g_rx_off_axis_db - l_mise_db

def compute_aggregate_interference_dbw(i_powers_dbw: List[float]) -> float:
    """
    Computes aggregate interference power (Sum(I)) by summing linear powers (Watts), 
    as required by ITU-R S.1325 (Phase 2 Aggregate).
    """
    i_lin_list = [10**(i_dbw / 10) for i_dbw in i_powers_dbw]
    i_agg_lin = sum(i_lin_list)
    if i_agg_lin <= 1e-30: 
        return -300.0 
    return 10 * np.log10(i_agg_lin)

def compute_carrier_to_interference_db(c_dbw: float, i_dbw: float) -> float:
    """ITU-R S.1325-3 Section 4.1: C/I (can be single-entry or aggregate)."""
    return c_dbw - i_dbw

def compute_snr_with_interference_db(c_dbw: float, n_dbw: float, i_dbw: float) -> float:
    """ITU-R S.1325-3 Section 4.3: Link performance with interference (SNR = C / (N + I) linear sum)."""
    c_lin = 10**(c_dbw / 10)
    n_lin = 10**(n_dbw / 10)
    i_lin = 10**(i_dbw / 10)
    snr_lin = c_lin / (n_lin + i_lin)
    return 10 * np.log10(snr_lin)

# --- 4. Equivalent Power Flux Density (epfd) (S.1325 Annex 2) ---

def compute_epfd_dbw_m2_mhz(
    eirp_int_dbw: float, 
    g_rx_off_axis_db: float, 
    l_fs_int_db: float,
    d_km: float,
    bandwidth_mhz: float
) -> float:
    """
    Computes Equivalent Power Flux Density (epfd) in dBW/m²/MHz. 
    (Phase 2 Aggregate/epfd requirement).
    """
    d_m = d_km * 1000.0
    area_term_db = 10 * np.log10(4 * np.pi * d_m**2)

    pfd_dbw_m2 = (
        eirp_int_dbw  
        - l_fs_int_db 
        + g_rx_off_axis_db
        - area_term_db # Area term adjustment
    )
    return pfd_dbw_m2 - 10 * np.log10(bandwidth_mhz) 

# --- 5. SA.1157 Time-Varying Metrics ---

def compute_time_fraction_exceeded(
    data_samples_db: np.ndarray, 
    threshold_db: float
) -> float:
    """ITU-R SA.1157 Section 3: Percentage of time interference/SNR loss exceeds a threshold."""
    count_exceeded = np.sum(data_samples_db > threshold_db)
    total_samples = len(data_samples_db)
    return (count_exceeded / total_samples) * 100.0

def generate_log_normal_interference_samples_dbw(
    mean_dbw: float, 
    std_dev_db: float, 
    num_samples: int,
    duty_cycle: float = 1.0
) -> np.ndarray:
    """ITU-R SA.1157 Section 4.2: Interference modeled as Gaussian in dB (log-normal in linear)."""
    i_gaussian_dbw = np.random.normal(loc=mean_dbw, scale=std_dev_db, size=num_samples)
    
    if duty_cycle < 1.0:
        num_on = int(num_samples * duty_cycle)
        i_off_dbw = np.full(num_samples, -300.0) 
        on_indices = np.random.choice(num_samples, size=num_on, replace=False)
        i_off_dbw[on_indices] = i_gaussian_dbw[on_indices]
        return i_off_dbw
        
    return i_gaussian_dbw

# --- 6. Geometric Simulation Helper (Phase 3 Dynamic Geometry) ---

def generate_geometric_sweep(
    max_theta_deg: float, 
    min_theta_deg: float, 
    num_steps: int = 100
) -> np.ndarray:
    """
    Generates a time-series of off-axis angles (theta) simulating a pass-by 
    where the angle sweeps from max_theta, down to min_theta (closest approach), and back.
    """
    t = np.linspace(-1, 1, num_steps)
    sweep = 0.5 * (1 + np.cos(t * np.pi)) 
    theta_range = max_theta_deg - min_theta_deg
    angles = (sweep * theta_range) + min_theta_deg
    
    return angles