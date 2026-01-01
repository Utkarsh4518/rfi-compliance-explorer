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

export default function SnrTimeComparePlot({
  time,
  snrA,
  snrB,
  threshold,
}) {
  const data = time.map((t, i) => ({
    time: t,
    A: snrA[i],
    B: snrB[i],
  }));

  return (
    <div style={{ marginTop: "30px" }}>
      <h3>SNR Loss vs Time (Scenario A vs B)</h3>

      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" label={{ value: "Time (s)", position: "insideBottom" }} />
          <YAxis label={{ value: "SNR Loss (dB)", angle: -90, position: "insideLeft" }} />
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

          <ReferenceLine
            y={threshold}
            stroke="black"
            strokeDasharray="5 5"
            label="ITU Threshold"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
