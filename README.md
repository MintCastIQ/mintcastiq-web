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

## Installation

### Backend
```bash
python3 -m venv webvenv
source webvenv/bin/activate
pip install -r requirements.txt
python api.py
```

### Frontend
```bash
cd frontend-vite
npm install
npm run dev   # local dev server
npm run build # production build -> dist/
```

### nginx
- Config lives in /etc/nginx/sites-available/mintcastiq.conf
- Symlink into sites-enabled/:
```bash
sudo ln -s /etc/nginx/sites-available/mintcastiq.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Deployment
- nginx serves frontend-vite/dist
- Flask API proxied at /api/
