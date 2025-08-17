function colorFor(action) {
  if (!action) return "#00FF41";
  if (action === "openPage") return "#7CFC00";
  if (action === "portScan" || action === "sniffTraffic") return "cyan";
  if (action === "enableFirewall") return "yellow";
  if (action === "blockTraffic") return "red";
  if (action === "disableFirewall") return "#00FF41";
  return "#00FF41";
}

export default function Topology({
  level,
  firewallEnabled,
  firewallBlocking,
  blockAttacker,
  lastAction
}) {
  const fwColor = !firewallEnabled
    ? "#00FF41"
    : firewallBlocking
    ? "red"
    : "yellow";

  const pulseColor = colorFor(lastAction);
  const animClass = lastAction ? "pulse" : "";

  return (
    <div style={{ fontFamily: "Courier New", whiteSpace: "pre" }}>
      <h2>NETWORK TOPOLOGY</h2>
      {level === "1" ? (
        <div>
          <span className={animClass} style={{ color: pulseColor }}>
            [ CLIENT ]
          </span>
          {" <---> (network) <---> "}
          <span className={animClass} style={{ color: pulseColor }}>
            [ WEB SERVER ]
          </span>
          <br />
          {"                        |"}
          <br />
          {"                +-------+--------+"}
          <br />
          {"                |                |"}
          <br />
          {"            [ SNIFFER ]      "}
          <span style={{ color: blockAttacker ? "red" : "#00FF41" }}>
            [ ATTACKER ]
          </span>
        </div>
      ) : (
        <div>
          <span className={animClass} style={{ color: pulseColor }}>
            [ CLIENT ]
          </span>
          {" <---> "}
          <span style={{ color: fwColor }}>[ FIREWALL ]</span>
          {" <---> (network) <---> "}
          <span className={animClass} style={{ color: pulseColor }}>
            [ WEB SERVER ]
          </span>
          <br />
          {"                                     |"}
          <br />
          {"                             +-------+--------+"}
          <br />
          {"                             |                |"}
          <br />
          {"                         [ SNIFFER ]      "}
          <span style={{ color: blockAttacker ? "red" : "#00FF41" }}>
            [ ATTACKER ]
          </span>
        </div>
      )}
    </div>
  );
}
// src/engine/simulator.js