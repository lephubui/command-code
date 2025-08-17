import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 1028,   // your preferred port
    open: true    // auto-open browser
  }
});
