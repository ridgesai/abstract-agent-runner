import os
import uvicorn
from fastapi import FastAPI



PROXY_HOST = os.environ["PROXY_HOST"]
PROXY_PORT = int(os.environ["PROXY_PORT"])



app = FastAPI(title="Inference Proxy", description="Inference proxy server with embedding and inference endpoints, forwards whitelisted requests to Chutes and Targon")



@app.get("/api/inference")
async def inference():
    """Inference endpoint - returns 200 OK for now."""
    return {"status": "ok"}



@app.get("/api/embedding") 
async def embedding():
    """Embedding endpoint - returns 200 OK for now."""
    return {"status": "ok"}



if __name__ == "__main__":
    uvicorn.run(app, host=PROXY_HOST, port=PROXY_PORT)
