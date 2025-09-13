"""
TODO: This file should eventually be replaced by either nginx, or a more robust proxy service.
      It should also not be run automatically by the SandboxManager.
      Users should be able to specify what proxies they want to use for their sandboxes.
"""

import os
import uvicorn
import requests
from fastapi import FastAPI, Request, Response, HTTPException



app = FastAPI()



FORWARD_TO = os.getenv("FORWARD_TO")



@app.post("/api/inference")
async def proxy_inference(request: Request):
    return await forward_post_request(request, "/api/inference")



@app.post("/api/embedding")
async def proxy_embedding(request: Request):
    return await forward_post_request(request, "/api/embedding")



async def forward_post_request(request: Request, path: str):
    forward_to_url = f"{FORWARD_TO}{path}"
    
    print(f"[SANDBOX_PROXY] POST {path} -> {forward_to_url}")
    
    try:
        body = await request.body()
        
        response = requests.post(
            url=forward_to_url,
            headers={"Content-Type": "application/json"},
            data=body,
            timeout=600
        )
        
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers={"Content-Type": response.headers.get("content-type")}
        )
        
    except requests.exceptions.Timeout:
        print(f"[SANDBOX_PROXY] Timeout forwarding request to {forward_to_url}")
        raise HTTPException(status_code=504, detail="Proxy timeout forwarding request")
    except requests.exceptions.RequestException as e:
        print(f"[SANDBOX_PROXY] Error forwarding request to {forward_to_url}: {e}")
        raise HTTPException(status_code=502, detail="Proxy error forwarding request")
    except Exception as e:
        print(f"[SANDBOX_PROXY] Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Proxy unexpected error")



def main():
    host = "0.0.0.0"
    port = 80
    
    print(f"[SANDBOX_PROXY] Starting sandbox proxy on {host}:{port}")
    print(f"[SANDBOX_PROXY] Forward to: {FORWARD_TO}")
    
    uvicorn.run(app, host=host, port=port, log_level="error")



if __name__ == "__main__":
    main()