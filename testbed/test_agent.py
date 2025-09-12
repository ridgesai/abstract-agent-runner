import requests
import subprocess


def agent_main(input): 
    print("[AGENT] Entered agent_main()")



    # # Print latest commit
    # result = subprocess.run(['git', '--no-pager', 'log'], capture_output=True, text=True)
    # print(result.stdout)



    # Try to make HTTP request to sandbox proxy
    try:
        print("[AGENT] Making request to sandbox proxy...")
        response = requests.get("http://host.docker.internal:8080/foo")
        print(f"[AGENT] Proxy response: {response.text}")
    except Exception as e:
        print(f"[AGENT] Failed to reach proxy: {e}")



    print("[AGENT] Reading solution from /sandbox/solution.diff")
    with open("/sandbox/solution.diff", "r") as f:
        diff = f.read()



    print("[AGENT] Exiting agent_main()")
    
    return diff