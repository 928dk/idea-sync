from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests
import gzip
import json
import os

app = FastAPI(title="AI Grid Smartphone Hub")
security = HTTPBearer()

# CONFIG
OLLAMA_URL = "http://localhost:11434"
ACCESS_TOKEN = "your-secret-token-here" # Change this!

def verify_token(auth: HTTPAuthorizationCredentials = Security(security)):
    if auth.credentials != ACCESS_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid Token")
    return auth.credentials

@app.post("/proxy/generate")
async def proxy_generate(payload: dict, token: str = Depends(verify_token)):
    """Proxies request to local Ollama grid with optional compression."""
    try:
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, stream=False)
        data = resp.json()
        
        # In a real scenario, we could compress here if the client requests it
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_status():
    return {"status": "GRID_ONLINE", "nodes": "autodiscovering"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
