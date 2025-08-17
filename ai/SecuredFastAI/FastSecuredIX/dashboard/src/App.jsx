import React, { useEffect, useState } from "react";
import axios from "axios";

export default function App() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch list of logs from backend
  useEffect(() => {
    async function fetchLogs() {
      try {
        const result = await axios.get("http://backend:2892/logs");
        setLogs(result.data.objects || []);
      } catch (err) {
        console.error("Failed to fetch logs: ", err);
      } finally {
        setLoading(false);
      }
    }
    fetchLogs();
  }, []);

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>📁 FastSecuredIX Log Dashboard</h1>

      {loading ? (
        <p>Loading logs...</p>
      ) : logs.length === 0 ? (
        <p>No logs were found. Try uploading some!</p>
      ) : (
        <ul>
          {logs.map((log) => (
            <li key={log}>{log}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
