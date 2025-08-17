// helper for coloring log lines
function getColor(line) {
  if (line.includes("200 OK") || line.includes("ALLOW")) return "#00FF41";
  if (line.includes("BLOCKED") || line.includes("DENY")) return "red";
  if (line.includes("Firewall")) return "yellow";
  if (line.includes("nmap") || line.includes("Sniffer")) return "cyan";
  return "#FFFFFF";
}

// new helper to color the top info message
function colorForInfo(text) {
  const lower = text.toLowerCase();
  if (lower.includes("blocked") || lower.includes("drop")) return "red";
  if (lower.includes("allow") || lower.includes("reached")) return "#00FF41";
  if (lower.includes("enabled")) return "yellow";
  if (lower.includes("scan") || lower.includes("sniffer")) return "cyan";
  return "#FFFFFF";
}

export default function InfoPane({ info, logs, onClear }) {
  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h2>INFO PANE</h2>
        <span
          title="Clear Logs"
          style={{ cursor: "pointer", fontSize: "20px" }}
          onClick={onClear}
        >
          🗑️
        </span>
      </div>
      <p style={{ color: colorForInfo(info) }}>{info}</p>
      <h3>Logs</h3>
      <div style={{ background: "#222", height: "75vh", overflow: "auto", padding: "4px" }}>
        {logs.map((l, i) => (
          <pre
            key={i}
            style={{ margin: 0, color: getColor(l), fontWeight: l.includes("BLOCKED") ? "bold" : "normal" }}
          >
            {l}
          </pre>
        ))}
      </div>
    </div>
  );
}
