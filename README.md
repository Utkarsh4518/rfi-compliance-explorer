\# RFI Compliance Explorer

  

An ITU-R aligned simulation and visualization tool for evaluating \*\*radio-frequency interference (RFI)\*\* impacts on space communication systems.

  

This project combines a \*\*physics-based RFI engine\*\*, \*\*probabilistic ITU compliance checks\*\*, and an \*\*interactive web frontend\*\* for dynamic and statistical analysis.

  

\---

  

\## ✨ Features

  

\### 🔬 Backend (FastAPI + Python)

\- Dynamic time-domain RFI simulation

\- Aggregate Monte-Carlo interference analysis

\- ITU-R compliance evaluation:

  - \*\*SA.1157\*\* (Deep-space services)

  - \*\*SA.609\*\* (Near-Earth services)

\- Statistical exceedance and CCDF outputs

\- Clean REST API with OpenAPI docs

  

\### 📊 Frontend (React + Vite)

\- Interactive parameter controls

\- Time-domain \*\*SNR loss vs time\*\* plots

\- \*\*CCDF plots\*\* for probabilistic analysis

\- Side-by-side \*\*Scenario A vs Scenario B\*\* comparison

\- Clear compliance verdict badges

\- Dark, technical UI optimized for analysis

  

\---

  

\## 🧠 What This Tool Is For

  

This tool is designed for:

\- RFI impact assessment

\- ITU compliance studies

\- Spectrum sharing analysis

\- Academic research and simulation

\- Engineering trade-off exploration

  

It is \*\*not\*\* a toy demo — results are derived from physically meaningful models and ITU-style evaluation logic.

  

\---

  

\## 🗂 Project Structure

  

rfi-compliance-explorer/

│

├── backend/

│ └── app/

│ ├── main.py # FastAPI entrypoint

│ ├── models.py # Request / response models

│ └── simulation.py # API-safe simulation wrappers

│

├── rfi/

│ └── scenario.py # Core RFI physics engine

│

├── frontend/

│ └── rfi-frontend/

│ ├── src/

│ │ ├── App.jsx

│ │ ├── SnrTimePlot.jsx

│ │ ├── CcdfPlot.jsx

│ │ ├── Comparison plots

│ │ └── UI components

│ └── vite.config.js

│

└── README.md

  

  

  

\---

  

\## 🚀 Getting Started

  

\### 1️⃣ Backend Setup

  

Create and activate a virtual environment, then install dependencies:

  

\`\`\`bash

pip install fastapi uvicorn numpy

  

Run the backend:

  

uvicorn backend.app.main:app --reload

  

  

API will be available at:

  

http://127.0.0.1:8000

  

Docs: http://127.0.0.1:8000/docs

  

2️⃣ Frontend Setup

cd frontend/rfi-frontend

npm install

npm run dev

  

  

Frontend runs at:

  

http://localhost:5173

  

📡 API Endpoints

Dynamic Simulation

POST /simulate/dynamic

  

  

Time-varying interferer geometry

  

Returns SNR loss vs time + compliance verdict

  

Aggregate / Statistical Simulation

POST /simulate/aggregate

  

  

Monte-Carlo interference statistics

  

Returns CCDF and ITU exceedance results

  

📈 Outputs Explained

  

SNR Loss (dB): Degradation relative to noise-only baseline

  

CCDF: Probability that SNR loss exceeds a given threshold

  

Compliance Verdict:

  

COMPLIANT

  

NON-COMPLIANT

  

Based on ITU-R time-fraction limits

  

🧪 Scenario Comparison

  

The frontend supports:

  

Scenario A vs Scenario B

  

Shared geometry, varied parameters

  

Direct visual and compliance comparison

  

This is especially useful for:

  

Power trade studies

  

Geometry sensitivity

  

Policy threshold exploration

  

⚠️ Notes & Assumptions

  

Free-space propagation model

  

Atmospheric losses ignored (RFI-focused analysis)

  

Log-normal interference statistics

  

Simplified antenna off-axis model (ITU-style)

  

These choices are deliberate and documented.

  

🧭 Roadmap (Optional)

  

Possible future extensions:

  

Multiple simultaneous interferers (dynamic)

  

Geospatial visualization

  

Exportable reports (PDF / CSV)

  

Scenario presets

  

Deployment as hosted service

  

📜 License

  

This project is provided for research and educational use.

No warranty is implied. Use responsibly.

  

👤 Author

  

Developed by Utkarsh Maurya

RFI modeling, ITU compliance logic, and frontend architecture by design.

  

If you made it this far, congrats.

You’re not just running simulations — you’re running studies.

  

  

Can you put this all as markdown for my github read me file that I will paste directly in github
