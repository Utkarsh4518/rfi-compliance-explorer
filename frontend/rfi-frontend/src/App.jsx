import { useState } from "react";
import SnrTimeComparePlot from "./SnrTimeComparePlot";
import CcdfComparePlot from "./CcdfComparePlot";
import ComplianceBadge from "./ComplianceBadge";
import NumberInput from "./NumberInput";

/* -----------------------------
   Shared default inputs
----------------------------- */
const defaultInputs = {
  f_ghz: 8.0,
  d_km: 35786.0,
  EIRP_dbw: 30.0,
  G_rx_db: 35.0,
  theta_3db: 1.5,

  EIRP_int_dbw: 20.0,
  d0_km: 500.0,
  v_km_s: 0.2,
  theta0_deg: 1.0,
  omega_deg_s: 0.05,

  duration_s: 600,
  time_step_s: 1,
};

function App() {
  /* -------- Scenario A -------- */
  const [inputsA, setInputsA] = useState({ ...defaultInputs });
  const [dynamicA, setDynamicA] = useState(null);
  const [aggregateA, setAggregateA] = useState(null);

  /* -------- Scenario B -------- */
  const [inputsB, setInputsB] = useState({ ...defaultInputs });
  const [dynamicB, setDynamicB] = useState(null);
  const [aggregateB, setAggregateB] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  /* -----------------------------
     Backend helpers
  ----------------------------- */
  async function runDynamic(inputs, setResult) {
    setResult(null);

    const payload = {
      band_params: {
        f_ghz: inputs.f_ghz,
        d_km: inputs.d_km,
        EIRP_dbw: inputs.EIRP_dbw,
        G_rx_db: inputs.G_rx_db,
        theta_3db: inputs.theta_3db,
      },
      interferer: {
        EIRP_int_dbw: inputs.EIRP_int_dbw,
        d0_km: inputs.d0_km,
        v_km_s: inputs.v_km_s,
        theta0_deg: inputs.theta0_deg,
        omega_deg_s: inputs.omega_deg_s,
      },
      service_type: "deep-space",
      duration_s: inputs.duration_s,
      time_step_s: inputs.time_step_s,
    };

    const res = await fetch("http://127.0.0.1:8000/simulate/dynamic", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) throw new Error("Dynamic simulation failed");
    setResult(await res.json());
  }

  async function runAggregate(inputs, setResult) {
    setResult(null);

    const payload = {
      band_params: {
        f_ghz: inputs.f_ghz,
        d_km: inputs.d_km,
        EIRP_dbw: inputs.EIRP_dbw,
        G_rx_db: inputs.G_rx_db,
        theta_3db: inputs.theta_3db,
      },
      interferers: [
        {
          EIRP_int_dbw: inputs.EIRP_int_dbw,
          d_km: inputs.d0_km,
          theta_off_axis_deg: inputs.theta0_deg,
          sigma_db: 4,
          duty_cycle: 1,
        },
      ],
      service_type: "deep-space",
      time_samples: 10000,
    };

    const res = await fetch("http://127.0.0.1:8000/simulate/aggregate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) throw new Error("Aggregate simulation failed");
    setResult(await res.json());
  }

  async function runBoth() {
    setLoading(true);
    setError(null);

    setDynamicA(null);
    setDynamicB(null);
    setAggregateA(null);
    setAggregateB(null);

    try {
      await Promise.all([
        runDynamic(inputsA, setDynamicA),
        runDynamic(inputsB, setDynamicB),
        runAggregate(inputsA, setAggregateA),
        runAggregate(inputsB, setAggregateB),
      ]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ padding: "32px", fontFamily: "sans-serif" }}>
      <h1>RFI Compliance Explorer</h1>

      {/* ================= INPUTS ================= */}
      <div style={{ display: "flex", gap: "64px", marginBottom: "32px" }}>
        <div style={{ flex: 1 }}>
          <h2>Scenario A</h2>
          <NumberInput
            label="Interferer EIRP (dBW)"
            value={inputsA.EIRP_int_dbw}
            onChange={(v) => setInputsA({ ...inputsA, EIRP_int_dbw: v })}
          />
        </div>

        <div style={{ flex: 1 }}>
          <h2>Scenario B</h2>
          <NumberInput
            label="Interferer EIRP (dBW)"
            value={inputsB.EIRP_int_dbw}
            onChange={(v) => setInputsB({ ...inputsB, EIRP_int_dbw: v })}
          />
        </div>
      </div>

      <button
        onClick={runBoth}
        disabled={loading}
        style={{
          padding: "12px 24px",
          fontWeight: "bold",
          backgroundColor: "#222",
          color: "white",
          marginBottom: "40px",
        }}
      >
        {loading ? "Running…" : "Run Both Scenarios (Compare)"}
      </button>

      {error && <div style={{ color: "red" }}>{error}</div>}

      {/* ================= RESULTS ================= */}
      {dynamicA && dynamicB && aggregateA && aggregateB && (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1.3fr 1fr",
            gap: "72px",
            alignItems: "start",
          }}
        >
          {/* -------- LEFT: TIME DOMAIN -------- */}
          <div style={{ display: "flex", flexDirection: "column" }}>
            <h3>SNR Loss vs Time (Scenario A vs B)</h3>

            <div style={{ height: "520px", marginBottom: "48px" }}>
              <SnrTimeComparePlot
                time={dynamicA.time_s}
                snrA={dynamicA.snr_loss_db}
                snrB={dynamicB.snr_loss_db}
                threshold={dynamicA.overall_compliance.threshold_db}
              />
            </div>

            <ComplianceBadge verdict={dynamicA.overall_compliance} />
          </div>

          {/* -------- RIGHT: CCDF -------- */}
          <div style={{ display: "flex", flexDirection: "column" }}>
            <h3>CCDF Comparison (Scenario A vs B)</h3>

            <div style={{ height: "520px", marginBottom: "48px" }}>
              <CcdfComparePlot
                ccdfA={aggregateA.ccdf}
                ccdfB={aggregateB.ccdf}
              />
            </div>

            <ComplianceBadge verdict={aggregateB.overall_compliance} />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
