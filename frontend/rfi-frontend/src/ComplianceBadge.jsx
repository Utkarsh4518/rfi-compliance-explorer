function ComplianceBadge({ verdict }) {
  if (!verdict) return null;

  const isCompliant = verdict.status === "COMPLIANT";

  const style = {
    padding: "20px",
    marginTop: "20px",
    fontSize: "24px",
    fontWeight: "bold",
    textAlign: "center",
    color: "white",
    backgroundColor: isCompliant ? "green" : "red",
    borderRadius: "8px",
  };

  return (
    <div style={style}>
      {verdict.standard}: {verdict.status}
      <div style={{ fontSize: "16px", marginTop: "8px" }}>
        Observed: {verdict.observed_time_fraction_pct}% &nbsp;|&nbsp;
        Allowed: {verdict.max_time_fraction_pct}%
      </div>
    </div>
  );
}

export default ComplianceBadge;
