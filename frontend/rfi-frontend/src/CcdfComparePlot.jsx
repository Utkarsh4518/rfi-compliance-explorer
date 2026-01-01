import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
  ResponsiveContainer,
} from "recharts";

export default function CcdfComparePlot({ ccdfA, ccdfB }) {
  const data = ccdfA.snr_loss_db.map((x, i) => ({
    snrLoss: x,
    A: ccdfA.ccdf[i],
    B: ccdfB.ccdf[i],
  }));

  return (
    <div style={{ marginTop: "30px" }}>
      <h3>CCDF Comparison (Scenario A vs B)</h3>

      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis label={{ value: "SNR Loss (dB)", position: "insideBottom" }} />
          <YAxis
            scale="log"
            domain={[1e-4, 1]}
            label={{
              value: "P(SNR Loss > X)",
              angle: -90,
              position: "insideLeft",
            }}
          />
          <Tooltip />

          <Line
            type="monotone"
            dataKey="A"
            stroke="#1f77b4"
            dot={false}
            name="Scenario A"
          />

          <Line
            type="monotone"
            dataKey="B"
            stroke="#d62728"
            dot={false}
            name="Scenario B"
          />

          {/* ITU thresholds */}
          <ReferenceLine x={1} stroke="green" strokeDasharray="5 5" />
          <ReferenceLine x={3} stroke="orange" strokeDasharray="5 5" />
          <ReferenceLine x={6} stroke="red" strokeDasharray="5 5" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
