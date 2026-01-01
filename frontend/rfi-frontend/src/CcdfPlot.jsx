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

export default function CcdfPlot({ snrLossDb, ccdf }) {
  const data = snrLossDb.map((x, i) => ({
    snrLoss: x,
    probability: ccdf[i],
  }));

  return (
    <div style={{ marginTop: "30px" }}>
      <h2>CCDF: P(SNR Loss &gt; X)</h2>

      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="snrLoss"
            label={{ value: "SNR Loss (dB)", position: "insideBottom", offset: -5 }}
          />
          <YAxis
            scale="log"
            domain={[1e-4, 1]}
            label={{
              value: "Probability of Exceedance",
              angle: -90,
              position: "insideLeft",
            }}
          />
          <Tooltip />

          <Line
            type="monotone"
            dataKey="probability"
            stroke="#1e90ff"
            dot={false}
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
