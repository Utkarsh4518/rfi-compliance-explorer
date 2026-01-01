# RFI Compliance Explorer

An ITU-R aligned simulation and visualization tool for evaluating **radio-frequency interference (RFI)** impacts on space communication systems.

This project combines a **physics-based RFI engine**, **probabilistic ITU compliance checks**, and an **interactive web frontend** for dynamic and statistical analysis.

---

## ✨ Features

### 🔬 Backend (FastAPI + Python)
- Dynamic time-domain RFI simulation
- Aggregate Monte-Carlo interference analysis
- ITU-R compliance evaluation:
  - **SA.1157** (Deep-space services)
  - **SA.609** (Near-Earth services)
- Statistical exceedance and CCDF outputs
- Clean REST API with OpenAPI docs

### 📊 Frontend (React + Vite)
- Interactive parameter controls
- Time-domain **SNR loss vs time** plots
- **CCDF plots** for probabilistic analysis
- Side-by-side **Scenario A vs Scenario B** comparison
- Clear compliance verdict badges
- Dark, technical UI optimized for analysis

---

## 🧠 What This Tool Is For

This tool is designed for:
- RFI impact assessment
- ITU compliance studies
- Spectrum sharing analysis
- Academic research and simulation
- Engineering trade-off exploration

It is **not** a toy demo — results are derived from physically meaningful models and ITU-style evaluation logic.

---

## 🗂 Project Structure

