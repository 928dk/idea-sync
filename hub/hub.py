from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import httpx
import hmac
import logging
import os

logger = logging.getLogger(__name__)

OLLAMA_URL = "http://localhost:11434"
REQUEST_TIMEOUT = 30.0


def _get_access_token() -> str:
    token = os.environ.get("GRID_ACCESS_TOKEN")
    if not token:
        raise RuntimeError(
            "GRID_ACCESS_TOKEN environment variable is not set. "
            "Set it before starting the hub."
        )
    return token


@asynccontextmanager
async def lifespan(_app: FastAPI):
    _get_access_token()
    yield


app = FastAPI(title="AI Grid Smartphone Hub", lifespan=lifespan)
security = HTTPBearer()


def verify_token(auth: HTTPAuthorizationCredentials = Security(security)):
    if not hmac.compare_digest(auth.credentials, _get_access_token()):
        raise HTTPException(status_code=401, detail="Invalid Token")
    return auth.credentials


class ProxyRequest(BaseModel):
    model: str
    prompt: str
    stream: bool = False


@app.post("/proxy/generate")
async def proxy_generate(payload: ProxyRequest, token: str = Depends(verify_token)):
    """Proxies request to local Ollama grid with optional compression."""
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            resp = await client.post(f"{OLLAMA_URL}/api/generate", json=payload.model_dump())
            data = resp.json()
            return data
    except Exception:
        logger.exception("Proxy request to Ollama failed")
        raise HTTPException(status_code=502, detail="Upstream request failed")


@app.get("/status")
async def get_status():
    return {"status": "GRID_ONLINE", "nodes": "autodiscovering"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
