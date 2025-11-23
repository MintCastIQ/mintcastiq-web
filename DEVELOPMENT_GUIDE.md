# MintCastIQ Development Guide
## Overview
- MintCastIQ is a contributor‑safe pipeline for trading card capture, grading, and benchmarking.  
- This guide documents the development environment, contributor workflow, and host worker setup.
---
## Prerequisites
- Docker & Docker Compose installed
- Git installed
- Access to `.env` file with Postgres credentials (provided separately)
---
## Clonme the repository
```bash
git clone https://github.com/MintCastIQ/mintcastiq-web.git
```
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
```

### Add Docker’s official GPG key
```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

### Add Docker repo
```bash
echo \
  "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### Install Docker CE + CLI + Compose plugin
```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```
### Build and Run
```bash
docker compose build --no-cache
docker compose up -d
```
### Verify
```bash
# Django is running
curl -s http://localhost:8000/ | head -20

# Database connectivity
docker compose exec web python backend/manage.py showmigrations
```
### Common Troubleshooting
- ModuleNotFoundError → check spelling in requirements.txt.
- DB connection errors → confirm .env matches your VFM Postgres.
- Static files → ensure BASE_DIR and STATIC_ROOT are defined in settings.py.

## Contributor Workflow
- **Primary focus**: CPU‑safe development in VMs or local environments.
- **Endpoints**: Contributors interact with the worker via HTTP API.
## Architecture
- Python and Django
- Docker
- Postgres

## Folder Layout
/opt/mintcastiq-web/ 
├── backend
│   ├── core
│   ├── manage.py
│   ├── mintcastiq
│   │   ├── __pycache__
│   │   └── settings.py
│   └── staticfiles
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── webvenv

---

## 🌿 Git Branch Naming Policy
To maintain clarity and audit‑grade workflows, all branches must follow these conventions:

### Prefix by Purpose
- feature/ → new functionality
- fix/ → bug fixes
- docs/ → documentation changes
- test/ → testing or CI improvements
- chore/ → maintenance, cleanup, dependency bumps
- hotfix/ → urgent production fixes

### Slug Format
- Use lowercase words separated by hyphens (-).
- Keep names short but descriptive (3–5 words).

### Example:
```bash
feature/db-factory-tests
docs/add-testing-guide
fix/postgres-uri-validation
```
### Issue/Ticket Reference
If the branch relates to a GitHub Issue append the ID:
```bash
feature/db-factory-tests-#42
fix/postgres-uri-validation-#17
```
### Lifecycle Rules
- Branches must be rebased or rebranched if divergence occurs.
- Delete merged branches promptly to avoid stale history.
- Contributors should never push directly to main. Always use a PR workflow.

### Contributor Checklist
✅ Create branch with correct prefix and slug.
✅ Link branch to issue/ticket in PR description.
✅ Ensure all tests pass before merge.
✅ Delete branch after merge.
