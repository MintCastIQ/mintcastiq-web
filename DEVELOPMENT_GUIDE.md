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
## Architecture
- **Frontend**: React + Vite, modular sections (`FormSection`, `ResultsSection`, `OverlaySection`, `InventorySection`, `ChecklistSection`).
- **Backend**: Flask API, routes under `/api/`.
- **nginx**: Serves React build, proxies API.

## Folder Layout
/opt/mintcastiq-web/ 
├── api.py 
├── backend/ 
├── frontend-vite/ 
│ ├── src/ (components, sections, layouts) 
│ ├── public/ 
│ ├── vite.config.ts 
│ └── tsconfig.json 
├── nginx/ 
├── logs/ 
└── webvenv/
---

## Local Development
### Run Flask API:
```bash
  source webvenv/bin/activate
  python api.py
```
### Run React dev server:
```bash
cd frontend-vite
npm run dev
```
### Access at:
- Frontend → http://localhost:5173
- Backend → http://localhost:5001/api/...

### Deployment
Build frontend:
```bash
cd frontend-vite
npm run build
```
### nginx config:
- / → frontend-vite/dist
- /api/ → Flask backend

## Contributor Checklist
- Before committing:
- [ ] Run npm run lint (frontend)
- [ ] Run pytest (backend)
- [ ] Verify routes (/api/...) respond correctly
- [ ] Confirm build succeeds (npm run build)
- [ ] Ensure no logs, venv, or node_modules committed

Package Installs
Frontend:
```bash
npm install react react-dom react-router-dom
npm install -D typescript vite eslint prettier
```
Backend
```bash
pip install flask flask-cors
pip install pytest
```

