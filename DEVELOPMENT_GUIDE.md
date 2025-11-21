# Development Guide

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
│ └── tsconfig.json ├
── nginx/ 
├── logs/ 
└── webvenv/


## Local Dev
- Run Flask API: `python api.py`
- Run React dev server: `npm run dev`
- Access at: `http://localhost:5173` (frontend), `http://localhost:5001/api/...` (backend)

## Deployment
- Build frontend: `npm run build` → `dist/`
- nginx config:
  - `/` → `frontend-vite/dist`
  - `/api/` → Flask backend

## Contributor Safety
- Each section isolated in `/sections`.
- Shared UI in `/components`.
- Layouts wrap sections for modular composition.
- Explicit logging in backend for forensic validation.
