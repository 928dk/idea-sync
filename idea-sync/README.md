# AI Grid Smartphone Sync

This project provides a secure bridge between your Samsung mobile devices and your home Ollama compute grid.

## How it works:
1.  **Home Hub**: Runs a FastAPI server that acts as a secure entry point.
2.  **Authentication**: Uses a Bearer Token to ensure only your devices can access the grid.
3.  **Proxy**: Forwards AI requests to your local nodes (localhost, 198.51.100.10, etc.).

## Setup (Home Server):
1.  Run the hub:
    ```bash
    ./launch_hub.sh
    ```
2.  Ensure port **8888** is open on your router/firewall if you want to access it from work.

## Mobile Usage (Samsung Device):
1.  Install **Termux** or a Python environment on your phone.
2.  Copy `mobile/client.py` to your device.
3.  Update the `HUB_URL` with your home's public IP.
4.  Run the client to send prompts to your home supercomputer!

## Data Optimization:
The hub is designed to handle large AI responses efficiently to minimize mobile data usage.
