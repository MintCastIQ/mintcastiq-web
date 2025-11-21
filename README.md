# MintCastIQ

MintCastIQ is a modular, contributor‑safe platform for forensic trading card capture and grading.

## Project Structure
- **backend/** → Flask API (Python 3.12)
- **api.py** → API entry point
- **frontend-vite/** → React + Vite frontend
- **nginx/** → nginx config for serving frontend + proxying API
- **logs/** → runtime logs (ignored in git)
- **webvenv/** → Python virtual environment (ignored in git)

## Requirements
- Node.js ≥ 20.20.0 (or 21.x)
- Python 3.12
- Flask (see `requirements.txt`)
- nginx

## Quick Start
```bash
# Backend
python3 -m venv webvenv
source webvenv/bin/activate
pip install -r requirements.txt
python api.py

# Frontend
cd frontend-vite
npm install
npm run dev   # local dev server
npm run build # production build -> dist/

## Deployment
- nginx serves frontend-vite/dist
- Flask API proxied at /api/


