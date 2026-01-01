function NumberInput({ label, value, onChange, step = 0.1 }) {
  return (
    <div style={{ marginBottom: "10px" }}>
      <label>
        {label}:{" "}
        <input
          type="number"
          value={value}
          step={step}
          onChange={(e) => onChange(parseFloat(e.target.value))}
        />
      </label>
    </div>
  );
}

export default NumberInput;
