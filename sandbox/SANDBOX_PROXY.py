import uvicorn
from fastapi import FastAPI



app = FastAPI()



@app.get("/foo")
async def handle_foo():
    print("[SANDBOX_PROXY] GET /foo")
    return "foo"



def main():
    port = 8080
    
    print(f"[SANDBOX_PROXY] Starting sandbox proxy on port {port}")
    
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="error")



if __name__ == "__main__":
    main()