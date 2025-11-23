# MintCastIQ
- MintCastIQ is a **web‑first platform** designed for resilient, audit‑grade trading card workflows.  
- Originally prototyped as an Android app, MintCastIQ has shifted focus to the web, with a mobile companion planned for the future.
---
## 🚀 Vision
- Build contributor‑safe, forensic‑grade pipelines for trading card capture and validation.
- Empower contributors with ergonomic tooling, clear documentation, and audit‑ready workflows.
## 📂 Repository Contents
- `README.md` — overview and vision
- `CONTRIBUTING.md` — guidelines for safe and effective collaboration
- `PRIVACY.md` — transparency on data handling and contributor safety
- `DEVELOPMENT_GUIDE.md` — technical standards, workflows, and onboarding notes
---
## Features
- Full Django stack (no React/Node)
- PostgreSQL integration (external VFM instance)
- REST API powered by Django REST Framework
- Contributor-friendly Docker setup

## Quick Start
```bash
git clone https://github.com/<your-org>/mintcastiq-web.git
cd mintcastiq-web
cp .env.example .env   # fill in DB credentials
docker compose up -d
## 🧩 Getting Started
Clone the repository:
```bash
git clone https://github.com/MintCastIQ/MintCastIQ.git
cd MintCastIQ
```
### Create a Python virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --no-cache-dir -r requirements.txt
```
## 🔒 Principles
- **Audit‑grade clarity**: Every workflow is documented and reproducible.
- **Contributor safety**: No secrets or personal data in commits.
- **Modularity**: Infrastructure and tooling are designed for scale and adaptability.
---
## 🤝 Community
- MintCastIQ thrives on collaboration.  
- Please read the [`CONTRIBUTING.md`](CONTRIBUTING.md) before submitting pull requests
- Join discussions to help shape the roadmap.
---
## 📜 License
This project will be released under an open‑source license (to be finalized).  
All contributions are subject to review for audit clarity and contributor safety.
