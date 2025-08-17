import React from "react";
import ReactDOM from "react-dom/client";
import App from "./src/App.jsx";

const rootElement = document.getElementById("root");

if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
} else {
  console.error("💥 Missing <div id='root'></div> in index.html");
}
