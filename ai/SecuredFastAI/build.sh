#!/usr/bin/env bash
set -e

PROJECT="FastSecuredIX"
ZIP="${PROJECT}.zip"

# Start fresh
rm -rf "$PROJECT"
rm -f "$ZIP"

echo "Creating folder layout..."
mkdir -p \
  "$PROJECT/backend" \
  "$PROJECT/dashboard/src" \
  "$PROJECT/ml_jobs" \
  "$PROJECT/aistore"

#############################
# docker-compose.yml
#############################
cat > "$PROJECT/docker-compose.yml" << 'EOF'
version: '3.9'
services:
  aistore:
    image: nexenta/aistore:latest
    environment: [AIS_IS_PRIMARY=true]
    volumes:
      - ./aistore/ais.json:/etc/ais/ais.json
    ports: ["8080:8080"]

  backend:
    build: ./backend
    environment:
      - AIS_ENDPOINT=http://aistore:8080
      - PORT=2892
    ports: ["2892:2892"]
    depends_on: [aistore]

  mljob:
    build: ./ml_jobs
    environment: [AIS_ENDPOINT=http://aistore:8080]
    depends_on: [aistore]

  dashboard:
    build: ./dashboard
    ports: ["3000:3000"]
    depends_on: [backend]

volumes:
  aistore_data:
EOF

#############################
# aistore config
#############################
cat > "$PROJECT/aistore/ais.json" << 'EOF'
{
  "cluster": { "primary_url": "http://aistore:8080" }
}
EOF

#############################
# backend
#############################
cat > "$PROJECT/backend/requirements.txt" << 'EOF'
fastapi
uvicorn
boto3
EOF

cat > "$PROJECT/backend/Dockerfile" << 'EOF'
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","2892"]
EOF

cat > "$PROJECT/backend/main.py" << 'EOF'
from fastapi import FastAPI, UploadFile, File
import os, boto3

client=boto3.client('s3',endpoint_url=os.getenv("AIS_ENDPOINT"))
bucket="logs"
try: client.create_bucket(Bucket=bucket)
except: pass

app=FastAPI()

@app.post("/ingest")
async def ingest(f:UploadFile=File(...)):
    data=await f.read()
    client.put_object(Bucket=bucket,Key=f.filename,Body=data)
    return {"ok":True}

@app.get("/logs")
def logs():
    r=client.list_objects_v2(Bucket=bucket)
    return {"objects":[o['Key'] for o in r.get("Contents",[])]}
EOF

#############################
# ml job
#############################
cat > "$PROJECT/ml_jobs/requirements.txt" << 'EOF'
torch
boto3
EOF

cat > "$PROJECT/ml_jobs/Dockerfile" << 'EOF'
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python","infer.py"]
EOF

cat > "$PROJECT/ml_jobs/infer.py" << 'EOF'
import boto3,os
s=boto3.client("s3",endpoint_url=os.getenv("AIS_ENDPOINT","http://localhost:8080"))
for o in s.list_objects_v2(Bucket="logs").get("Contents",[]):
  d=s.get_object(Bucket="logs",Key=o["Key"])["Body"].read().splitlines()
  print(o["Key"],"ALERT" if len(d)>1000 else "OK")
EOF

#############################
# dashboard
#############################
cat > "$PROJECT/dashboard/Dockerfile" << 'EOF'
FR
