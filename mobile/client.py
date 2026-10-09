import os
import requests

HUB_URL = os.environ.get("GRID_HUB_URL", "http://your-home-ip:8888")
TOKEN = os.environ.get("GRID_ACCESS_TOKEN")
if not TOKEN:
    raise RuntimeError("GRID_ACCESS_TOKEN environment variable is not set.")


def ask_grid(prompt, model="llama3.2:1b"):
    headers = {"Authorization": f"Bearer {TOKEN}"}
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    print(f"Sending request to Home Grid...")
    try:
        response = requests.post(f"{HUB_URL}/proxy/generate", json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json().get('response', '')
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Connection Failed: {e}"

if __name__ == "__main__":
    res = ask_grid("What is the status of the compute grid?")
    print(f"Grid Response: {res}")
