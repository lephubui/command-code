from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
import asyncio
import json
import random
from datetime import datetime

app = FastAPI()

# Simulated data generator
async def data_stream():
    while True:
        data = {
            "timestamp": datetime.now().isoformat(),
            "value": random.randint(1, 100),
            "metric": f"metric_{random.choice(['A', 'B', 'C'])}"
        }
        yield f"data: {json.dumps(data)}\n\n"
        await asyncio.sleep(1)  # Stream data every second

# Route for the dashboard
@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Real-Time Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            #data { margin-top: 20px; }
            .metric { margin: 10px 0; padding: 10px; border: 1px solid #ccc; }
        </style>
    </head>
    <body>
        <h1>Real-Time Metrics Dashboard</h1>
        <div id="data"></div>
        <script>
            const eventSource = new EventSource('/stream');
            eventSource.onmessage = function(event) {
                const data = JSON.parse(event.data);
                const div = document.createElement('div');
                div.className = 'metric';
                div.textContent = `Metric: ${data.metric}, Value: ${data.value}, Time: ${data.timestamp}`;
                document.getElementById('data').prepend(div);
            };
        </script>
    </body>
    </html>
    """

# Route for streaming data
@app.get("/stream")
async def stream():
    return Response(data_stream(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)