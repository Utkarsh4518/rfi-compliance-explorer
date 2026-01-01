# 📡 RFI Compliance Explorer

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React-61DAFB?style=flat-square&logo=react&logoColor=black)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)

An **ITU-R aligned** simulation and visualization tool for evaluating **Radio-Frequency Interference (RFI)** impacts on space communication systems. 

This project combines a physics-based RFI engine, probabilistic ITU compliance checks, and an interactive web frontend for dynamic and statistical analysis.

---

## ✨ Features

### 🔬 Backend (FastAPI + Python)
* **Dynamic Simulation:** Time-domain RFI simulation based on orbital/signal geometry.
* **Monte-Carlo Analysis:** Aggregate interference analysis for statistical reliability.
* **ITU-R Compliance Engine:** Automated evaluation against:
    * **SA.1157** (Deep-space services)
    * **SA.609** (Near-Earth services)
* **Statistical Outputs:** Full CCDF (Complementary Cumulative Distribution Function) and exceedance data.
* **Clean REST API:** Fully documented via OpenAPI/Swagger.

### 📊 Frontend (React + Vite)
* **Real-time Visualization:** Interactive time-domain **SNR loss** and **CCDF plots**.
* **A/B Scenario Testing:** Side-by-side comparison for engineering trade-studies.
* **Compliance Dashboard:** High-visibility verdict badges (**COMPLIANT** / **NON-COMPLIANT**).
* **Analysis-First UI:** Dark-themed, technical interface optimized for data density.

---

## 🧠 What This Tool Is For

This tool is designed for spectrum engineers and researchers to perform:
* **RFI Impact Assessment:** Quantify degradation in link budgets.
* **ITU Compliance Studies:** Verify if a system meets international regulatory thresholds.
* **Spectrum Sharing Analysis:** Explore how primary and secondary services coexist.
* **Trade-off Exploration:** Test power levels, geometry, and policy thresholds.

> [!IMPORTANT]
> This is a professional-grade simulation tool. Results are derived from physically meaningful models and rigorous ITU-style evaluation logic.

---

## 🗂 Project Structure

```text
rfi-compliance-explorer/
├── backend/
│   └── app/
│       ├── main.py          # FastAPI entrypoint
│       ├── models.py        # Request / response schemas
│       └── simulation.py    # API-safe simulation wrappers
├── rfi/
│   └── scenario.py          # Core RFI physics engine
├── frontend/
│   └── rfi-frontend/
│       ├── src/             # React components & Plotting logic
│       └── vite.config.js
└── README.md
