# MintCastIQ Development Guide
This guide documents the development environment, contributor workflow, architectural standards, and validation patterns used throughout MintCastIQ. It is designed to ensure audit‑grade clarity, reproducibility, and contributor safety.

## I Overview
### MintCastIQ is a contributor‑safe, forensic‑grade platform for trading card capture, grading, and benchmarking. Development emphasizes:

- deterministic ingest pipelines
- modular Django architecture
- reproducible environments
-  explicit documentation and logging

## II Prerequisites
### Ensure the following are installed:
```
Docker & Docker Compose
Git
Python 3.12+
Database of your choice
```

## III Clone the Repository
```bash
git clone https://github.com/MintCastIQ/mintcastiq-web.git
cd mintcastiq-web
```
## IV Docker Installation
### Option A — Quick Install (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install docker.io
sudo systemctl enable --now docker
```
### Option B — Latest Docker CE & Compose v2 (Recommended)
#### Install prerequisites
```bash
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release
```
#### Add Docker’s GPG key
```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```
#### Add Docker repo
```bash
echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
| sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
#### Install Docker CE + Compose
```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
## V Build & Run the Stack
docker compose build --no-cache
docker compose up -d
```
#### Verify Django is running
```bash
curl -s http://localhost:8000/ | head -20
```
## VI Database Connectivity
### Run migrations to confirm DB connectivity:

```bash
docker compose exec web python backend/manage.py showmigrations
```
### Common Issues
- ModuleNotFoundError → check requirements.txt
- DB connection errors → verify .env matches VFM Postgres
- Static files → ensure STATIC_ROOT and BASE_DIR are correct

## VII Contributor Workflow
### Branching
Always branch from develop:

```bash
git checkout develop
git pull
git checkout -b feature/<slug>
```
### Branch Naming
#### Prefixes:

- feature/ — new functionality
- fix/ — bug fixes
- docs/ — documentation
- test/ — tests or CI
- chore/ — maintenance
- hotfix/ — urgent fixes

#### Format:

- lowercase
- hyphen‑separated
- 3–5 words

#### Examples:

- feature/db-factory-tests
- fix/postgres-uri-validation
- docs/add-testing-guide

#### Issue Reference
- Append issue ID if applicable:
- feature/db-factory-tests-42

### Lifecycle
- Rebase or rebranch if divergence occurs
- Delete merged branches
- Never push directly to main
- All merges go through PR + merge queue

### Contributor Checklist
- Correct branch prefix
- Linked issue in PR
- Tests passing
- Branch deleted after merge

## VIII Folder Layout

mintcastiq-web/
├── backend/
│   ├── core/
│   ├── manage.py
│   ├── mintcastiq/
│   │   └── settings.py
│   └── staticfiles/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── webvenv/
## IX Docstring Style Guide
- Use explicit, structured docstrings for audit clarity.

### General Format
```Code
"""
[One-line summary]

[Extended description]

Args:
    arg (type): Description.
Returns:
    type: Description.
Raises:
    ExceptionType: Conditions.
Example:
    >>> result = fn("input")
"""
```
### Validator Example
```python
def validate_slug(value):
    """
    Validates that a slug contains only lowercase letters, numbers, and hyphens.
    Ensures audit-safe identifiers for DimCard objects.

    Args:
        value (str): Slug to validate.
    Raises:
        ValidationError: If invalid.
    """
```
### Model Method Example
```python
def clean(self):
    """
    Validates cross-field integrity for DimCard.
    Ensures hash_count is exactly 10.
    """
```
## X Soft Delete & Status Enum
### MintCastIQ uses soft deletion to preserve audit history.

- Status.ACTIVE → visible
- Status.INACTIVE → soft‑deleted

### Managers:

- objects → all rows
- active → only active rows

#### Example:

```python
obj.soft_delete()
obj.restore()
YourModel.active.all()
```
## XI Hash Run Integrity
Each card image produces 10 positional hashes per hash_run.

Constraint
```python
models.UniqueConstraint(
    fields=["card", "hash_run", "hash_position"],
    name="unique_card_run_position"
)
```
Verification Script
```bash
python manage.py shell -c "
from app.models import DimCardHash, Card;
card = Card.objects.first();
for run in DimCardHash.objects.filter(card=card).values_list('hash_run', flat=True).distinct():
    count = DimCardHash.objects.filter(card=card, hash_run=run).count()
    print(f'Card {card.id}, run {run}: {count} positions')"
```
## XII Parallels: Abstract vs Concrete
Abstract (Set‑level)
Stored in DimParallel Example: “Diamante” for 2025 Topps Baseball

Concrete (Card‑level)
Stored in DimCardParallel Example: Card #12345 → Diamante

Relationships
Code
DimSet
 └── DimParallel
      └── DimCardParallel
           └── DimCard
## XIII Component Tracking
Component	Status	Assignee	Tests	Dependencies
Header	🟡 In Progress	@username	✅	Base template
Footer	🔵 Not Started	—	❌	Base template
Menu/Nav	🔵 Not Started	—	❌	Context processor
Base.html	🟢 Complete	@maintainer	✅	—
## XIV Color Scheme
Role	Hex	Notes
Primary	#005f73	Deep teal
Secondary	#0a9396	Bright teal
Accent	#94d2bd	Soft aqua
Background	#e9d8a6	Warm sand
Highlight	#ee9b00	Amber
Alert	#ca6702	Burnt orange
Success	#2a9d8f	Green‑blue
Neutral Dark	#001219	High contrast
Neutral Mid	#7d8597	Muted gray
Neutral Light	#fefefe	White
## XV Best Practices
Always include runnable examples

Explain why, not just what

Use consistent terminology:

“forensic validation”

“contributor‑safe”

“audit‑grade”


