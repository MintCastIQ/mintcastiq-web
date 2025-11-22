# MintCastIQ Development Guide
## Overview
- MintCastIQ is a contributor‑safe pipeline for trading card capture, grading, and benchmarking.  
- This guide documents the development environment, contributor workflow, and host GPU worker setup.
---
## Install Docker
### Option 1 Quick Install Debian/Ubuntu
```bash
sudo apt update
sudo apt install docker.io
sudo systemctl enable --now docker
```
### Option 2 Latest Docker CE & Compose v2 (Recommended)
```bash
# Install prerequisites
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release

# Add Docker’s official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Add Docker repo
echo \
  "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker CE + CLI + Compose plugin
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```
## Contributor Workflow
- **Primary focus**: CPU‑safe development in VMs or local environments.
- **Endpoints**: Contributors interact with the GPU worker via HTTP API.
  - `/benchmark` → runs a matrix multiplication benchmark
  - `/process` → accepts JSON payloads for card processing
- **Fallback logic**: If GPU acceleration is unavailable, code runs in CPU mode with identical results.
Contributors **do not need ROCm or GPU drivers**.  
They only need:
- Python 3.10+
- Flask
- Torch (CPU build is sufficient)
---
## Host GPU Worker (Audit Record)
The homelab host runs the accelerated worker service.  
Documented environment for reproducibility:
- **Hardware**: AMD GPU (RX series)
- **Driver stack**: ROCm 7.1
- **Python environment**: venv at `/opt/gpu_worker/gpuvenv`
- **Key packages**:
  - `torch` (ROCm build)
  - `flask`
- **Systemd service**: `gpu-worker.service`  
  - Runs `/opt/gpu_worker/worker.py` via venv interpreter
  - Exposes API on `http://<host-ip>:9091`
---
## Connectivity
  ```bash
  curl http://<host-ip>:9091/benchmark
  ```
Firewall must allow inbound traffic on chosen port.
### Service User and Port Binding Notes
- All MintCastIQ services run under the dedicated `mintcastiq` service account for audit‑grade clarity.
- Flask (frontend.py) must **not** bind directly to privileged ports (<1024) when running under non‑root users.
  - Attempting to bind to port 80 or 443 as `mintcastiq` will result in `Permission denied` errors in systemd logs.
  - Example log snippet:
    ```
    * Serving Flask app 'frontend'
    * Debug mode: off
    Permission denied
    ```
- **Resolution Options:**
  1. Run Flask on an unprivileged port (e.g. 8080) and proxy traffic from 80/443 using nginx or another reverse proxy.
  2. Alternatively, grant the Python binary `cap_net_bind_service` capability:
     ```bash
     sudo setcap 'cap_net_bind_service=+ep' /opt/mintcastiq-web/webvenv/bin/python3
     ```
     This allows binding to low ports without root, but is less contributor‑friendly.
- **Recommended practice:** Use port 8080 for the Flask service and configure nginx to proxy external requests to it. This keeps the service user clean and avoids privileged port issues.
### Reverse Proxy with nginx
To serve MintCastIQ on standard HTTP/HTTPS ports while keeping Flask on an unprivileged port (e.g. 8080), configure nginx as a reverse proxy:
1. Install nginx:
   ```bash
   sudo apt install nginx
2. Create a site config /etc/nginx/sites-available/mintcastiq:
   ```Nginx
   server {
    listen 80;
    server_name mintcastiq.ts.net;
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
  }
```
3. Enable the site
```bash
sudo ln -s /etc/nginx/sites-available/mintcastiq /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```
4. Use certbot (optional)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d mintcastiq.ts.net
```
### Systemd Units

MintCastIQ uses systemd to manage both the Flask frontend and the nginx reverse proxy. This ensures services start on boot, restart on failure, and run under the correct service accounts.
```ini
[Unit]
Description=MintCastIQ Frontend Web Service
After=network.target

[Service]
User=mintcastiq
Group=mintcastiq
WorkingDirectory=/opt/mintcastiq-web
ExecStart=/opt/mintcastiq-web/webvenv/bin/python /opt/mintcastiq-web/frontend.py
Restart=always
EnvironmentFile=/opt/mintcastiq-web/.env
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
```
### Reverse Proxy (nginx)
File: /etc/systemd/system/nginx.service (usually provided by the package manager)

- nginx runs as www-data by default.
- Ensure the MintCastIQ site config is enabled (/etc/nginx/sites-enabled/mintcastiq).
- Systemd will manage nginx automatically once installed.

Check status:
```bash
sudo systemctl status nginx
```
Enable on boot:
```bash
sudo systemctl enable nginx
```
Restart after config changes:
```bash
sudo systemctl reload nginx

```
### Contributor Notes
- Frontend runs on port 8080 under the mintcastiq service user.
- nginx proxies requests from port 80/443 → 8080.
- Both services are managed by systemd and should be enabled on boot.
- If you see Permission denied in logs, check for privileged port binding (Flask must not bind directly to 80/443).


#### Frontend (Flask)

File: `/etc/systemd/system/mintcastiq-web.service`

## Development Standards
Audit clarity: Every architectural decision logged in this guide.
Environment reproducibility: Record GPU model, ROCm version, and PyTorch build.
Contributor safety: No hardware requirements; CPU fallback always available.
API contract: Endpoints documented and stable.
## Example Test
### PRISM endpoint
CPU processing will be used due to the effort level involved in aligning Ubuntu with an AMD GPU.

To see the health of the endpoint or process images
```bash
curl http://mintcastiq-gpu.tail0cc642.ts.net/benchmark
curl http://mintcastiq-gpu.tail0cc642.ts.net/process (not implemented)
```
### Expected response
{"status":"ok","result_shape":[10000,10000]}
## Notes
- Contributors should not attempt ROCm installation unless they are running their own GPU worker.
- Host environment details are included here for audit reproducibility only.
- Future versions may add reverse proxy routing for multiple workers.
