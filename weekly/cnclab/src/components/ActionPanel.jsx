export default function ActionPanel({
  level,
  firewallEnabled,
  blockClient,
  blockAttacker,
  onAction
}) {
  const activeStyle = (color) => ({
    backgroundColor: color,
    color: "#000"
  });

  return (
    <div>
      <h2>ACTIONS</h2>
      <button onClick={() => onAction("openPage")}>Open Web Page</button>
      <button onClick={() => onAction("portScan")}>Run Port Scan</button>
      <button onClick={() => onAction("sniffTraffic")}>Sniff Traffic</button>

      {level === "2" && (
        <>
          <hr style={{ margin: "12px 0", border: "1px dashed #00FF41" }} />

          <button
            title="Toggle firewall on/off"
            style={firewallEnabled ? activeStyle("yellow") : undefined}
            onClick={() => onAction("enableFirewall")}
          >
            Enable Firewall
          </button>

          <button
            title="Drop requests from client to server"
            style={blockClient ? activeStyle("red") : undefined}
            onClick={() => onAction("blockClient")}
            disabled={!firewallEnabled}
          >
            Block Client Request
          </button>

          <button
            title="Drop attacker traffic (e.g., scans/attacks)"
            style={blockAttacker ? activeStyle("red") : undefined}
            onClick={() => onAction("blockAttacker")}
            disabled={!firewallEnabled}
          >
            Block Attacker
          </button>

          <button
            title="Turn off all firewall filtering"
            onClick={() => onAction("disableFirewall")}
          >
            Disable Firewall
          </button>
        </>
      )}
    </div>
  );
}
// --- IGNORE ---