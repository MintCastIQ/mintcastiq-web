# MintCastIQ
MintCastIQ is a **web‑first platform** for resilient, audit‑grade trading card workflows. Originally prototyped as an Android app, the project has shifted to a browser‑centric architecture, with a mobile companion planned for the future.

## 🚀 Vision
- Build contributor‑safe, forensic‑grade pipelines for trading card capture, validation, and provenance.
- Empower contributors with ergonomic tooling, clear documentation, and audit‑ready workflows.
- Maintain a modular, scalable architecture that supports community growth and future automation.

## 📂 Repository Structure
- README.md — project overview and vision
- CONTRIBUTING.md — collaboration and workflow guidelines
- PRIVACY.md — data handling and contributor safety
- DEVELOPMENT_GUIDE.md — environment setup, standards, and onboarding
- Django backend (mintcastiq/)
- Docker configuration (docker-compose.yml)

## ✨ Features
- Full Django stack (no React/Node)
- PostgreSQL integration (external VFM instance)
- REST API powered by Django REST Framework
- Contributor‑friendly Docker setup
- Audit‑grade ingest and validation pipelines

## 🧩 Getting Started
### Clone the repository
```Bash
git clone https://github.com/MintCastIQ/mintcastiq-web.git
cd mintcastiq-web
```
### Create a Python virtual environment
```Bash
python3 -m venv venv
source venv/bin/activate
pip install --no-cache-dir -r requirements.txt
```
### Environment configuration
```Bash
cp .env.example .env
# Fill in DB credentials and service configuration
```
### Run with Docker
```Bash
docker compose up -d
```
## Principles
- Audit‑grade clarity — every workflow is documented, reproducible, and contributor‑safe.
- No secrets in commits — contributors must avoid committing personal data or credentials.
- Modularity — infrastructure, ingest pipelines, and services are designed for scale and adaptability.
- Determinism — ingest and validation workflows avoid destructive operations and preserve provenance.

## 🤝 Community
MintCastIQ thrives on collaboration.
- Read the CONTRIBUTING.md before submitting pull requests.
- Participate in discussions to help shape the roadmap and contributor experience.

## 📜 License
The project will be released under an open‑source license (to be finalized). All contributions are reviewed for audit clarity and contributor safety.