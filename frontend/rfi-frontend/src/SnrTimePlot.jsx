import Plot from "react-plotly.js";

function SnrTimePlot({ time, snrLoss, threshold }) {
  if (!time || !snrLoss) return null;

  return (
    <Plot
      data={[
        {
          x: time,
          y: snrLoss,
          type: "scatter",
          mode: "lines",
          name: "SNR Loss (dB)",
        },
        {
          x: time,
          y: time.map(() => threshold),
          type: "scatter",
          mode: "lines",
          name: "ITU Threshold",
          line: { dash: "dash", color: "red" },
        },
      ]}
      layout={{
        title: "SNR Loss vs Time",
        xaxis: { title: "Time (s)" },
        yaxis: { title: "SNR Loss (dB)" },
        margin: { t: 50, l: 50, r: 20, b: 50 },
      }}
      style={{ width: "100%", height: "400px" }}
    />
  );
}

export default SnrTimePlot;
