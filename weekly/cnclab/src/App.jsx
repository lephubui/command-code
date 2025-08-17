import React, { useState } from "react";
import "./App.css";
import Topology from "./components/Topology.jsx";
import ActionPanel from "./components/ActionPanel.jsx";
import InfoPane from "./components/InfoPane.jsx";
import { simulate } from "./engine/simulator.js";

export default function App() {
  const [level, setLevel] = useState("1");
  const [logs, setLogs] = useState([]);
  const [info, setInfo] = useState("💻 INIT: ready for action...");
  const [firewallEnabled, setFirewallEnabled] = useState(false);
  const [blockClient, setBlockClient] = useState(false);
  const [blockAttacker, setBlockAttacker] = useState(false);
  const [lastAction, setLastAction] = useState(null);

  const handleAction = (action) => {
    setLastAction(action);
    const { newLogs, newInfo } = simulate(action);

    if (action === "enableFirewall") {
      setFirewallEnabled(!firewallEnabled);
      if (firewallEnabled) {
        // turning off firewall should turn off rules
        setBlockClient(false);
        setBlockAttacker(false);
      }
    }
    if (action === "blockClient") {
      setBlockClient(!blockClient);
    }
    if (action === "blockAttacker") {
      setBlockAttacker(!blockAttacker);
    }
    if (action === "disableFirewall") {
      setFirewallEnabled(false);
      setBlockClient(false);
      setBlockAttacker(false);
    }

    setLogs((prev) => [...prev, ...newLogs]);
    setInfo(newInfo);
  };

  const changeLevel = (e) => {
    setLevel(e.target.value);
    setLogs([]);
    setInfo("💻 INIT: ready for action...");
    setFirewallEnabled(false);
    setBlockClient(false);
    setBlockAttacker(false);
    setLastAction(null);
  };

  return (
    <div>
      <div style={{ textAlign: "center", padding: "8px" }}>
        <select
          value={level}
          onChange={changeLevel}
          style={{
            backgroundColor: "#111",
            color: "#00FF41",
            border: "1px solid #00FF41",
            fontFamily: "Courier New",
            padding: "4px 8px"
          }}
        >
          <option value="1">Level 1 – Basic Traffic</option>
          <option value="2">Level 2 – Firewall</option>
        </select>
      </div>

      <div style={{ display: "flex", height: "94vh" }}>
        <div className="panel" style={{ flex: 2 }}>
          <Topology
            level={level}
            firewallEnabled={firewallEnabled}
            firewallBlocking={blockClient}
            blockAttacker={blockAttacker}
            lastAction={lastAction}
          />
        </div>
        <div className="panel" style={{ flex: 1 }}>
          <ActionPanel
            level={level}
            firewallEnabled={firewallEnabled}
            blockClient={blockClient}
            blockAttacker={blockAttacker}
            onAction={handleAction}
          />
        </div>
        <div className="panel" style={{ flex: 3 }}>
          <InfoPane info={info} logs={logs} onClear={() => {
            setLogs([]);
            setInfo("💻 INIT: ready for action...");
          }} />
        </div>
      </div>
    </div>
  );
}
// --- IGNORE ---