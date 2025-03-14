import agentops
import requests
import os

agentops_api_key = os.getenv("AGENTOPS_API_KEY")

agentops.init(
    api_key=agentops_api_key,
    agent_name="SIEM-Agent"
)

@agentops.monitor
def handle_request(user_input):
    response = f"Response to: {user_input}"
    
    # Send log to backend
    log = {
        "input": user_input,
        "response": response,
        "status": "success"
    }
    try:
        requests.post("http://localhost:5000/log", json=log)
    except Exception as e:
        print(f"Failed to send log: {e}")

    return response